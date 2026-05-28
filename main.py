from src.data_prep import create_mock_data, process_features
from src.model import train_and_evaluate

def run_pipeline():
    df_sales, df_product, df_promo = create_mock_data()
    
    df_processed = process_features(df_sales, df_product, df_promo)
    
    model, mae, rmse = train_and_evaluate(df_processed)
    
    print("=== Model Training Metrics ===")
    print(f"MAE: {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")

if __name__ == "__main__":
    run_pipeline()