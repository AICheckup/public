import joblib  # For saving and loading the model
from sklearn.linear_model import LogisticRegression  # Example model
from sklearn.feature_extraction.text import TfidfVectorizer  # Example feature extraction
from sklearn.pipeline import Pipeline  # Example pipeline

class DiagnosisModel:
    """
    A class representing the machine learning model for diagnosis prediction.
    """

    def __init__(self, model_path=None):
        """
        Initializes the DiagnosisModel.

        Args:
            model_path (str, optional): Path to a pre-trained model file. 
                                         If None, a new model will be trained. Defaults to None.
        """
        self.model_path = model_path
        if model_path:
            self.model = self.load_model(model_path)
        else:
            self.model = self.create_model()

    def create_model(self):
        """
        Creates and returns a new diagnosis prediction model.

        Returns:
            Pipeline: A machine learning pipeline for diagnosis prediction.
        """
        # Example pipeline: TF-IDF for text vectorization and Logistic Regression for classification
        model = Pipeline([
            ('tfidf', TfidfVectorizer()),  # Convert text symptoms to numerical vectors
            ('clf', LogisticRegression())  # Train a logistic regression classifier
        ])
        return model

    def train(self, X_train, y_train):
        """
        Trains the diagnosis prediction model.

        Args:
            X_train (list): List of training data (e.g., symptoms as text).
            y_train (list): List of corresponding labels (e.g., diagnoses).
        """
        self.model.fit(X_train, y_train)

    def predict(self, symptoms):
        """
        Predicts the diagnosis based on the input symptoms.

        Args:
            symptoms (str): Input symptoms.

        Returns:
            str: Predicted diagnosis.
        """
        # Assuming the model expects a list of strings as input
        return self.model.predict([symptoms])[0]

    def predict_proba(self, symptoms):
        """
        Predicts the probabilities of each possible diagnosis.

        Args:
            symptoms (str): Input symptoms.

        Returns:
            dict: A dictionary where keys are diagnoses and values are their probabilities.
        """
        # Assuming the model returns probabilities for each class
        probabilities = self.model.predict_proba([symptoms])[0]
        classes = self.model.classes_  # Get the class labels from the model
        return dict(zip(classes, probabilities))

    def save_model(self, model_path):
        """
        Saves the trained model to a file.

        Args:
            model_path (str): Path to save the model.
        """
        joblib.dump(self.model, model_path)

    def load_model(self, model_path):
        """
        Loads a pre-trained model from a file.

        Args:
            model_path (str): Path to the pre-trained model file.

        Returns:
            Pipeline: The loaded model.
        """
        return joblib.load(model_path)

# Example usage (you can add this to a separate script or within a conditional block)
# if __name__ == "__main__":
#     # Create and train a new model (replace with your actual training data)
#     model = DiagnosisModel()
#     X_train = ["headache fever", "cough sore throat", "stomach pain nausea"]
#     y_train = ["migraine", "cold", "gastritis"]
#     model.train(X_train, y_train)

#     # Save the model
#     model.save_model("diagnosis_model.joblib")

#     # Load the saved model
#     loaded_model = DiagnosisModel(model_path="diagnosis_model.joblib")

#     # Predict using the loaded model
#     prediction = loaded_model.predict("headache")
#     print(f"Prediction: {prediction}")

#     # Predict probabilities using the loaded model
#     probabilities = loaded_model.predict_proba("headache")
#     print(f"Probabilities: {probabilities}")
