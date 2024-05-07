import pandas as pd
import webbrowser
from abc import ABC, abstractmethod

# Abstract base class for reporting strategies
class DataReportingStrategy(ABC):
    @abstractmethod
    def generate_report(self, data):
        pass

# Concrete class for generating text reports
class TextReportStrategy(DataReportingStrategy):
    def generate_report(self, data):
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        report = f"Text Report:\n{data.to_string()}"
        print(report)
        return report

# Concrete class for generating CSV reports
class CSVReportStrategy(DataReportingStrategy):
    def generate_report(self, data):
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        data.to_csv('report.csv', index=False)
        print("CSV report generated.")
        return 'report.csv'

# Concrete class for generating HTML reports
class HTMLReportStrategy(DataReportingStrategy):
    def generate_report(self, data):
        # Check if data is a dictionary of DataFrames
        if isinstance(data, dict):
            for key, df in data.items():
                if isinstance(df, pd.DataFrame):
                    html_content = df.to_html()
                    filename = f"{key}_report.html"
                    with open(filename, 'w') as f:
                        f.write(html_content)
                    webbrowser.open(filename, new=2)
                    print(f"{key.capitalize()} report generated successfully.")
        else:
            # Fallback for a single DataFrame
            html_content = data.to_html()
            with open('report.html', 'w') as f:
                f.write(html_content)
            webbrowser.open('report.html', new=2)
            print("HTML report generated successfully.")
# Concrete class for direct output
class ReturnReportStrategy(DataReportingStrategy):
    def generate_report(self, data):
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)
        return data.to_dict(orient='records')

# Context class for setting the reporting strategy
class DataReportingContext:
    def __init__(self, strategy: DataReportingStrategy):
        self.strategy = strategy

    def generate_report(self, data):
        return self.strategy.generate_report(data)
