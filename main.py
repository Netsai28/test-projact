from src.pipeline import RetailDataPipeline
from src.trainer import DemandForecaster
import logging

def main():
    # 1. ETL Pipeline
    pipeline = RetailDataPipeline(data_dir="data")
    pipeline.extract()
    processed_data = pipeline.transform()
    
    # 2. Model Training & Evaluation
    forecaster = DemandForecaster()
    forecaster.train_evaluate(processed_data)
    
    # 3. Save Artifact for API usage
    forecaster.save()

if __name__ == "__main__":
    main()