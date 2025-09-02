# Laevitas API

A Python package to interact with the Laevitas API for retrieving historical options and futures data.

## Installation

Install the package directly from GitHub:

```bash
pip install git+https://github.com/yourusername/laevitas_api.git
```

To install a specific version or update to the latest version:

```bash
pip install --upgrade git+https://github.com/yourusername/laevitas_api.git
```

## Prerequisites

- Python 3.8+
- An API key from Laevitas (set as environment variable `api_lav`)

Set your API key:

```bash
export api_lav='your-api-key-here'
```

## Usage

To avoid naming conflicts with other Python modules, always import functions from the `laevitas_api` package explicitly:

```python
from laevitas_api import get_OptTrades, get_OptSnapshot, get_FutSnapshot, get_lav_implied_vol
from laevitas_api import utilities as ut  # Use this to avoid conflicts with other 'utilities' modules

# Get options trades
df_trades = get_OptTrades("DERIBIT", "BTC", "2025-01-06")

# Get options snapshot
df_snapshot = get_OptSnapshot("DERIBIT", "BTC", "2025-01-06", "2025-01-07", "1h")

# Get futures snapshot
df_futures = get_FutSnapshot("DERIBIT", "BTC", "2025-01-06", "2025-01-07", "1h")

# Get implied volatility
result = get_lav_implied_vol("BTC-31DEC25-50000-C", "2025-01-07")

# Example using utilities
dates = ut.generate_all_daily_dates("2025-01-01", "2025-01-07")
```

## Functions

- `get_OptTrades(exchange, theCoin, theDate, max_retries=20)`: Retrieve historical options trades.
- `get_OptSnapshot(exchange, theCoin, dt_beg, dt_end, freq, max_retries=20)`: Retrieve options snapshot data.
- `get_FutSnapshot(exchange, theCoin, dt_beg, dt_end, freq, max_retries=20)`: Retrieve futures snapshot data.
- `get_lav_implied_vol(instrument, dt_str)`: Retrieve implied volatility for a specific option instrument.
- `laevitas_api.utilities`: Contains helper functions like `to_timestamp`, `convert_uxtimestamp_to_hkt`, etc.

## Dependencies

- requests
- pandas
- pytz

## Development

To contribute or modify the package:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/laevitas_api.git
   cd laevitas_api
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run tests:
   ```bash
   pytest
   ```

## Avoiding Naming Conflicts

The `utilities` module is scoped under `laevitas_api`. To avoid conflicts with other Python modules named `utilities`, always import it as:

```python
from laevitas_api import utilities as ut
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.