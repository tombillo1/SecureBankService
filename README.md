# SecureBank Fraud Prediction System

This project is a Flask-based web API that receives transaction data and classifies each transaction as either fraudulent or legitimate using simple rule-based logic. The system is containerized using Docker for easy deployment and interaction.

---

## Quick Start (Docker)

Follow these steps to build and run the app using Docker:

### 1. Build the Docker image

Open a terminal in the root `securebank/` directory and run:

docker build -t securebank-app .

### 2. Run the Docker container

docker run -p 5000:5000 securebank-app

The Flask server will now be running on:

http://localhost:5000/predict

---

## Test the API with curl

Create a file named test.json with the following content:

{
    "trans_date_trans_time": "2024-09-15 12:34:56",
    "cc_num": 38859492057661,
    "unix_time": 1694775296,
    "merchant": "fraud_Lind-Buckridge",
    "category": "entertainment",
    "amt": 50.75,
    "merch_lat": 43.150704,
    "merch_long": -112.154481
}

Then run the following command from your terminal to test the API:

curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d @test.json

Expected output (if amt < 1000):

{"prediction":"legitimate"}

---

## Dependencies

This project uses only the approved packages:

- Flask
- Pandas
- NumPy
- scikit-learn

These are automatically installed when you build the Docker image.
