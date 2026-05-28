import xgboost as xgb
from sklearn.metrics import mean_absolute_error

def train_xgboost(df):
    X = df[['day_of_week', 'month', 'is_promo', 'sales_lag_7', 'rolling_mean_30']]
    y = df['qty']
    
    split = int(len(df) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    
    return model, mae