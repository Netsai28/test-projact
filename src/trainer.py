import xgboost as xgb
import joblib
import logging
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from pathlib import Path

logger = logging.getLogger(__name__)

class DemandForecaster:
    def __init__(self, model_dir: str = "artifacts"):
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        self.model_path = self.model_dir / "xgboost_forecaster.joblib"
        
        self.model = xgb.XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1
        )
        
        self.features = [
            'avg_price', 'is_weekend', 'month', 
            'lag_1d', 'lag_7d', 'rolling_7d_mean', 'rolling_30d_mean'
        ]
        self.target = 'total_qty'

    def train_evaluate(self, df: pd.DataFrame):
        logger.info("Initializing Time-Series Split...")
        
        # Must sort by time for valid time-series validation
        df = df.sort_values('datetime')
        X = df[self.features]
        y = df[self.target]
        
        # 80/20 Time-based holdout
        split_idx = int(len(df) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
        
        logger.info(f"Training XGBoost on {len(X_train)} samples...")
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        
        preds = self.model.predict(X_test)
        
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        
        # MAPE is crucial for business (Percentage Error)
        mape = np.mean(np.abs((y_test - preds) / (y_test + 1))) * 100 
        
        logger.info("--- Model Performance Metrics ---")
        logger.info(f"MAE:  {mae:.2f} units")
        logger.info(f"RMSE: {rmse:.2f} units")
        logger.info(f"MAPE: {mape:.2f}% error")
        
        return mae, rmse, mape
        
    def save(self):
        joblib.dump(self.model, self.model_path)
        logger.info(f"Model artifact saved to {self.model_path}")
        
    def load(self):
        self.model = joblib.load(self.model_path)
        logger.info("Model loaded successfully from artifact.")