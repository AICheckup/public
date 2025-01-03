import unittest
import os
from app.models import DiagnosisModel

class DiagnosisModelTestCase(unittest.TestCase):
    def setUp(self):
        """
        Setup before each test.
        """
        self.model = DiagnosisModel()
        # Example training data
        self.X_train = ["headache fever", "cough sore throat", "stomach pain nausea"]
        self.y_train = ["migraine", "cold", "gastritis"]

        # Remove the test model if it exists from previous test runs
        if os.path.exists("test_model.joblib"):
            os.remove("test_model.joblib")

    def tearDown(self):
        """
        Cleanup after each test.
        """
        # Remove the test model after each test run
        if os.path.exists("test_model.joblib"):
            os.remove("test_model.joblib")

    def test_create_model(self):
        """
        Test model creation.
        """
        self.assertIsNotNone(self.model.model)

    def test_train_model(self):
        """
        Test model training.
        """
        self.model.train(self.X_train, self.y_train)
        # Add assertions to check if the model is trained correctly
        # For example, check if the model has certain attributes after training

    def test_predict(self):
        """
        Test model prediction.
        """
        self.model.train(self.X_train, self.y_train)
        prediction = self.model.predict("headache")
        self.assertIsInstance(prediction, str)

    def test_predict_proba(self):
        """
        Test model probability prediction.
        """
        self.model.train(self.X_train, self.y_train)
        probabilities = self.model.predict_proba("headache")
        self.assertIsInstance(probabilities, dict)
        self.assertTrue(all(isinstance(value, float) for value in probabilities.values()))

    def test_save_and_load_model(self):
        """
        Test saving and loading the model.
        """
        self.model.train(self.X_train, self.y_train)
        self.model.save_model("test_model.joblib")
        loaded_model = DiagnosisModel(model_path="test_model.joblib")
        self.assertIsNotNone(loaded_model.model)
        prediction = loaded_model.predict("headache")
        self.assertIsInstance(prediction, str)

    # Add more tests for models.py if needed
