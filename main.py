from src.data_prep import generate_data, prep_features
from src.model import train_xgboost

def main():
    df_raw = generate_data()
    df_clean = prep_features(df_raw)
    
    model, mae = train_xgboost(df_clean)
    
    print(f"Model Training Completed")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")

if __name__ == "__main__":
    main()