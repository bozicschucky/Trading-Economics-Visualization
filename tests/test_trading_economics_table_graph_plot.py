import unittest
from unittest.mock import patch, mock_open
import os
import pandas as pd
from trading_economics_table_graph_plot import load_or_fetch_data
from unittest.mock import patch, MagicMock
from trading_economics_table_graph_plot import plot_core_inflation_comparison
from unittest.mock import patch
from trading_economics_table_graph_plot import plot_stock_market_comparison

class TestTradingEconomicsTableGraphPlot(unittest.TestCase):

  @patch('trading_economics_table_graph_plot.os.path.exists')
  @patch('trading_economics_table_graph_plot.pd.read_csv')
  def test_load_data_from_csv(self, mock_read_csv, mock_path_exists):
    # Mock the os.path.exists to return True
    mock_path_exists.return_value = True
    # Mock the pd.read_csv to return a sample DataFrame
    mock_df = pd.DataFrame({'Country': ['Mexico'], 'Category': ['Core Inflation Rate'], 'q1': [1.0], 'q2': [1.1], 'q3': [1.2], 'q4': [1.3]})
    mock_read_csv.return_value = mock_df

    csv_file = 'dummy.csv'
    df = load_or_fetch_data(csv_file)

    # Check if the read_csv was called with the correct file
    mock_read_csv.assert_called_once_with(csv_file)
    # Check if the returned DataFrame is as expected
    pd.testing.assert_frame_equal(df, mock_df)

  @patch('trading_economics_table_graph_plot.requests.get')
  @patch('trading_economics_table_graph_plot.pd.DataFrame.to_csv')
  @patch('trading_economics_table_graph_plot.os.path.exists')
  @patch('trading_economics_table_graph_plot.os.getenv')
  def test_fetch_data_from_api(self, mock_getenv, mock_path_exists, mock_to_csv, mock_requests_get):
    # Mock the os.path.exists to return False
    mock_path_exists.return_value = False
    # Mock the os.getenv to return a dummy API key
    mock_getenv.return_value = 'dummy_api_key'
    # Mock the requests.get to return a sample JSON response
    mock_response = {
      'Country': ['Mexico'], 'Category': ['Core Inflation Rate'], 'q1': [1.0], 'q2': [1.1], 'q3': [1.2], 'q4': [1.3]
    }
    mock_requests_get.return_value.json.return_value = mock_response
    # Mock the DataFrame.to_csv to do nothing
    mock_to_csv.return_value = None

    csv_file = 'dummy.csv'
    df = load_or_fetch_data(csv_file)

    # Check if the requests.get was called with the correct URL
    mock_requests_get.assert_called_once_with('https://api.tradingeconomics.com/forecast/country/Mexico,New Zealand,Sweden?c=dummy_api_key')
    # Check if the DataFrame.to_csv was called with the correct file
    mock_to_csv.assert_called_once_with(csv_file, index=False)
    # Check if the returned DataFrame is as expected
    expected_df = pd.DataFrame(mock_response)
    pd.testing.assert_frame_equal(df, expected_df)


  # class TestTradingEconomicsInflationTableGraphPlot(unittest.TestCase):

  @patch('trading_economics_table_graph_plot.plt.show')
  @patch('trading_economics_table_graph_plot.plt.figure')
  @patch('trading_economics_table_graph_plot.plt.plot')
  @patch('trading_economics_table_graph_plot.plt.title')
  @patch('trading_economics_table_graph_plot.plt.xlabel')
  @patch('trading_economics_table_graph_plot.plt.ylabel')
  @patch('trading_economics_table_graph_plot.plt.legend')
  @patch('trading_economics_table_graph_plot.plt.tight_layout')
  def test_plot_core_inflation_comparison(self, mock_tight_layout, mock_legend, mock_ylabel, mock_xlabel, mock_title, mock_plot, mock_figure, mock_show):
      # Create a sample DataFrame
      data = {
          'Country': ['Mexico', 'Sweden', 'New Zealand'],
          'Category': ['Core Inflation Rate', 'Core Inflation Rate', 'Core Inflation Rate'],
          'q1': [1.0, 1.1, 1.2],
          'q2': [1.3, 1.4, 1.5],
          'q3': [1.6, 1.7, 1.8],
          'q4': [1.9, 2.0, 2.1]
      }
      df = pd.DataFrame(data)

      # Call the function
      plot_core_inflation_comparison(df)

      # Check if the figure was created
      mock_figure.assert_called_once_with(figsize=(8, 5))
      # Check if the plot function was called for each country
      self.assertEqual(mock_plot.call_count, 3)
      # Check if the title, xlabel, ylabel, legend, and tight_layout were called
      mock_title.assert_called_once_with(
          'Quarterly Core Inflation Rate Comparison: Mexico, Sweden, New Zealand')
      mock_xlabel.assert_called_once_with('Quarter')
      mock_ylabel.assert_called_once_with('Core Inflation Rate (%)')
      mock_legend.assert_called_once()
      mock_tight_layout.assert_called_once()
      # Check if plt.show() was called
      mock_show.assert_called_once()


  @patch('trading_economics_table_graph_plot.plt.show')
  @patch('trading_economics_table_graph_plot.plt.tight_layout')
  @patch('trading_economics_table_graph_plot.plt.legend')
  @patch('trading_economics_table_graph_plot.plt.ylabel')
  @patch('trading_economics_table_graph_plot.plt.xlabel')
  @patch('trading_economics_table_graph_plot.plt.title')
  @patch('trading_economics_table_graph_plot.plt.plot')
  @patch('trading_economics_table_graph_plot.plt.figure')
  def test_plot_stock_market_comparison(self, mock_figure, mock_plot, mock_title, mock_xlabel, mock_ylabel, mock_legend, mock_tight_layout, mock_show):
    # Create a sample DataFrame
    data = {
      'Country': ['Mexico', 'Sweden', 'New Zealand'],
      'Category': ['Stock Market', 'Stock Market', 'Stock Market'],
      'q1_date': ['2023-01-01', '2023-01-01', '2023-01-01'],
      'q2_date': ['2023-04-01', '2023-04-01', '2023-04-01'],
      'q3_date': ['2023-07-01', '2023-07-01', '2023-07-01'],
      'q4_date': ['2023-10-01', '2023-10-01', '2023-10-01'],
      'q1': [100, 200, 300],
      'q2': [110, 210, 310],
      'q3': [120, 220, 320],
      'q4': [130, 230, 330]
    }
    df = pd.DataFrame(data)

    # Call the function
    plot_stock_market_comparison(df)

    # Check if the figure was created
    mock_figure.assert_called_once_with(figsize=(10, 6))
    # Check if the plot function was called for each country and each quarter
    self.assertEqual(mock_plot.call_count, 12)
    # Check if the title, xlabel, ylabel, legend, and tight_layout were called
    mock_title.assert_called_once_with('Quarterly Stock Market Comparison across Countries: Mexico, Sweden, New Zealand')
    mock_xlabel.assert_called_once_with('Date')
    mock_ylabel.assert_called_once_with('Stock Market Index')
    mock_legend.assert_called_once_with(bbox_to_anchor=(1.05, 1), loc='upper left')
    mock_tight_layout.assert_called_once()
    # Check if plt.show() was called
    mock_show.assert_called_once()

if __name__ == '__main__':
  unittest.main()