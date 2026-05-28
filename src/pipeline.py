import pandas as pd
import numpy as np
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RetailDataPipeline:
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        self.sales_df = pd.DataFrame()
        self.product_df = pd.DataFrame()
        self.promo_df = pd.DataFrame()

    def extract(self) -> None:
        logger.info("Extracting data from CSV sources...")
        try:
            self.sales_df = pd.read_csv(self.data_dir / 'sales_transaction.csv')
            self.product_df = pd.read_csv(self.data_dir / 'product_master.csv')
            self.promo_df = pd.read_csv(self.data_dir / 'promotion_master.csv')
            
            self.sales_df['datetime'] = pd.to_datetime(self.sales_df['datetime'])
            self.promo_df['start_date'] = pd.to_datetime(self.promo_df['start_date'])
            self.promo_df['end_date'] = pd.to_datetime(self.promo_df['end_date'])
        except FileNotFoundError as e:
            logger.error(f"Missing required data file: {e}")
            raise

    def transform(self) -> pd.DataFrame:
        logger.info("Starting data transformation and feature engineering...")
        
        df = self.sales_df.merge(
            self.product_df[['product_id', 'price']], 
            on='product_id', 
            how='left'
        )
        
        df['year'] = df['datetime'].dt.year
        df['month'] = df['datetime'].dt.month
        df['day_of_week'] = df['datetime'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Aggregate to daily level to resolve multiple transactions per day
        daily_sales = df.groupby(['datetime', 'store_id', 'product_id']).agg(
            total_qty=('qty', 'sum'),
            avg_price=('price', 'mean'),
            is_weekend=('is_weekend', 'max'),
            month=('month', 'max')
        ).reset_index()

        daily_sales = daily_sales.sort_values(['store_id', 'product_id', 'datetime'])
        
        logger.info("Calculating time-series features (Lags, Rolling Means)...")
        grouped = daily_sales.groupby(['store_id', 'product_id'])
        
        # Time-series specific features
        daily_sales['lag_1d'] = grouped['total_qty'].shift(1)
        daily_sales['lag_7d'] = grouped['total_qty'].shift(7)
        daily_sales['rolling_7d_mean'] = grouped['total_qty'].transform(
            lambda x: x.shift(1).rolling(7, min_periods=1).mean()
        )
        daily_sales['rolling_30d_mean'] = grouped['total_qty'].transform(
            lambda x: x.shift(1).rolling(30, min_periods=1).mean()
        )
        
        clean_df = daily_sales.dropna().reset_index(drop=True)
        logger.info(f"Transformation complete. Final shape: {clean_df.shape}")
        
        return clean_df