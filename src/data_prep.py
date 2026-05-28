import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_mock_data(n_days=180):
    np.random.seed(42)
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_days)]
    product_ids = [f'P{str(i).zfill(3)}' for i in range(1, 11)]
    store_ids = ['S01', 'S02', 'S03']
    
    df_product = pd.DataFrame({
        'product_id': product_ids,
        'price': np.random.choice([50, 100, 150, 200, 500], len(product_ids)),
        'product_taxonomies': np.random.choice(['Food', 'Beverage', 'Electronics'], len(product_ids))
    })
    
    df_promo = pd.DataFrame({
        'promotion_id': ['PROMO_01', 'PROMO_02'],
        'discount': [0.10, 0.20],
        'product_id': ['P001', 'P005'],
        'start_date': [datetime(2023, 3, 1), datetime(2023, 5, 1)],
        'end_date': [datetime(2023, 3, 15), datetime(2023, 5, 15)]
    })

    sales_data = []
    for d in dates:
        for p in product_ids:
            for s in store_ids:
                is_weekend = 1 if d.weekday() >= 5 else 0
                is_holiday = np.random.choice([0, 1], p=[0.95, 0.05])
                
                base_qty = np.random.randint(5, 20)
                qty = base_qty + (is_weekend * 5) + (is_holiday * 15)
                
                sales_data.append({
                    'datetime': d,
                    'product_id': p,
                    'store_id': s,
                    'qty': qty,
                    'customer_id': f'C{np.random.randint(1000, 9999)}',
                    'promotion_id': np.random.choice([None, 'PROMO_01', 'PROMO_02'], p=[0.8, 0.1, 0.1]),
                    'po_id': f'PO{np.random.randint(100, 999)}',
                    'is_holiday_flag': is_holiday
                })
                
    df_sales = pd.DataFrame(sales_data)
    return df_sales, df_product, df_promo

def process_features(df_sales, df_product, df_promo):
    df_merged = df_sales.merge(df_product, on='product_id', how='left')
    df_merged = df_merged.merge(df_promo, on=['promotion_id', 'product_id'], how='left')
    
    df_merged['discount'] = df_merged['discount'].fillna(0)
    df_merged['final_price'] = df_merged['price'] * (1 - df_merged['discount'])
    
    df_merged['year'] = df_merged['datetime'].dt.year
    df_merged['month'] = df_merged['datetime'].dt.month
    df_merged['dayofweek'] = df_merged['datetime'].dt.dayofweek
    
    df_merged = pd.get_dummies(df_merged, columns=['product_taxonomies'], drop_first=True)
    
    df_merged = df_merged.sort_values(by=['store_id', 'product_id', 'datetime'])
    df_merged['lag_1_qty'] = df_merged.groupby(['store_id', 'product_id'])['qty'].shift(1)
    df_merged['lag_7_qty'] = df_merged.groupby(['store_id', 'product_id'])['qty'].shift(7)
    
    df_merged = df_merged.dropna()
    return df_merged