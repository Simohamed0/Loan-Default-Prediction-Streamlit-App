import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import pandas as pd
import joblib
import json

# Initialize the FastAPI app
app = FastAPI()

# Load the trained model
model = joblib.load('models/random_forest_model.joblib')
scaler = joblib.load('models/scaler.joblib')

# Load from a JSON file
with open('feature_names.json', 'r') as f:
    feature_names = json.load(f)


# Configure logging
logging.basicConfig(level=logging.INFO)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the prediction API!"}

@app.post("/predict/")
async def predict(request: Request):
    try:
        # Parse JSON request
        request_data = await request.json()
        data = request_data.get("data", [])
        
        if not data:
            raise HTTPException(status_code=400, detail="No data provided for prediction.")
        
        logging.info("Received request data: %s", data)
        
        # Convert JSON data to DataFrame
        input_df = pd.DataFrame(data)
        ID = input_df['id']
        X = input_df.drop(columns=['loan_status', 'id'])  # Features
        # Debugging: Print the columns before dropping any
        logging.info("Initial DataFrame columns: %s", input_df.columns.tolist())
        
        # Ensure the correct format of the data (e.g., check for expected columns)
        required_columns = feature_names
        missing_columns = [col for col in required_columns if col not in input_df.columns]
        
        if missing_columns:
            logging.error("Missing required columns: %s", missing_columns)
            raise HTTPException(status_code=400, detail=f"JSON data must contain columns: {', '.join(missing_columns)}")

        # Drop any columns that are not in the feature_names
        X = X[feature_names]
        logging.info("DataFrame after ensuring feature columns: %s", X.head())

        # Scale the data
        X = scaler.transform(X)
        # Make predictions
        predictions = model.predict(X)
        logging.info("Generated predictions: %s", predictions)

        # Add predictions to the DataFrame
        result_df = pd.DataFrame()  # Recreate original DataFrame with all columns
        result_df['id'] = ID
        result_df['predictions'] = predictions

        # Convert the DataFrame to JSON
        predictions_json = result_df.to_dict(orient='records')

        logging.info("Returning predictions: %s", predictions_json)
        
        return JSONResponse(content={"predictions": predictions_json})

    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
