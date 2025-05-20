import pandas as pd
import numpy as np
import os

class RawDataHandler:
    """
    Handles extraction, transformation, and description of raw data for machine learning preprocessing.
    """

    def __init__(self, storage_path, save_path):
        self.storage_path = storage_path
        self.save_path = save_path

    def extract(self, customer_information_filename, transaction_filename, fraud_information_filename):
        customer_path = os.path.join(self.storage_path, customer_information_filename)
        transaction_path = os.path.join(self.storage_path, transaction_filename)
        fraud_path = os.path.join(self.storage_path, fraud_information_filename)

        customer_df = pd.read_csv(customer_path)
        transaction_df = pd.read_parquet(transaction_path)

        fraud_series = pd.read_json(fraud_path, typ='series')
        fraud_series.index = range(len(fraud_series))

        return customer_df, transaction_df, fraud_series

    def convert_dates(self, df):
        if 'trans_date_trans_time' not in df.columns:
            return df

        dt = pd.to_datetime(df['trans_date_trans_time'])
        df['day_of_week'] = dt.dt.day_name()
        df['hour'] = dt.dt.hour
        df['minute'] = dt.dt.minute
        df['seconds'] = dt.dt.second
        df['day_date'] = dt.dt.day
        df['month_date'] = dt.dt.month_name()
        df['year_date'] = dt.dt.year

        return df.drop(columns=['trans_date_trans_time'])

    def transform(self, customer_information, transaction_information, fraud_information):
        df = transaction_information.reset_index(drop=True)
        fraud_information = fraud_information.reset_index(drop=True)
        df['is_fraud'] = fraud_information

        merged = df.merge(customer_information, on='cc_num', how='left')
        cleaned = merged.drop_duplicates().dropna()

        return cleaned

    def describe(self, raw_data):
        return {
            "number_of_records": int(raw_data.shape[0]),
            "number_of_columns": int(raw_data.shape[1]),
            "feature_names": list(raw_data.columns),
            "number_missing_values": int(raw_data.isnull().sum().sum()),
            "column_data_types": [str(dtype) for dtype in raw_data.dtypes]
        }

if __name__ == '__main__':
    handler = RawDataHandler(storage_path="data_sources", save_path="output")

    # Extract raw data
    customer_info, transaction_info, fraud_info = handler.extract(
        "customer_release.csv", "transactions_release.parquet", "fraud_release.json"
    )

    # Transform the data
    cleaned_data = handler.transform(customer_info, transaction_info, fraud_info)
    cleaned_data = handler.convert_dates(cleaned_data)

    # Describe the cleaned data
    description = handler.describe(cleaned_data)
    print(description)

