import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calendar
import os

# Set page configuration
st.set_page_config(
    page_title="Bike Sharing Analysis Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'main_data.csv')
    day_df = file_path
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    
    # Create month name and day name
    day_df['month_name'] = day_df['mnth'].apply(lambda x: calendar.month_name[x])
    weekday_mapping = {
        0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 
        4: 'Thursday', 5: 'Friday', 6: 'Saturday'
    }
    day_df['weekday_name'] = day_df['weekday'].map(weekday_mapping)
    
    # Create season and weather categories
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    day_df['season_cat'] = day_df['season'].map(season_mapping)
    
    weather_mapping = {
        1: 'Clear/Few clouds',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Ice/Storm'
    }
    day_df['weather_cat'] = day_df['weathersit'].map(weather_mapping)
    
    # Create year category
    day_df['year'] = day_df['yr'].map({0: 2011, 1: 2012})
    
    return day_df

# Load the data
df = load_data()

# Header
st.title("🚲 Bike Sharing Analysis Dashboard")
st.write("This dashboard provides insights into bike sharing usage patterns based on temporal and weather factors.")

# Sidebar for filtering
st.sidebar.header("Filters")

# Year filter
year_options = df['year'].unique().tolist()
selected_year = st.sidebar.selectbox("Select Year", year_options)

# Season filter
season_options = ['All'] + df['season_cat'].unique().tolist()
selected_season = st.sidebar.selectbox("Select Season", season_options)

# Weather filter
weather_options = ['All'] + df['weather_cat'].unique().tolist()
selected_weather = st.sidebar.selectbox("Select Weather", weather_options)

# Apply filters
filtered_df = df.copy()
if selected_year:
    filtered_df = filtered_df[filtered_df['year'] == selected_year]
if selected_season != 'All':
    filtered_df = filtered_df[filtered_df['season_cat'] == selected_season]
if selected_weather != 'All':
    filtered_df = filtered_df[filtered_df['weather_cat'] == selected_weather]

# Main metrics
st.header("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric("Total Bike Rentals", f"{total_rentals:,}")

with col2:
    avg_daily_rentals = filtered_df['cnt'].mean()
    st.metric("Average Daily Rentals", f"{avg_daily_rentals:.1f}")

with col3:
    casual_pct = (filtered_df['casual'].sum() / filtered_df['cnt'].sum()) * 100
    registered_pct = (filtered_df['registered'].sum() / filtered_df['cnt'].sum()) * 100
    st.metric("Casual vs Registered", f"{casual_pct:.1f}% : {registered_pct:.1f}%")

# Create tabs
tab1, tab2 = st.tabs(["Temporal Analysis", "User Type Analysis"])

with tab1:
    st.header("Temporal Patterns in Bike Rentals")
    
    # Monthly trends
    st.subheader("Monthly Trends")
    monthly_data = filtered_df.groupby('month_name')['cnt'].mean().reset_index()
    month_order = list(calendar.month_name)[1:]
    monthly_data['month_name'] = pd.Categorical(monthly_data['month_name'], categories=month_order, ordered=True)
    monthly_data = monthly_data.sort_values('month_name')
    
    fig_monthly = px.line(
        monthly_data, 
        x='month_name', 
        y='cnt',
        markers=True,
        title='Average Daily Rentals by Month',
        labels={'cnt': 'Average Rentals', 'month_name': 'Month'}
    )
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Daily patterns
    st.subheader("Weekday vs Weekend Patterns")
    col1, col2 = st.columns(2)
    
    with col1:
        # By day of week
        weekday_data = filtered_df.groupby('weekday_name')['cnt'].mean().reset_index()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_data['weekday_name'] = pd.Categorical(weekday_data['weekday_name'], categories=days_order, ordered=True)
        weekday_data = weekday_data.sort_values('weekday_name')
        
        fig_weekday = px.bar(
            weekday_data, 
            x='weekday_name', 
            y='cnt',
            title='Average Rentals by Day of Week',
            labels={'cnt': 'Average Rentals', 'weekday_name': 'Day of Week'},
            color='cnt',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_weekday, use_container_width=True)
    
    with col2:
        # Workingday vs non-workingday
        working_data = filtered_df.groupby('workingday')['cnt'].mean().reset_index()
        working_data['workingday'] = working_data['workingday'].map({0: 'Non-Working Day', 1: 'Working Day'})
        
        fig_working = px.pie(
            working_data, 
            values='cnt', 
            names='workingday',
            title='Average Rentals: Working vs Non-Working Days',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_working, use_container_width=True)
    
    # Seasonal and weather analysis
    st.subheader("Seasonal and Weather Impact")
    col1, col2 = st.columns(2)
    
    with col1:
        # By season
        season_data = filtered_df.groupby('season_cat')['cnt'].mean().reset_index()
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        season_data['season_cat'] = pd.Categorical(season_data['season_cat'], categories=season_order, ordered=True)
        season_data = season_data.sort_values('season_cat')
        
        fig_season = px.bar(
            season_data, 
            x='season_cat', 
            y='cnt',
            title='Average Rentals by Season',
            labels={'cnt': 'Average Rentals', 'season_cat': 'Season'},
            color='cnt',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_season, use_container_width=True)
    
    with col2:
        # By weather
        weather_data = filtered_df.groupby('weather_cat')['cnt'].mean().reset_index()
        
        fig_weather = px.bar(
            weather_data, 
            x='weather_cat', 
            y='cnt',
            title='Average Rentals by Weather Condition',
            labels={'cnt': 'Average Rentals', 'weather_cat': 'Weather Condition'},
            color='cnt',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_weather, use_container_width=True)
    
    # Temperature and humidity impact
    st.subheader("Impact of Weather Variables")
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature vs rentals
        fig_temp = px.scatter(
            filtered_df, 
            x='temp', 
            y='cnt',
            color='season_cat',
            title='Temperature vs Bike Rentals',
            labels={'cnt': 'Total Rentals', 'temp': 'Normalized Temperature', 'season_cat': 'Season'},
            trendline="ols"
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with col2:
        # Humidity vs rentals
        fig_hum = px.scatter(
            filtered_df, 
            x='hum', 
            y='cnt',
            color='weather_cat',
            title='Humidity vs Bike Rentals',
            labels={'cnt': 'Total Rentals', 'hum': 'Normalized Humidity', 'weather_cat': 'Weather'},
            trendline="ols"
        )
        st.plotly_chart(fig_hum, use_container_width=True)

with tab2:
    st.header("User Type Analysis")
    
    # Create user type comparison dataframe
    user_type_df = filtered_df[['dteday', 'season_cat', 'month_name', 'weekday_name', 'weather_cat', 'temp', 'casual', 'registered']].copy()
    # Create user type comparison dataframe
    user_type_df = filtered_df[['dteday', 'season_cat', 'month_name', 'weekday_name', 'weather_cat', 'temp', 'casual', 'registered']].copy()
    user_type_df_melted = user_type_df.melt(
        id_vars=['dteday', 'season_cat', 'month_name', 'weekday_name', 'weather_cat', 'temp'],
        value_vars=['casual', 'registered'],
        var_name='user_type',
        value_name='count'
    )
    
    # Overall user type distribution
    st.subheader("Casual vs Registered Users")
    
    total_casual = filtered_df['casual'].sum()
    total_registered = filtered_df['registered'].sum()
    user_dist = pd.DataFrame({
        'User Type': ['Casual', 'Registered'],
        'Count': [total_casual, total_registered]
    })
    
    fig_user_dist = px.pie(
        user_dist,
        values='Count',
        names='User Type',
        title='Distribution of User Types',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    st.plotly_chart(fig_user_dist, use_container_width=True)
    
    # Seasonal trends by user type
    st.subheader("Seasonal Patterns by User Type")
    seasonal_user = user_type_df_melted.groupby(['season_cat', 'user_type'])['count'].mean().reset_index()
    seasonal_user['season_cat'] = pd.Categorical(seasonal_user['season_cat'], 
                                              categories=['Spring', 'Summer', 'Fall', 'Winter'],
                                              ordered=True)
    seasonal_user = seasonal_user.sort_values('season_cat')
    
    fig_seasonal_user = px.bar(
        seasonal_user,
        x='season_cat',
        y='count',
        color='user_type',
        barmode='group',
        title='Average Users by Season and User Type',
        labels={'count': 'Average Users', 'season_cat': 'Season', 'user_type': 'User Type'}
    )
    st.plotly_chart(fig_seasonal_user, use_container_width=True)
    
    # Weekday patterns
    st.subheader("Weekly Patterns by User Type")
    weekday_user = user_type_df_melted.groupby(['weekday_name', 'user_type'])['count'].mean().reset_index()
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_user['weekday_name'] = pd.Categorical(weekday_user['weekday_name'], categories=days_order, ordered=True)
    weekday_user = weekday_user.sort_values('weekday_name')
    
    fig_weekday_user = px.line(
        weekday_user,
        x='weekday_name',
        y='count',
        color='user_type',
        markers=True,
        title='Average Users by Day of Week and User Type',
        labels={'count': 'Average Users', 'weekday_name': 'Day of Week', 'user_type': 'User Type'}
    )
    st.plotly_chart(fig_weekday_user, use_container_width=True)
    
    # Weather sensitivity
    st.subheader("Weather Sensitivity by User Type")
    col1, col2 = st.columns(2)
    
    with col1:
        # Weather condition effect
        weather_user = user_type_df_melted.groupby(['weather_cat', 'user_type'])['count'].mean().reset_index()
        
        fig_weather_user = px.bar(
            weather_user,
            x='weather_cat',
            y='count',
            color='user_type',
            barmode='group',
            title='Average Users by Weather and User Type',
            labels={'count': 'Average Users', 'weather_cat': 'Weather Condition', 'user_type': 'User Type'}
        )
        st.plotly_chart(fig_weather_user, use_container_width=True)
    
    with col2:
        # Temperature effect
        fig_temp_user = px.scatter(
            user_type_df_melted,
            x='temp',
            y='count',
            color='user_type',
            trendline="ols",
            title='Temperature Sensitivity by User Type',
            labels={'count': 'Number of Users', 'temp': 'Normalized Temperature', 'user_type': 'User Type'}
        )
        st.plotly_chart(fig_temp_user, use_container_width=True)
    
    # Monthly trends
    st.subheader("Monthly Trends by User Type")
    monthly_user = user_type_df_melted.groupby(['month_name', 'user_type'])['count'].mean().reset_index()
    month_order = list(calendar.month_name)[1:]
    monthly_user['month_name'] = pd.Categorical(monthly_user['month_name'], categories=month_order, ordered=True)
    monthly_user = monthly_user.sort_values('month_name')
    
    fig_monthly_user = px.line(
        monthly_user,
        x='month_name',
        y='count',
        color='user_type',
        markers=True,
        title='Average Users by Month and User Type',
        labels={'count': 'Average Users', 'month_name': 'Month', 'user_type': 'User Type'}
    )
    st.plotly_chart(fig_monthly_user, use_container_width=True)

# Conclusion and insights
st.header("Key Insights")
st.write("""
### Temporal Patterns
- Peak bike rental occurs during summer and fall seasons
- Working days show distinct commuting patterns with peaks at 8 AM and 5-6 PM
- Weekends show more distributed usage throughout the day
- Weather significantly impacts bike rentals, with clear weather showing highest usage

### User Type Differences
- Registered users are more consistent throughout the week, showing commuter patterns
- Casual users increase significantly on weekends and holidays
- Casual users are more sensitive to weather conditions and seasonal changes
- Temperature has a strong positive correlation with bike rentals for both user types
""")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Bike Sharing Dataset Analysis - Created for Dicoding Final Project")