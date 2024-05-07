import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.express as px  # Import Plotly Express
from dash.dependencies import Input, Output, State

# Load your dataset
data = pd.read_csv('dataset/PurchasePricesData.csv')

app = dash.Dash(__name__)

# Check if the DataFrame is empty or not
initial_column = data.columns[0] if not data.empty else None

# Convert necessary columns to numeric, handling errors
for col in ['PurchasePrice', 'SellingPrice']:
    if col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

# Creating the plots with Plotly Express
volume_counts = data['Volume'].value_counts().reset_index()
volume_counts.columns = ['Volume', 'Count']  # Rename columns for clarity
fig_volume = px.bar(volume_counts, x='Volume', y='Count', title="Volume Analysis")
fig_price_vs_purchase = px.scatter(data, x='Price', y='PurchasePrice', title="Price vs. Purchase Price")

classification_counts = data['Classification'].value_counts().reset_index()
classification_counts.columns = ['Classification', 'Count']  # Renaming the columns for clarity
fig_classification = px.bar(classification_counts, x='Classification', y='Count', labels={'Classification': 'Classification', 'Count': 'Count'}, title="Classification Analysis")

vendor_counts = data['VendorName'].value_counts().reset_index()
vendor_counts.columns = ['Vendor Name', 'Count']  # Explicitly renaming the columns
fig_vendor = px.bar(vendor_counts, x='Vendor Name', y='Count', labels={'Vendor Name': 'Vendor Name', 'Count': 'Count'}, title="Vendor Analysis")

numeric_columns = [col for col in data.columns if data[col].dtype in ['float64', 'int64']]

app.layout = html.Div([
    # DataTable with filtering, sorting, and pagination
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        page_size=10,
        page_action='native',
        filter_action='native',
        sort_action='native',
        style_table={'height': '300px', 'overflowY': 'auto'}
    ),

    # Checklist for selecting columns to plot
    html.Label('Select columns to plot:'),
    dcc.Checklist(
        id='column-selector',
        options=[{'label': col, 'value': col} for col in numeric_columns],
        value=numeric_columns,  # Pre-select all numeric columns initially
        inline=True
    ),


    # Dropdown for selecting which column to plot
    dcc.Dropdown(
        id='column-dropdown',
        options=[{'label': i, 'value': i} for i in data.columns if data[i].dtype in ['float64', 'int64']],
        value=initial_column
    ),

    dcc.Graph(id='dynamic-chart'),

    # Plots section
    dcc.Graph(figure=fig_volume),
    dcc.Graph(figure=fig_price_vs_purchase),
    dcc.Graph(figure=fig_classification),
    dcc.Graph(figure=fig_vendor),
])

@app.callback(
    Output('data-table', 'columns'),
    [Input('column-selector', 'value')]
)

def update_columns(selected_columns):
    return [{"name": i, "id": i} for i in selected_columns]


@app.callback(
    Output('dynamic-chart', 'figure'),
    [Input('table', 'derived_virtual_data'),
     Input('table', 'derived_virtual_selected_rows'),
     Input('column-selector', 'value')]
)


def update_chart(rows, selected_rows, selected_columns):
    # If there's no data or no columns selected, return an empty figure
    if not rows or not selected_columns:
        return {'data': [], 'layout': {'title': 'Dynamically Generated Chart'}}

    # Convert the table's data into a DataFrame
    df = pd.DataFrame(rows)

    # If row selection is used, filter the data
    if selected_rows:
        df = df.iloc[selected_rows]

    # Prepare the data for the chart
    data = []
    for column in selected_columns:
        # Only plot columns that are numeric
        if df[column].dtype in ['float64', 'int64']:
            data.append({
                'x': df.index,
                'y': df[column],
                'type': 'line',  # or 'scatter', 'bar', etc.
                'name': column
            })

    # Return the figure object
    return {
        'data': data,
        'layout': {'title': 'Dynamically Generated Chart'}
    }


if __name__ == '__main__':
    app.run_server(debug=True)
