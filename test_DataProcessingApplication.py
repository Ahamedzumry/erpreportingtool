import pytest
import pandas as pd
import matplotlib.pyplot as plt
from DataProcessingApplication import VolumeAnalysis, PriceVsPurchasePrice, ClassificationAnalysis, VendorAnalysis, create_dashboard

# Create a sample DataFrame to use in tests
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Volume': ['low', 'medium', 'high', 'medium', 'low'],
        'Price': [10, 20, 30, 40, 50],
        'PurchasePrice': [8, 16, 24, 32, 40],
        'Classification': ['A', 'B', 'A', 'C', 'B'],
        'VendorName': ['Vendor1', 'Vendor2', 'Vendor1', 'Vendor3', 'Vendor2']
    })

def test_volume_analysis_plot(sample_data):
    fig, ax = plt.subplots()
    VolumeAnalysis.plot(sample_data, ax)
    assert len(ax.patches) > 0, "Should have some bars plotted for volumes"

def test_price_vs_purchase_price_plot(sample_data):
    fig, ax = plt.subplots()
    PriceVsPurchasePrice.plot(sample_data, ax)
    assert len(ax.collections) == 1, "Should plot scatter points for price comparisons"

def test_classification_analysis_plot(sample_data):
    fig, ax = plt.subplots()
    ClassificationAnalysis.plot(sample_data, ax)
    assert len(ax.patches) > 0, "Should have some bars plotted for classifications"

def test_vendor_analysis_plot(sample_data):
    fig, ax = plt.subplots()
    VendorAnalysis.plot(sample_data, ax)
    assert len(ax.patches) > 0, "Should have some bars plotted for vendors"

def test_create_dashboard_missing_columns():
    data = pd.DataFrame({
        'Volume': ['low', 'medium', 'high'],
        'Classification': ['A', 'B', 'A'],
        'VendorName': ['Vendor1', 'Vendor2', 'Vendor1']
    })  # Missing 'Price' and 'PurchasePrice' columns
    # We don't actually display the plot in tests, so no assertion for show
    create_dashboard(data)  # We're testing for no exceptions here

def test_create_dashboard_full_data(sample_data):
    # Similarly, you would call this just to ensure no exceptions, or check for expected output if possible
    create_dashboard(sample_data)  # We're testing for no exceptions here

