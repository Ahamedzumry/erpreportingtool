import pandas as pd
import matplotlib.pyplot as plt

class VolumeAnalysis:
    @staticmethod
    def plot(data, ax):
        data['Volume'].value_counts().plot(kind='bar', ax=ax, title='Volume Analysis')

class PriceVsPurchasePrice:
    @staticmethod
    def plot(data, ax):
        ax.scatter(data['Price'], data['PurchasePrice'])
        ax.set_title('Price vs. Purchase Price')
        ax.set_xlabel('Selling Price')
        ax.set_ylabel('Purchase Price')

class ClassificationAnalysis:
    @staticmethod
    def plot(data, ax):
        data['Classification'].value_counts().plot(kind='bar', ax=ax, title='Classification Analysis')

class VendorAnalysis:
    @staticmethod
    def plot(data, ax):
        data['VendorName'].value_counts().plot(kind='bar', ax=ax, title='Vendor Analysis')


def create_dashboard(data):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # Convert columns to numeric if they exist
    for col in ['PurchasePrice', 'SellingPrice']:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')

    # Initialize the figure and axes for the subplots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))
    plt.subplots_adjust(hspace=0.5, wspace=0.3)


    # Add the main title (heading) for the dashboard
    fig.suptitle('ERP Reporting Tool - Dashboard', fontsize=16)



    # Continue with the existing plots
    VolumeAnalysis.plot(data, axs[0, 0])
    if 'PurchasePrice' in data.columns:
        # Assuming you want to plot PurchasePrice against another column or just visualize it alone
        axs[0, 1].scatter(data['Price'], data['PurchasePrice'])
        axs[0, 1].set_title('Purchase Price vs Buying Price')
        axs[0, 1].set_xlabel('Price')
        axs[0, 1].set_ylabel('Purchase Price')
    else:
        axs[0, 1].text(0.5, 0.5, 'PurchasePrice column missing', ha='center')
    ClassificationAnalysis.plot(data, axs[1, 0])
    VendorAnalysis.plot(data, axs[1, 1])

    plt.tight_layout()
    plt.show()

