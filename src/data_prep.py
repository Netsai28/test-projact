import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data(n_days=365):
    dates = [datetime(2023, 1, 1) + timedelta(days=i) for i in range(n_days)]
    products = ['P001', 'P002', 'P003']
    stores = ['S01', 'S02']
    data = []
    
    for date in dates:
        for p_id in products:
            for s_id in stores:
                is_weekend = 1 if date.weekday() >= 5 else 0
                promotion = 1 if (date.day % 10 == 0) else 0
                base_sales = np.random.randint(10, 50)
                qty = base_sales + (is_weekend * 15) + (promotion * 20)
                
                data.append({
                    'datetime': date,
                    'product_id': p_id,
                    'store_id': s_id,
                    'price': 100 if p_id == 'P001' else 200,
                    'qty': qty,
                    'promotion_id': 'PROMO_10' if promotion else None
                })
                
    return pd.DataFrame(data)

def prep_features(df):
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['month'] = df['datetime'].dt.month
    df['is_promo'] = df['promotion_id'].notnull().astype(int)
    
    df = df.sort_values(['product_id', 'store_id', 'datetime'])
    df['sales_lag_7'] = df.groupby(['product_id', 'store_id'])['qty'].shift(7)
    df['rolling_mean_30'] = df.groupby(['product_id', 'store_id'])['qty'].transform(lambda x: x.shift(1).rolling(30).mean())
    
    return df.dropna()