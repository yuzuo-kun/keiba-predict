const button = document.getElementById("predictBtn");

button.addEventListener("click", async () => {

    const url = document.getElementById("raceUrl").value;

    const response = await fetch("https://keiba-predict-x1bh.onrender.com/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            url: url
        })
    });

    if (!response.ok) {
        alert("取得に失敗しました");
        return;
    }

    const blob = await response.blob();

    const downloadUrl = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = "race.html";
    a.click();

    window.URL.revokeObjectURL(downloadUrl);
});