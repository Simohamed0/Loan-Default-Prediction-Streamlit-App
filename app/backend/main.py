import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import pandas as pd
import joblib

# Initialize the FastAPI app
app = FastAPI()

# Load the trained model
model = joblib.load('loan_default_model.pkl')

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
        logging.info("Converted data to DataFrame: %s", input_df.head())

        # Ensure the correct format of the data (e.g., check for expected columns)
        required_columns = ['loan_amnt', 'installment', 'annual_inc', 'dti', 'fico_range_low', 'fico_range_high']
        if not all(col in input_df.columns for col in required_columns):
            logging.error("Missing required columns")
            raise HTTPException(status_code=400, detail=f"JSON data must contain columns: {', '.join(required_columns)}")

        # Make predictions
        predictions = model.predict(input_df)
        logging.info("Generated predictions: %s", predictions)

        # Add predictions to the DataFrame
        input_df['predictions'] = predictions

        # Convert the DataFrame to JSON
        predictions_json = input_df.to_dict(orient='records')
        logging.info("Returning predictions: %s", predictions_json)
        
        return JSONResponse(content={"predictions": predictions_json})

    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))
