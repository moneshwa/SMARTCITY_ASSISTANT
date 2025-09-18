import pandas as pd
from io import StringIO
from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from sklearn.linear_model import LinearRegression

router = APIRouter()

@router.post("/forecast", tags=["Data Analysis"])
async def forecast_kpi(file: UploadFile = File(...), kpi_column: str = Query(...)):
    """
    Accepts a CSV, a KPI column name, and forecasts the next year's value.
    Assumes the CSV has a 'year' column.
    """
    try:
        contents = await file.read()
        csv_data = StringIO(contents.decode("utf-8"))
        df = pd.read_csv(csv_data)

        if 'year' not in df.columns or kpi_column not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'year' and the specified KPI column.")

        model = LinearRegression()
        model.fit(df[['year']], df[[kpi_column]])
        
        next_year = df['year'].max() + 1
        prediction = model.predict([[next_year]])
        
        return {
            "predicted_year": int(next_year),
            "kpi": kpi_column,
            "predicted_value": round(prediction[0][0], 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/anomalies", tags=["Data Analysis"])
async def detect_anomalies(
    file: UploadFile = File(...), 
    kpi_column: str = Query(...), 
    threshold: float = Query(...)
):
    """
    Accepts a CSV, a KPI column, and a threshold to find anomalies.
    """
    try:
        contents = await file.read()
        csv_data = StringIO(contents.decode("utf-8"))
        df = pd.read_csv(csv_data)

        if kpi_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"CSV does not contain the column '{kpi_column}'.")

        anomalies = df[df[kpi_column] > threshold]
        
        return {
            "kpi": kpi_column,
            "threshold": threshold,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies.to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
