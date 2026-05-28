import pandas as pd
import numpy as np
import os

os.makedirs('data', exist_ok=True)
np.random.seed(42)

dates = pd.date_range('2023-01-01', '2023-12-31')

prod_df = pd.DataFrame({
    'product_id': [f'P{str(i).zfill(3)}' for i in range(1, 51)],
    'product_taxonomies': np.random.choice(['Food', 'Beverage', 'Electronics', 'Apparel', 'Beauty'], 50),
    'price': np.random.uniform(50, 2000, 50).round(2),
})
prod_df['cost_price'] = (prod_df['price'] * np.random.uniform(0.4, 0.7, 50)).round(2)

store_df = pd.DataFrame({
    'store_id': [f'S{str(i).zfill(2)}' for i in range(1, 6)],
    'store_taxonomies': ['Flagship', 'Mall', 'Street', 'Mall', 'Street'],
    'region': ['Central', 'North', 'South', 'Central', 'East']
})

cust_df = pd.DataFrame({
    'customer_id': [f'C{str(i).zfill(4)}' for i in range(1, 1001)],
    'age_group': np.random.choice(['Gen Z', 'Millennials', 'Gen X', 'Boomers'], 1000, p=[0.2, 0.4, 0.3, 0.1]),
    'customer_segment': np.random.choice(['VIP', 'Regular', 'Occasional', 'New'], 1000, p=[0.1, 0.4, 0.3, 0.2]),
    'gender': np.random.choice(['M', 'F', 'Other'], 1000, p=[0.45, 0.5, 0.05])
})

promo_df = pd.DataFrame({
    'promotion_id': ['PROMO_NY', 'PROMO_SUMMER', 'PROMO_PAYDAY', 'PROMO_11_11'],
    'discount': [0.15, 0.10, 0.05, 0.20],
    'product_id': np.random.choice(prod_df['product_id'], 4, replace=False),
    'start_date': pd.to_datetime(['2023-01-01', '2023-04-01', '2023-08-25', '2023-11-10']),
    'end_date': pd.to_datetime(['2023-01-15', '2023-04-15', '2023-08-31', '2023-11-15'])
})

n_rows = 50000
sales_data = []

rand_dates = np.random.choice(dates, n_rows)
rand_prods = np.random.choice(prod_df['product_id'], n_rows)
rand_stores = np.random.choice(store_df['store_id'], n_rows)
rand_custs = np.random.choice(cust_df['customer_id'], n_rows)

for i in range(n_rows):
    d = rand_dates[i]
    p = rand_prods[i]
    
    qty = np.random.randint(1, 5)
    if pd.Timestamp(d).weekday() >= 5:
        qty = int(qty * 1.5)
        
    mask = (promo_df['product_id'] == p) & (promo_df['start_date'] <= d) & (promo_df['end_date'] >= d)
    promo_match = promo_df[mask]
    
    promo_id = promo_match['promotion_id'].iloc[0] if not promo_match.empty else None
    if promo_id:
        qty += np.random.randint(1, 3)
        
    sales_data.append({
        'datetime': d,
        'product_id': p,
        'store_id': rand_stores[i],
        'customer_id': rand_custs[i],
        'qty': qty,
        'promotion_id': promo_id
    })

sales_df = pd.DataFrame(sales_data)
sales_df = sales_df.merge(prod_df[['product_id', 'price']], on='product_id', how='left')
sales_df = sales_df.sort_values('datetime').reset_index(drop=True)

prod_df.to_csv('data/product_master.csv', index=False)
store_df.to_csv('data/store_master.csv', index=False)
cust_df.to_csv('data/customer_master.csv', index=False)
promo_df.to_csv('data/promotion_master.csv', index=False)
sales_df.to_csv('data/sales_transaction.csv', index=False)

print("exported data successfully")