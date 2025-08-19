import sys
import json
import pandas as pd
import pickle
import os

def predict():
    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        data = json.loads(input_data)

        # Create DataFrame
        new_data = pd.DataFrame({
            'age': [int(data['age'])],
            'sex': [data['sex']],
            'bmi': [float(data['bmi'])],
            'children': [int(data['children'])],
            'smoker': [data['smoker']],
            'region': [data['region']]
        })

        # Preprocess
        new_data['smoker'] = new_data['smoker'].str.lower().map({'yes': 1, 'no': 0})
        new_data = new_data.drop(['sex', 'region'], axis=1)

        # Load model and predict
        model_path = os.path.join(os.path.dirname(__file__), "insurancemodelf.pkl")
        with open(model_path, "rb") as file:
            model = pickle.load(file)

        prediction = float(model.predict(new_data)[0])

        # Return result
        print(json.dumps({'predicted_price': prediction}))
        sys.stdout.flush()

    except Exception as e:
        print(json.dumps({'error': str(e)}))
        sys.stdout.flush()
        sys.exit(1)

if __name__ == '__main__':
    predict()
