import requests
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Azure ML API Endpoint
SCORING_URI = "http://aadde018-752b-4227-a0c7-6fd6ce4afb12.centralindia.azurecontainer.io/score"
HEADERS = {"Content-Type": "application/json"}

@app.route("/") 
def home():
    return render_template("index.html")  # This will look for 'templates/index.html'

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from frontend
        user_data = request.get_json()
        print("Received JSON Data:", user_data)  # Debugging step

        # Send request to Azure ML API
        response = requests.post(SCORING_URI, json=user_data, headers=HEADERS)
        print("Raw Response Text:", response.text)  # Debugging step

        # Check if API call failed
        if response.status_code != 200:
            return jsonify({"error": f"Azure API Error: {response.text}"}), 500

        # Try parsing response twice (handles double JSON encoding)
        try:
            result = response.json()
        except json.JSONDecodeError:
            result = json.loads(response.text)

        # Handle double-encoded JSON (if necessary)
        if isinstance(result, str):
            result = json.loads(result)

        print("Parsed Response:", result)  # Debugging step

        # Extract prediction
        if isinstance(result, dict) and "predicted_fare" in result:
            prediction = result["predicted_fare"]
            return jsonify({"predicted_fare": prediction})
        else:
            return jsonify({"error": "Invalid response format from Azure API"}), 500

    except Exception as e:
        print("Server Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
