import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

def train_and_evaluate(df):
    features = ['final_price', 'discount', 'month', 'dayofweek', 'is_holiday_flag', 
                'lag_1_qty', 'lag_7_qty'] + [col for col in df.columns if 'product_taxonomies_' in col]
    
    X = df[features]
    y = df['qty']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)
    
    model = xgb.XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    # แก้ไขการคำนวณ RMSE ตรงบรรทัดนี้
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    
    return model, mae, rmse