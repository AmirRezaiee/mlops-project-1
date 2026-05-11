@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <head>
        <title>Price Predictor</title>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {
                font-family: Arial;
                background: #121212;
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .card {
                background: #1e1e1e;
                padding: 25px;
                border-radius: 12px;
                width: 650px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
                animation: fadeIn 0.6s ease-in-out;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            h2 {
                text-align: center;
                margin-bottom: 20px;
            }

            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
            }

            input {
                width: 100%;
                padding: 10px;
                border-radius: 6px;
                border: none;
                background: #2c2c2c;
                color: white;
            }

            button {
                width: 100%;
                padding: 12px;
                margin-top: 15px;
                background: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
            }

            button:hover {
                background: #45a049;
            }

            #result {
                margin-top: 15px;
                text-align: center;
                font-weight: bold;
            }

            canvas {
                margin-top: 20px;
            }

            .spinner {
                border: 4px solid #333;
                border-top: 4px solid #4CAF50;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                animation: spin 1s linear infinite;
                margin: auto;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>

    <body>
        <div class="card">
            <h2>🌙 Price Predictor (Dark Mode)</h2>

            <div class="grid">
                <input id="MedInc" placeholder="Median Income">
                <input id="HouseAge" placeholder="House Age">
                <input id="AveRooms" placeholder="Rooms">
                <input id="AveBedrms" placeholder="Bedrooms">
                <input id="Population" placeholder="Population">
                <input id="AveOccup" placeholder="Occupancy">
                <input id="Latitude" placeholder="Latitude">
                <input id="Longitude" placeholder="Longitude">
            </div>

            <button onclick="predict()">Predict</button>

            <div id="result"></div>

            <canvas id="chart"></canvas>
        </div>

        <script>
        let chart;

        function formatCurrency(num) {
            return "$" + num.toLocaleString(undefined, {minimumFractionDigits: 2});
        }

        async function predict() {
            const resultDiv = document.getElementById("result");
            resultDiv.innerHTML = "<div class='spinner'></div>";

            try {
                const data = {
                    MedInc: parseFloat(document.getElementById("MedInc").value),
                    HouseAge: parseFloat(document.getElementById("HouseAge").value),
                    AveRooms: parseFloat(document.getElementById("AveRooms").value),
                    AveBedrms: parseFloat(document.getElementById("AveBedrms").value),
                    Population: parseFloat(document.getElementById("Population").value),
                    AveOccup: parseFloat(document.getElementById("AveOccup").value),
                    Latitude: parseFloat(document.getElementById("Latitude").value),
                    Longitude: parseFloat(document.getElementById("Longitude").value)
                };

                const response = await fetch("/predict", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                resultDiv.innerHTML = "💰 " + formatCurrency(result.predicted_house_value);

                // chart
                const ctx = document.getElementById("chart").getContext("2d");

                if (chart) chart.destroy();

                chart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ["Prediction"],
                        datasets: [{
                            label: "House Price",
                            data: [result.predicted_house_value],
                            backgroundColor: "#4CAF50"
                        }]
                    }
                });

            } catch (err) {
                resultDiv.innerHTML = "❌ Error";
            }
        }
        </script>
    </body>
    </html>
    """