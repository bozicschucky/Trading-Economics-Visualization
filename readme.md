# Trading Economics Data Visualization

This project visualizes economic forecast data for Mexico, New Zealand, and Sweden. It includes comparisons of core inflation rates and stock market indices across different quarters.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [License](#license)

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/trading_economics_app.git
   cd trading_economics_app
   ```

2. **Create a virtual environment**:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**: Create a `.env` file in the root directory and add your Trading Economics API key:
   ```
   API_KEY=your_api_key
   ```

## Usage

Run the script:
```sh
python trading_economics_table_graph_plot.py
```

View the plots: The script will generate and display plots comparing the core inflation rates and stock market indices for Mexico, New Zealand, and Sweden.

## Testing

Run the tests:
```sh
pytest
```

Test Structure:
- `tests/conftest.py`: Configures the test environment.
- `tests/test_trading_economics_table_graph_plot.py`: Contains unit tests for the functions in `trading_economics_table_graph_plot.py`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
