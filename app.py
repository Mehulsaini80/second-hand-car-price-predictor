from flask import Flask, request, jsonify, render_template
import pickle
import os

app = Flask(__name__)

# Load model and encoders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'rf_model.pkl')
encoder_path = os.path.join(BASE_DIR, 'le_dict.pkl')

with open(model_path, 'rb') as f:
    rf = pickle.load(f)

with open(encoder_path, 'rb') as f: 
    le_dict = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        brand = le_dict['Brand'].transform([data['brand']])[0]
        transmission = le_dict['Transmission'].transform([data['transmission']])[0]
        fuel_type = le_dict['Fuel Type'].transform([data['fuel_type']])[0]
        owner = le_dict['Owner'].transform([data['owner']])[0]

        # Define column order (same as training X.columns)
        columns = ['Brand', 'Model Name', 'Model Variant', 'Car Type', 'Transmission',
                   'Fuel Type', 'Owner', 'State', 'Accidental', 'Kilometers Driven', 'Year']

        input_data = []
        for col in columns:
            if col == 'Brand':
                input_data.append(brand)
            elif col == 'Transmission':
                input_data.append(transmission)
            elif col == 'Fuel Type':
                input_data.append(fuel_type)
            elif col == 'Owner':
                input_data.append(owner)
            elif col == 'Kilometers Driven':
                input_data.append(data['km_driven'])
            elif col == 'Year':
                input_data.append(data['year'])
            else:
                input_data.append(0)

        predicted_price = rf.predict([input_data])[0]
        return jsonify({'predicted_price': round(predicted_price, 2)})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
