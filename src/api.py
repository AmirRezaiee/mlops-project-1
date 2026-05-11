@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
    <head>
        <title>Price Predictor</title>

        <style>
            body {
                font-family: Arial;
                background: linear-gradient(135deg, #667eea, #764ba2);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }

            .card {
                background: white;
                padding: 25px;
                border-radius: 12px;
                width: 600px;
                box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
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
                border: 1px solid #ccc;
            }

            button {
                width: 100%;
                padding: 12px;
                margin-top: 15px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 16px;
            }

            #result {
                margin-top: 15px;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                border-radius: 6px;
            }

            .success {
                background: #d4edda;
                color: #155724;
            }

            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
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
            <h2>🏠 Price Predictor</h2>

            <div class="grid">
                <input id="MedInc" placeholder="Median Income">
                <input id="HouseAge" placeholder="House Age">

                <input id="AveRooms" placeholder="Average Rooms">
                <input id="AveBedrms" placeholder="Bedrooms">

                <input id="Population" placeholder="Population">
                <input id="AveOccup" placeholder="Occupancy">

                <input id="Latitude" placeholder="Latitude">
                <input id="Longitude" placeholder="Longitude">
            </div>

            <button onclick="predict()">Predict</button>

            <div id="result"></div>
        </div>

        <script>
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

                resultDiv.innerHTML = "💰 Price: " + formatCurrency(result.predicted_house_value);
                resultDiv.className = "success";

            } catch (err) {
                resultDiv.innerHTML = "❌ Error";
            }
        }
        </script>

    </body>
    </html>
    """