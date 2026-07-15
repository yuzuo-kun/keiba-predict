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

    const result = await response.json();

    console.log(result);

    document.getElementById("result").textContent =
        JSON.stringify(result, null, 2);

});