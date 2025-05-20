import logging
import requests
from requests.exceptions import RequestException
from .base_fetch_data import BaseFetchDataUseCase

class FetchODataDataUseCase(BaseFetchDataUseCase):
    def __init__(self, *args, **kwargs):
        print("[FetchODataDataUseCase.__init__] Initializing FetchODataDataUseCase")
        super().__init__(*args, **kwargs)

    def execute(self, endpoint: str = None):  # Default endpoint removed to avoid duplication
        print(f"[FetchODataDataUseCase.execute] Called with endpoint={endpoint}")
        response = self.api_client.fetch_data(endpoint) if endpoint else self.api_client.fetch_data()
        print(f"[FetchODataDataUseCase.execute] Response object: {response}")
        try:
            data = response.json()
            print(f"[FetchODataDataUseCase.execute] Response JSON: {data}")
        except Exception as e:
            print(f"[FetchODataDataUseCase.execute] Could not decode JSON: {e}")
            data = None
        processed_data = self.process_data(data)
        print(f"[FetchODataDataUseCase.execute] Processed data: {processed_data}")
        # Save only the 'value' part of the response data to avoid encoding issues
        self.save_to_duckdb(processed_data['value'])
        return processed_data

    def process_data(self, data):
        print(f"[FetchODataDataUseCase.process_data] Called with data: {data}")
        import polars as pl
        # Convert the data to a Polars DataFrame
        df = pl.DataFrame(data, strict=False)
        print(f"[FetchODataDataUseCase.process_data] Polars DataFrame: {df}")
        # Perform any necessary processing on the DataFrame
        return df

    def save_to_duckdb(self, df):
        print(f"[FetchODataDataUseCase.save_to_duckdb] Called with df: {df}")
        import duckdb
        # Save the DataFrame to DuckDB in Parquet format
        try:
            # add read_only=False   to allow writing to the database
            conn = duckdb.connect('backend/data/duckdb.db', read_only=False)
            conn.execute("CREATE TABLE IF NOT EXISTS odata_data AS SELECT * FROM df")
            conn.close()
            print("[FetchODataDataUseCase.save_to_duckdb] Data saved to DuckDB")
            # Process the data as needed
            return df
        except Exception as e:
            print(f"[FetchODataDataUseCase.save_to_duckdb] Error saving to DuckDB: {e}")
            logging.error(f"Error saving to DuckDB: {e}")
            raise
