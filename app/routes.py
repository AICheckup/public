from flask import Blueprint, request, jsonify
from app.models import DiagnosisModel  # Import the DiagnosisModel class
from app.utils import get_health_advice, find_nearby_hospitals  # Import the utility functions

# Create a Blueprint for the routes
bp = Blueprint('routes', __name__)

# Load the trained model (replace 'diagnosis_model.joblib' with your actual model path if different)
try:
    model = DiagnosisModel(model_path="diagnosis_model.joblib")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None  # Set model to None if loading fails

# Diagnosis endpoint
@bp.route('/diagnose', methods=['POST'])
def diagnose():
    """
    Endpoint to receive symptoms, and return diagnosis results and advice.

    Returns:
        JSON: Diagnosis and advice in JSON format.
    """
    try:
        data = request.get_json()
        symptoms = data['symptoms']

        # Multilingual support will be considered here (e.g., using a translation API)
        # Currently, it assumes English symptoms

        if model:
            # Get the diagnosis from the model
            diagnosis = model.predict(symptoms)
            probabilities = model.predict_proba(symptoms)

            # Get health advice based on the diagnosis
            advice = get_health_advice(diagnosis)

            return jsonify({"diagnosis": diagnosis, "probabilities": probabilities, "advice": advice})
        else:
            return jsonify({"error": "Model not loaded"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Medical institution search endpoint
@bp.route('/find_hospitals', methods=['POST'])
def find_hospitals():
    """
    Endpoint to receive location and return nearby medical institutions.

    Returns:
        JSON: List of nearby medical institutions in JSON format.
    """
    try:
        data = request.get_json()
        location = data['location']

        # Get nearby hospitals using the utility function
        hospitals = find_nearby_hospitals(location)

        return jsonify({"hospitals": hospitals})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
