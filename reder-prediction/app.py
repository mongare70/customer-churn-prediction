from fastapi import FastAPI
import pickle
import json
import pandas as pd
from pydantic import BaseModel, Field
from DataCleaning.clean import clean_data
from typing import Any
from typing import List, Dict, Any
import os
import uvicorn


app = FastAPI(title="Reder Prediction API", version="1.0")


class PredictionRequest(BaseModel):
    records: List[Dict[str, Any]] = Field(
        ...,
        example=[
            {
                "CustomerID": 1001,
                "Name": "Hillary Mongare",
                "Age": 31,
                "Gender": "Male",
                "Location": "United Kingdom",
                "Email": "john.doe@example.com",
                "Phone": "000000000000",
                "Address": "123 Main St, City, Country",
                "Segment": "Segment B",
                "NPS": "3",
                "Timestamp": "2020-01-27 01:36:49",
                "ProductList": "Product A, Product B",
                "TotalPurchaseFrequency": 38,
                "TotalPurchaseValue": 3339.72,
                "ProductList": "Frozen Cocktail Mixes|Guacamole|Hockey Stick Care|Invitations|Mortisers|Printer, Copier & Fax Machine Accessories|Rulers",
                "Plan": "Express",
                "Start_Date": "2023-01-01",
                "End_Date": "2023-01-02",
                "TotalInteractionType": "Call|Chat|Email",
                "numEmails": 1,
                "numCalls": 1,
                "numChats": 2,
                "FirstInteractionDate": "2023-01-01",
                "LastInteractionDate": "2023-01-02",
                "AVGLatePayment": 13.34,
                "NumPaymentMethods": 3,
                "PageViews": 49,
                "Timespent (minutes)": 15,
                "ActionCount": 24,
                "unique_pages": 13,
                "most_recent_action_date": "2022-11-07 02:24:31",
                "Logins": 19,
                "Frequency": "Weekly",
                "Rating": 1,
                "Comment": "",
                "AVGOpenDays": 818.0,
                "AVGClickDays": 319.0,
            }
        ],
    )


def load_assets():
    model_path = os.path.join("model", "model.pkl")
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    schema_path = os.path.join("model", "schema.json")
    with open(schema_path, "r") as f:
        schema = json.load(f)
        feature_schema = schema["model_schema"]
    return model, feature_schema


@app.post("/churn-predict")
def predict(request: PredictionRequest):
    data = pd.DataFrame(request.records)

    data = clean_data(data)

    model, feature_schema = load_assets()

    data = data.reindex(columns=feature_schema, fill_value=0)

    predictions = model.predict(data)

    return {"predictions": predictions.tolist()}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
