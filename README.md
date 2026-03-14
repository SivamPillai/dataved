# Data Analytics Dashboard

[![Python Tests](https://github.com/Zolnoi/data-dashboard/actions/workflows/tests.yml/badge.svg)](https://github.com/Zolnoi/data-dashboard/actions/workflows/tests.yml)

A Streamlit-based dashboard for analyzing electrical current data and harmonics from MongoDB. This application provides interactive visualizations and analysis tools for electrical current measurements and their harmonic components.

## Features

- **Data Fetching**: Retrieve data from MongoDB based on machine ID, tenant ID, and time range
- **Current Analysis**: Visualize current trends with interactive plots
- **Harmonics Analysis**: Analyze harmonic components of current measurements
- **Interactive UI**: User-friendly interface with customizable parameters
- **Data Cleaning**: Automatic handling of null values and data preprocessing

## Prerequisites

- Python 3.x
- MongoDB connection
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up secrets:
   - Create a `.streamlit/secrets.toml` file with the following structure:
     ```toml
     [mongodb]
     uri = "your_mongodb_uri"
     db_name = "your_database_name"
     ```
   - Replace the values with your actual MongoDB credentials
   - Note: Never commit the secrets.toml file to version control

## Usage

1. Start the Streamlit app:
   ```bash
   streamlit run data_dashboard.py
   ```

2. Use the sidebar to configure:
   - Dataset Name
   - Machine ID
   - Tenant ID
   - Collection Name
   - Date and Time Range

3. Click "Fetch Data" to retrieve data from MongoDB

4. Select datasets for analysis from the available options

5. Choose between:
   - Trend Analysis: View current measurements over time
   - Harmonics Analysis: Analyze harmonic components

## Data Structure

The application expects MongoDB documents with the following structure:
- `metaData`: Contains `machine_id` and `tenant_id`
- `timestamp`: Time of measurement
- Current measurements (`cur1`, `cur2`, `cur3`)
- Harmonic components (`ch1`, `ch2`, `ch3`)

## Features in Detail

### Current Analysis
- Displays rolling average of current measurements
- Interactive time series plots
- Multiple current channels visualization

### Harmonics Analysis
- Area plots showing harmonic components
- Comparison across multiple datasets
- Customizable visualization parameters

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is part of the Zolnoi Codebase and is proprietary software with restricted access. All rights reserved. Unauthorized copying, modification, distribution, or use of this software is strictly prohibited.
