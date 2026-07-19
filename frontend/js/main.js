let currentData = null;
let evaluationItems = [];

// API URL - 開発環境ではローカル、本番ではデプロイ先
const API_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/predict'
    : 'https://keiba-predict-x1bh.onrender.com/predict';

document.getElementById("predictBtn").addEventListener("click", async () => {
    const url = document.getElementById("raceUrl").value;
    
    if (!url) {
        alert("URLを入力してください");
        return;
    }

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        if (!response.ok) {
            throw new Error("取得に失敗しました");
        }

        currentData = await response.json();
        displayResults();
        
        document.getElementById("searchDiv").style.display = "none";
        document.getElementById("resultDiv").style.display = "block";
    } catch (error) {
        alert(error.message);
    }
});

document.getElementById("backBtn").addEventListener("click", () => {
    document.getElementById("resultDiv").style.display = "none";
    document.getElementById("searchDiv").style.display = "block";
});

document.getElementById("recalcBtn").addEventListener("click", () => {
    if (currentData) {
        recalculate();
    }
});

function displayResults() {
    const info = currentData.info;
    const distance = currentData.distance;
    const ranking = currentData.ranking;
    const horseCount = info.horses.length;

    // レース情報表示
    document.getElementById("raceInfo").innerHTML = `
        <p>場所: ${info.place}</p>
        <p>レース番号: ${info.race_no}</p>
        <p>レース名: ${info.race_name}</p>
        <p>距離: ${info.race_distance}m</p>
        <p>頭数: ${horseCount}頭</p>
    `;

    // 評価項目を動的に生成
    generateEvaluationItems(distance);

    // 総合順位表示
    displayOverallRanking(ranking, horseCount);

    // 集計設定表示
    displayEvaluationSettings();

    // 馬の結果表示
    displayHorseResults(ranking, horseCount);
}

function generateEvaluationItems(distance) {
    evaluationItems = [];
    
    // 全ての場所と距離の組み合わせを収集
    const placeDistanceCombos = new Set();
    distance.forEach(dh => {
        dh.distances.forEach(dd => {
            const key = `${dd.race_place}-${dd.distance}`;
            placeDistanceCombos.add(key);
        });
    });

    // 各組み合わせに対して評価項目を生成
    const fields = [
        { id: 'avg_time', name: '平均タイム' },
        { id: 'avg_last3f', name: '平均上がり' },
        { id: 'best_last3f', name: '最速上がり' },
        { id: 'avg_first_corner_diff', name: '第一コーナー先行指数' },
        { id: 'avg_final_corner_diff', name: '最終コーナー先行指数' }
    ];

    placeDistanceCombos.forEach(combo => {
        const [place, dist] = combo.split('-');
        fields.forEach(field => {
            evaluationItems.push({
                id: `${combo}-${field.id}`,
                name: `${combo} ${field.name}`,
                weight: 1,
                checked: true,
                place: place,
                distance: parseInt(dist),
                field: field.id
            });
        });
    });

    // パドック評価を追加
    evaluationItems.push({
        id: 'paddock',
        name: 'パドック評価',
        weight: 1,
        checked: true,
        isPaddock: true
    });
}

function displayEvaluationSettings() {
    const container = document.getElementById("evaluationSettings");
    container.innerHTML = evaluationItems.filter(item => !item.isPaddock).map(item => `
        <div class="evaluation-item">
            <label>
                <input type="checkbox" 
                       id="check_${item.id}" 
                       ${item.checked ? 'checked' : ''}
                       onchange="updateEvaluationSetting('${item.id}', 'checked', this.checked)">
                ${item.name}
            </label>
            <input type="number" 
                   id="weight_${item.id}" 
                   value="${item.weight}" 
                   min="0.1" 
                   step="0.1"
                   onchange="updateEvaluationSetting('${item.id}', 'weight', this.value)">
        </div>
    `).join('');
}

function displayOverallRanking(ranking, horseCount) {
    const container = document.getElementById("overallRankingList");
    
    // 各馬の総合点を計算
    const horseScores = ranking.map(rh => {
        let totalScore = 0;
        evaluationItems.forEach(item => {
            if (item.checked) {
                if (item.isPaddock) {
                    // パドック評価は後で処理
                } else {
                    const horseRanking = rh.rankings.find(r => r.race_place === item.place && r.distance === item.distance);
                    if (horseRanking) {
                        const rankField = `${item.field}_rank`;
                        const rank = horseRanking[rankField];
                        if (rank !== null && rank !== undefined) {
                            const score = horseCount - rank;
                            totalScore += score * item.weight;
                        }
                    }
                }
            }
        });
        
        // パドック評価を追加
        const paddockItem = evaluationItems.find(e => e.isPaddock);
        if (paddockItem && paddockItem.checked) {
            const paddockValue = currentData.paddockEvaluations && currentData.paddockEvaluations[rh.horse_no] 
                ? currentData.paddockEvaluations[rh.horse_no] 
                : 0;
            totalScore += paddockValue * paddockItem.weight;
        }
        
        return { horse_no: rh.horse_no, totalScore };
    });

    // 総合順位でソート
    horseScores.sort((a, b) => b.totalScore - a.totalScore);

    // 表示
    container.innerHTML = horseScores.map((hs, index) => {
        const paddockValue = currentData.paddockEvaluations && currentData.paddockEvaluations[hs.horse_no] 
            ? currentData.paddockEvaluations[hs.horse_no] 
            : 0;
        const paddockItem = evaluationItems.find(e => e.isPaddock);
        
        return `
            <div class="overall-ranking-item">
                <span class="rank">${index + 1}位</span>
                <span class="horse-no">${hs.horse_no}番</span>
                <span class="total-score">${hs.totalScore.toFixed(1)}点</span>
                <label class="paddock-check">
                    <input type="checkbox" 
                           id="paddock_check_${hs.horse_no}" 
                           ${paddockItem && paddockItem.checked ? 'checked' : ''}
                           onchange="updatePaddockCheck(${hs.horse_no}, this.checked)">
                    パドック
                </label>
                <input type="number" 
                       id="paddock_${hs.horse_no}" 
                       value="${paddockValue}" 
                       min="0" 
                       max="10"
                       class="paddock-input"
                       onchange="updatePaddockEvaluation(${hs.horse_no}, this.value)">
            </div>
        `;
    }).join('');
}

function displayHorseResults(ranking, horseCount) {
    const container = document.getElementById("horseResults");
    
    // 各馬の総合点を計算
    const horseScores = ranking.map(rh => {
        let totalScore = 0;
        evaluationItems.forEach(item => {
            if (item.checked) {
                if (item.isPaddock) {
                    // パドック評価は後で処理
                } else {
                    // 該当する場所と距離のランキングを探す
                    const horseRanking = rh.rankings.find(r => r.race_place === item.place && r.distance === item.distance);
                    if (horseRanking) {
                        const rankField = `${item.field}_rank`;
                        const rank = horseRanking[rankField];
                        if (rank !== null && rank !== undefined) {
                            const score = horseCount - rank;
                            totalScore += score * item.weight;
                        }
                    }
                }
            }
        });
        
        // パドック評価を追加
        const paddockItem = evaluationItems.find(e => e.isPaddock);
        if (paddockItem && paddockItem.checked) {
            const paddockValue = currentData.paddockEvaluations && currentData.paddockEvaluations[rh.horse_no] 
                ? currentData.paddockEvaluations[rh.horse_no] 
                : 0;
            totalScore += paddockValue * paddockItem.weight;
        }
        
        return { horse_no: rh.horse_no, totalScore };
    });

    // 総合順位を計算
    horseScores.sort((a, b) => b.totalScore - a.totalScore);
    const horseRanks = {};
    horseScores.forEach((hs, index) => {
        horseRanks[hs.horse_no] = index + 1;
    });

    // 表示
    container.innerHTML = ranking.map(rh => {
        const horseScore = horseScores.find(hs => hs.horse_no === rh.horse_no);
        
        let evaluationHtml = evaluationItems.map(item => {
            if (item.isPaddock) {
                const paddockValue = currentData.paddockEvaluations && currentData.paddockEvaluations[rh.horse_no] 
                    ? currentData.paddockEvaluations[rh.horse_no] 
                    : 0;
                return `
                    <div class="evaluation-detail">
                        <span>${item.name}:</span>
                        <span>${paddockValue}</span>
                    </div>
                `;
            }
            
            // 該当する場所と距離のランキングを探す
            const horseRanking = rh.rankings.find(r => r.race_place === item.place && r.distance === item.distance);
            if (horseRanking) {
                const rankField = `${item.field}_rank`;
                const rank = horseRanking[rankField];
                const score = rank !== null && rank !== undefined ? horseCount - rank : 0;
                
                return `
                    <div class="evaluation-detail">
                        <span>${item.name}:</span>
                        <span>順位: ${rank !== null && rank !== undefined ? rank : '-'}</span>
                        <span>点数: ${score}</span>
                    </div>
                `;
            }
            
            return '';
        }).join('');

        return `
            <div class="horse-result">
                <h3>馬番: ${rh.horse_no}</h3>
                <p>総合点: ${horseScore.totalScore.toFixed(1)}</p>
                <p>総合順位: ${horseRanks[rh.horse_no]}</p>
                <div class="evaluation-details">
                    ${evaluationHtml}
                </div>
            </div>
        `;
    }).join('');
}

function updateEvaluationSetting(id, field, value) {
    const item = evaluationItems.find(e => e.id === id);
    if (item) {
        item[field] = field === 'checked' ? value : parseFloat(value);
    }
}

function updatePaddockEvaluation(horseNo, value) {
    // パドック評価を保存（再計算時に使用）
    if (!currentData.paddockEvaluations) {
        currentData.paddockEvaluations = {};
    }
    currentData.paddockEvaluations[horseNo] = parseFloat(value);
}

function updatePaddockCheck(horseNo, checked) {
    // パドック評価のチェック状態を更新
    const paddockItem = evaluationItems.find(e => e.isPaddock);
    if (paddockItem) {
        paddockItem.checked = checked;
    }
}

function recalculate() {
    const horseCount = currentData.info.horses.length;
    const ranking = currentData.ranking;
    
    // 各馬の総合点を再計算
    const horseScores = ranking.map(rh => {
        let totalScore = 0;
        evaluationItems.forEach(item => {
            if (item.checked) {
                if (item.isPaddock) {
                    // パドック評価はユーザー入力値を使用
                    const paddockValue = currentData.paddockEvaluations && currentData.paddockEvaluations[rh.horse_no] 
                        ? currentData.paddockEvaluations[rh.horse_no] 
                        : 0;
                    totalScore += paddockValue * item.weight;
                } else {
                    // 該当する場所と距離のランキングを探す
                    const horseRanking = rh.rankings.find(r => r.race_place === item.place && r.distance === item.distance);
                    if (horseRanking) {
                        const rankField = `${item.field}_rank`;
                        const rank = horseRanking[rankField];
                        if (rank !== null && rank !== undefined) {
                            const score = horseCount - rank;
                            totalScore += score * item.weight;
                        }
                    }
                }
            }
        });
        
        return { horse_no: rh.horse_no, totalScore };
    });

    // 総合順位を再計算
    horseScores.sort((a, b) => b.totalScore - a.totalScore);
    
    // 再表示
    displayOverallRanking(ranking, horseCount);
    displayHorseResults(ranking, horseCount);
}