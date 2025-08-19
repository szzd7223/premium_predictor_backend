# predict.py
import sys
import json
import pandas as pd
import pickle

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
        new_data['smoker'] = new_data['smoker'].map({'yes': 1, 'no': 0})
        new_data = new_data.drop(['sex', 'region'], axis=1)
        
        # Load model and predict
        with open('insurancemodelf.pkl', 'rb') as file:
            model = pickle.load(file)
        
        prediction = float(model.predict(new_data)[0])
        
        # Return result
        print(json.dumps({
            'predicted_price': prediction
        }))
        sys.stdout.flush()
        
        
    except Exception as e:
        print(json.dumps({
            'error': str(e)
        }), file=sys.stderr)
        sys.stderr.flush()
        sys.exit(1)
        

if __name__ == '__main__':
    predict()