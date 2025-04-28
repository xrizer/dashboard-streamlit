# Bike Sharing Analysis Dashboard

## Setup Environment

```bash
pip install -r requirements.txt
```

## Run Dashboard

```bash
cd dashboard
streamlit run dashboard.py
```

## Project Structure

- **data/**: Contains the original dataset files
  - `day.csv`: Daily aggregated bike sharing data
  - `hour.csv`: Hourly aggregated bike sharing data
- **dashboard/**: Contains files for the Streamlit dashboard
  - `main_data.csv`: Processed data for the dashboard
  - `dashboard.py`: Streamlit dashboard application
- `notebook.ipynb`: Jupyter notebook containing the full data analysis process
- `requirements.txt`: List of required Python packages
- `README.md`: Project documentation

## About the Dataset

The Bike Sharing dataset contains the hourly and daily count of rental bikes between years 2011 and 2012 from the Capital Bikeshare system in Washington, D.C., with corresponding weather and seasonal information.

## Analysis Questions

- How does bike usage pattern vary based on time (hour, day, month, season) and weather factors?
- What are the differences in characteristics between casual and registered users in using the bike sharing service?

## Key Insights

- Bike usage is heavily influenced by both temporal factors (hour, day, season) and weather conditions.
- There are clear commuting patterns on weekdays with peaks at morning and evening rush hours.
- Casual and registered users show different usage patterns, with registered users displaying more consistent, commute-oriented usage.
- Weather conditions significantly impact bike rentals, with poor weather leading to decreased usage.

