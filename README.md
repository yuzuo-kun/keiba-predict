# keiba-predict
競馬予想を手助け

【概要】
・スマホ向けWebアプリ
・地方競馬の出馬表URLを入力すると、各馬の過去成績を取得し、独自ロジックで予想順位を表示する
・予想結果は画面上に表示し、ファイル出力は行わない

【入力】
・出馬表URL
・予想開始ボタン

【出力】
馬ごとに以下を表示する。
・馬番
・馬名
・総合点
・総合順位

各評価項目について
・値
・順位

【評価項目】
・距離別直近5走平均タイム
・距離別直近5走平均上がり
・全レース平均上がり
・最速上がり
・第一コーナー先行指数
・最終コーナー先行指数
・パドック評価（ユーザー入力）

【順位計算】
各評価項目ごとに順位を算出する。

点数計算式
点数 = 馬数 - (順位 - 1)

例（10頭立て）
1位 = 10点
2位 = 9点
・・・
10位 = 1点

【集計】
各評価項目ごとに以下を持つ。
・集計対象チェックボックス
・重み

総合点は、チェックされている項目のみ
「点数 × 重み」
を合計する。

重みの初期値はすべて「1」。

【パドック評価】
・各馬ごとにユーザーが入力できる
・集計対象に含めるか選択できる

【再計算】
再計算ボタン押下時に以下を反映する。
・集計対象チェック
・パドック評価
・重み
※再スクレイピングは行わず、取得済みデータのみで再計算する。

スマホ
    │
    ▼
HTML + CSS + JavaScript
    │
    ▼
FastAPI
    │
 ┌──┴──────────────┐
 │                 │
 ▼                 ▼
Playwright    Calculator
 │
 ▼
BeautifulSoup
 │
 ▼
JSONレスポンス
 │
 ▼
画面表示

keiba-predict/
│
├── frontend/
│   │
│   ├── index.html              # URL入力画面
│   │
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── main.js
│
└── backend/
    │
    ├── main.py                 # FastAPI起動
    ├── requirements.txt
    │
    ├── api/
    │   └── predict.py          # API
    │
    ├── models/
    │   ├── request.py          # リクエストモデル
    │   └── response.py         # レスポンスモデル（今後追加）
    │
    ├── scraper/
    │   ├── fetcher.py          # HTML取得(requests)
    │   ├── parser.py           # BeautifulSoup解析
    │   └── extractor.py        # 必要データ抽出
    │
    ├── analyzer/
    │   ├── calculator.py       # 評価点計算
    │   ├── ranking.py          # 順位付け
    │   └── distance.py         # 距離別集計
    │
    └── utils/
        └── helper.py