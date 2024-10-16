import unittest
from unittest.mock import patch
import pandas as pd
from trading_economics_table_graph_plot import load_or_fetch_data
from unittest.mock import patch
from trading_economics_table_graph_plot import plot_core_inflation_comparison
from unittest.mock import patch
from trading_economics_table_graph_plot import plot_stock_market_comparison

class TestTradingEconomicsTableGraphPlot(unittest.TestCase):

  @patch('trading_economics_table_graph_plot.os.path.exists')
  @patch('trading_economics_table_graph_plot.pd.read_csv')
  def test_load_data_from_csv(self, mock_read_csv, mock_path_exists):
    mock_path_exists.return_value = True
    mock_df = pd.DataFrame({'Country': ['Mexico'], 'Category': ['Core Inflation Rate'], 'q1': [1.0], 'q2': [1.1], 'q3': [1.2], 'q4': [1.3]})
    mock_read_csv.return_value = mock_df

    csv_file = 'dummy.csv'
    df = load_or_fetch_data(csv_file)

    mock_read_csv.assert_called_once_with(csv_file)
    pd.testing.assert_frame_equal(df, mock_df)

  @patch('trading_economics_table_graph_plot.requests.get')
  @patch('trading_economics_table_graph_plot.pd.DataFrame.to_csv')
  @patch('trading_economics_table_graph_plot.os.path.exists')
  @patch('trading_economics_table_graph_plot.os.getenv')
  def test_fetch_data_from_api(self, mock_getenv, mock_path_exists, mock_to_csv, mock_requests_get):
    mock_path_exists.return_value = False
    mock_getenv.return_value = 'dummy_api_key'
    mock_response = {
      'Country': ['Mexico'], 'Category': ['Core Inflation Rate'], 'q1': [1.0], 'q2': [1.1], 'q3': [1.2], 'q4': [1.3]
    }
    mock_requests_get.return_value.json.return_value = mock_response
    mock_to_csv.return_value = None

    csv_file = 'dummy.csv'
    df = load_or_fetch_data(csv_file)

    mock_requests_get.assert_called_once_with(
        'https://api.tradingeconomics.com/forecast/country/Mexico,New Zealand,Sweden?c=dummy_api_key')
    mock_to_csv.assert_called_once_with(csv_file, index=False)
    expected_df = pd.DataFrame(mock_response)
    pd.testing.assert_frame_equal(df, expected_df)



  @patch('trading_economics_table_graph_plot.plt.show')
  @patch('trading_economics_table_graph_plot.plt.figure')
  @patch('trading_economics_table_graph_plot.plt.plot')
  @patch('trading_economics_table_graph_plot.plt.title')
  @patch('trading_economics_table_graph_plot.plt.xlabel')
  @patch('trading_economics_table_graph_plot.plt.ylabel')
  @patch('trading_economics_table_graph_plot.plt.legend')
  @patch('trading_economics_table_graph_plot.plt.tight_layout')
  def test_plot_core_inflation_comparison(self, mock_tight_layout, mock_legend, mock_ylabel, mock_xlabel, mock_title, mock_plot, mock_figure, mock_show):
      data = {
          'Country': ['Mexico', 'Sweden', 'New Zealand'],
          'Category': ['Core Inflation Rate', 'Core Inflation Rate', 'Core Inflation Rate'],
          'q1': [1.0, 1.1, 1.2],
          'q2': [1.3, 1.4, 1.5],
          'q3': [1.6, 1.7, 1.8],
          'q4': [1.9, 2.0, 2.1]
      }
      df = pd.DataFrame(data)

      plot_core_inflation_comparison(df)

      mock_figure.assert_called_once_with(figsize=(8, 5))
      self.assertEqual(mock_plot.call_count, 3)
      mock_title.assert_called_once_with(
          'Quarterly Core Inflation Rate Comparison: Mexico, Sweden, New Zealand')
      mock_xlabel.assert_called_once_with('Quarter')
      mock_ylabel.assert_called_once_with('Core Inflation Rate (%)')
      mock_legend.assert_called_once()
      mock_tight_layout.assert_called_once()
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

    plot_stock_market_comparison(df)

    mock_figure.assert_called_once_with(figsize=(10, 6))
    self.assertEqual(mock_plot.call_count, 12)
    mock_title.assert_called_once_with('Quarterly Stock Market Comparison across Countries: Mexico, Sweden, New Zealand')
    mock_xlabel.assert_called_once_with('Date')
    mock_ylabel.assert_called_once_with('Stock Market Index')
    mock_legend.assert_called_once_with(bbox_to_anchor=(1.05, 1), loc='upper left')
    mock_tight_layout.assert_called_once()
    mock_show.assert_called_once()

if __name__ == '__main__':
  unittest.main()