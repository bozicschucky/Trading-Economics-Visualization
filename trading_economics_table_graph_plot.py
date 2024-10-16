from dotenv import load_dotenv
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

def load_or_fetch_data(csv_file):
  """
  Load data from a CSV file or fetch from the API if the file does not exist.

  Parameters:
  csv_file (str): The path to the CSV file.

  Returns:
  pandas.DataFrame: The DataFrame containing the data.
  This prevents making unnecessary API calls if the data has already been fetched and saved to a CSV file.
  """
  if not os.path.exists(csv_file):
    api_key = os.getenv("API_KEY")
    url = f'https://api.tradingeconomics.com/forecast/country/Mexico,New Zealand,Sweden?c={api_key}'
    data = requests.get(url).json()
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
  else:
    df = pd.read_csv(csv_file)

  return df


def plot_core_inflation_comparison(df):
  """
  Plots the core inflation rate comparison across countries.

  Parameters:
  df (pandas.DataFrame): The DataFrame containing the core inflation data.
  """
  core_inflation_data = df[df['Category'] == 'Core Inflation Rate']

  core_inflation_table = core_inflation_data[['Country', 'q1', 'q2', 'q3', 'q4']]
  print(core_inflation_table)

  plt.figure(figsize=(8, 5))
  for country in core_inflation_data['Country'].unique():
    country_data = core_inflation_data[core_inflation_data['Country'] == country]
    plt.plot(['q1', 'q2', 'q3', 'q4'], country_data[['q1', 'q2', 'q3', 'q4']].values[0], marker='o', label=country)

  plt.title('Quarterly Core Inflation Rate Comparison: Mexico, Sweden, New Zealand')
  plt.xlabel('Quarter')
  plt.ylabel('Core Inflation Rate (%)')
  plt.legend()
  plt.tight_layout()
  plt.show()


def plot_stock_market_comparison(df):
  """
  Plots the time series chart for stock market comparison across countries.

  Parameters:
  df (pandas.DataFrame): The DataFrame containing the stock market data.
  """
  stock_market_data = df[df['Category'].str.contains('Stock Market', case=False, na=False)]

  stock_market_data.loc[:, 'q1_date'] = pd.to_datetime(stock_market_data['q1_date'])
  stock_market_data.loc[:, 'q2_date'] = pd.to_datetime(stock_market_data['q2_date'])
  stock_market_data.loc[:, 'q3_date'] = pd.to_datetime(stock_market_data['q3_date'])
  stock_market_data.loc[:, 'q4_date'] = pd.to_datetime(stock_market_data['q4_date'])

  plt.figure(figsize=(10, 6))

  for country in stock_market_data['Country'].unique():
    country_data = stock_market_data[stock_market_data['Country'] == country]

    plt.plot(country_data['q1_date'], country_data['q1'], marker='o', label=f'{country} Q1')
    plt.plot(country_data['q2_date'], country_data['q2'], marker='o', label=f'{country} Q2')
    plt.plot(country_data['q3_date'], country_data['q3'], marker='o', label=f'{country} Q3')
    plt.plot(country_data['q4_date'], country_data['q4'], marker='o', label=f'{country} Q4')

  plt.title('Quarterly Stock Market Comparison across Countries: Mexico, Sweden, New Zealand')
  plt.xlabel('Date')
  plt.ylabel('Stock Market Index')
  plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
  plt.tight_layout()
  plt.show()



if __name__ == '__main__':
  csv_file = 'mexico_new_zealand_sweden_forecast.csv'
  df = load_or_fetch_data(csv_file)
  plot_core_inflation_comparison(df)
  plot_stock_market_comparison(df)
