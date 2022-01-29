from joblib import load
from pathlib import Path

class Recommender:
    def __init__(self):
        pass


    def load_model(self):
        current_dir = Path(__file__).parent

        self.model = load(f'{current_dir}/GBR100.joblib')


    def predict(self, df):
        predictions = self.model.predict(df)

        return predictions


recommender = Recommender()
