import json
import csv
import pandas as pd
from abc import ABC, abstractmethod

# Abstract base class for data ingestion strategies
class DataIngestionStrategy(ABC):
    @abstractmethod
    def ingest_data(self, file_path):
        pass

# Concrete class for JSON data ingestion
class JSONDataIngestion(DataIngestionStrategy):
    def ingest_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

# Concrete class for CSV data ingestion
class CSVDataIngestion(DataIngestionStrategy):
    def ingest_data(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
        return data

# Concrete class for Excel data ingestion
class ExcelDataIngestion(DataIngestionStrategy):
    def ingest_data(self, file_path):
        # Using pandas to read Excel files
        data = pd.read_excel(file_path, engine='openpyxl')
        return data.to_dict(orient='records')

# Context class for setting the data ingestion strategy
class DataIngestionContext:
    def __init__(self, strategy: DataIngestionStrategy):
        self.strategy = strategy

    def ingest_data(self, file_path):
        return self.strategy.ingest_data(file_path)
