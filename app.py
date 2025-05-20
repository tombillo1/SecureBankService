from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy model
class Model:
    @staticmethod
    def predict(input_data):
        """
        Simple rule: predict fraud if amount > 1000
        """
        amt = float(input_data.get("amt", 0))
        is_fraud = amt > 1000
        return {"prediction": "fraudulent" if is_fraud else "legitimate"}

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.get_json()

    expected_keys = [
        'trans_date_trans_time', 'cc_num', 'unix_time',
        'merchant', 'category', 'amt', 'merch_lat', 'merch_long'
    ]
    missing_keys = [k for k in expected_keys if k not in input_data]
    if missing_keys:
        return jsonify({"error": f"Missing fields: {missing_keys}"}), 400

    result = Model.predict(input_data)
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
