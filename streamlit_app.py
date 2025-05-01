import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import gdown

# Set page config
#test comment
st.set_page_config(
    page_title="SF Crime Data Visualization",
    page_icon="🚨",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1E3A8A;
    text-align: center;
    margin-bottom: 2rem;
}
.subheader {
    font-size: 1.5rem;
    font-weight: bold;
    color: #1E3A8A;
    margin-top: 1rem;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<p class="main-header">San Francisco Crime Data Visualization</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Visualization Settings")

# File uploader
uploaded_file = st.sidebar.file_uploader("Upload your SF crime data CSV", type="csv")

# Initialize date_column variable
date_column = None

# Demo data loading function
@st.cache_data
def load_demo_data():
    try:
        df = pd.read_csv("train_small.csv")
        df.drop_duplicates(inplace=True)
        
        # Check for date column with different possible names
        date_columns = ['Dates', 'Date', 'date', 'DATETIME', 'datetime']
        date_column = next((col for col in date_columns if col in df.columns), None)
        
        if date_column:
            df[date_column] = pd.to_datetime(df[date_column])
            df['Hour'] = df[date_column].dt.hour
            df['Month'] = df[date_column].dt.month
            df['Year'] = df[date_column].dt.year
            df['day'] = df[date_column].dt.day
        else:
            st.warning("No date column found in the dataset. Time-based analysis will not be available.")
            
        return df
    except Exception as e:
        st.error(f"Error loading demo data: {str(e)}")
        return pd.DataFrame()  # Return empty dataframe on error

# Load data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    # Ensure proper datetime conversion and hour extraction if needed
    date_column = 'Date' if 'Date' in df.columns else 'Dates'
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column])
        if 'Hour' not in df.columns:
            df['Hour'] = df[date_column].dt.hour
        if 'DayOfWeek' not in df.columns:
            df['DayOfWeek'] = df[date_column].dt.day_name()
        if 'Month' not in df.columns:
            df['Month'] = df[date_column].dt.month_name()
else:
    df = load_demo_data()
    date_column = 'Dates'  # Set date_column for demo data
    st.sidebar.info("Using demo data. Upload your own CSV for custom analysis.")

# Create tabs for different visualizations
tab1, tab2, tab3, tab4 = st.tabs(["Crime Categories", "District Distribution", "Time Analysis", "Additional Insights"])

with tab1:
    st.markdown('<p class="subheader">Crime Distribution by Category</p>', unsafe_allow_html=True)
    
    # Controls for category visualization
    col1, col2 = st.columns([1, 1])
    with col1:
        num_categories = st.slider("Number of top categories to show", 5, 20, 15)
    with col2:
        color_palette = st.selectbox("Color palette", 
                                   ["coolwarm", "viridis", "plasma", "inferno", "magma", "cividis", 
                                    "Blues", "Greens", "Reds", "Purples", "Oranges"])
    
    # Visualization options
    chart_type = st.radio("Chart type", ["Bar Chart", "Horizontal Bar", "Treemap"], horizontal=True)
    
    # Get top crimes
    top_crimes = df['Category'].value_counts().head(num_categories)
    top_crimes_df = pd.DataFrame({'Category': top_crimes.index, 'Count': top_crimes.values})
    
    if chart_type == "Bar Chart":
        fig = px.bar(
            top_crimes_df, 
            x='Category', 
            y='Count',
            color='Category',
            color_discrete_sequence=getattr(px.colors.sequential, color_palette.lower(), px.colors.qualitative.Plotly),
            labels={'Count': 'Number of Incidents', 'Category': 'Crime Category'},
            title=f'Top {num_categories} Crime Categories'
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
    elif chart_type == "Horizontal Bar":
        fig = px.bar(
            top_crimes_df, 
            x='Count', 
            y='Category',
            color='Category',
            color_discrete_sequence=getattr(px.colors.sequential, color_palette.lower(), px.colors.qualitative.Plotly),
            labels={'Count': 'Number of Incidents', 'Category': 'Crime Category'},
            title=f'Top {num_categories} Crime Categories',
            orientation='h'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # Treemap
        fig = px.treemap(
            top_crimes_df, 
            path=['Category'], 
            values='Count',
            color='Count',
            color_continuous_scale=getattr(px.colors.sequential, color_palette.lower(), px.colors.sequential.Viridis),
            title=f'Top {num_categories} Crime Categories'
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown('<p class="subheader">Crime Distribution by District</p>', unsafe_allow_html=True)
    
    # Controls for district visualization
    viz_type = st.radio("Visualization type", ["Pie Chart", "Bar Chart", "Map"], horizontal=True)
    
    if viz_type in ["Pie Chart", "Bar Chart"]:
        # Get district counts
        district_counts = df['PdDistrict'].value_counts()
        district_df = pd.DataFrame({'District': district_counts.index, 'Count': district_counts.values})
        
        # Color options
        district_color = st.selectbox("Color scheme for districts", 
                                    ["Blues", "Greens", "Reds", "Purples", "Oranges", 
                                     "viridis", "plasma", "inferno", "magma"])
        
        if viz_type == "Pie Chart":
            # Control for pie chart
            donut = st.checkbox("Display as donut chart", value=False)
            
            fig = px.pie(
                district_df,
                names='District',
                values='Count',
                title='Crime Distribution by District',
                color_discrete_sequence=getattr(px.colors.sequential, district_color, px.colors.qualitative.Plotly)
            )
            
            if donut:
                fig.update_traces(hole=0.4)
                
            fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Bar Chart
            sort_order = st.radio("Sort order", ["Descending", "Ascending", "Alphabetical"], horizontal=True)
            
            if sort_order == "Descending":
                district_df = district_df.sort_values('Count', ascending=False)
            elif sort_order == "Ascending":
                district_df = district_df.sort_values('Count', ascending=True)
            else:  # Alphabetical
                district_df = district_df.sort_values('District')
                
            fig = px.bar(
                district_df,
                x='District',
                y='Count',
                color='Count',
                title='Crime by District',
                color_discrete_sequence=getattr(px.colors.sequential, district_color, px.colors.qualitative.Plotly)
            )
            
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    else:  # Map
        st.info("In a real application, this would display a map of San Francisco with crime hotspots. For the demo, we're showing a placeholder.")
        
        # Placeholder for map
        st.image("https://via.placeholder.com/800x400?text=San+Francisco+Crime+Map", use_column_width=True)
        st.write("Note: To implement an actual map, you would need geographical coordinates (latitude/longitude) in your dataset and use libraries like folium or pydeck.")

with tab3:
    st.markdown('<p class="subheader">Crime Analysis by Time</p>', unsafe_allow_html=True)
    
    # Time analysis type
    time_analysis = st.radio("Analyze by", ["Hour of Day", "Day of Week", "Month"], horizontal=True)
    
    # Line style options
    col1, col2 = st.columns([1, 1])
    with col1:
        line_color = st.color_picker("Line color", "#483D8B")
    with col2:
        marker_color = st.color_picker("Marker color", "#9370DB")
    
    marker_size = st.slider("Marker size", 5, 15, 8)
    line_width = st.slider("Line width", 1, 5, 2)
    
    if time_analysis == "Hour of Day":
        # Group by hour
        crime_by_hour = df.groupby('Hour')['Category'].count().reset_index()
        crime_by_hour.columns = ['Hour', 'Count']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=crime_by_hour['Hour'],
            y=crime_by_hour['Count'],
            mode='lines+markers',
            line=dict(color=line_color, width=line_width),
            marker=dict(color=marker_color, size=marker_size),
            name='Incidents'
        ))
        
        fig.update_layout(
            title='Crime Incidents by Hour of Day',
            xaxis=dict(
                title='Hour (24-hour format)',
                tickmode='linear',
                tick0=0,
                dtick=1
            ),
            yaxis=dict(title='Number of Incidents'),
            hovermode='x',
            plot_bgcolor='rgba(240, 240, 240, 0.5)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    elif time_analysis == "Day of Week":
        # Ensure proper day of week ordering
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Group by day of week
        crime_by_dow = df['DayOfWeek'].value_counts().reset_index()
        crime_by_dow.columns = ['DayOfWeek', 'Count']
        
        # Reorder days
        crime_by_dow['DayOfWeek'] = pd.Categorical(crime_by_dow['DayOfWeek'], categories=day_order, ordered=True)
        crime_by_dow = crime_by_dow.sort_values('DayOfWeek')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=crime_by_dow['DayOfWeek'],
            y=crime_by_dow['Count'],
            mode='lines+markers',
            line=dict(color=line_color, width=line_width),
            marker=dict(color=marker_color, size=marker_size),
            name='Incidents'
        ))
        
        fig.update_layout(
            title='Crime Incidents by Day of Week',
            xaxis=dict(title='Day of Week'),
            yaxis=dict(title='Number of Incidents'),
            hovermode='x',
            plot_bgcolor='rgba(240, 240, 240, 0.5)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # Month analysis
        if date_column in df.columns:
            # Extract month
            df['Month'] = df[date_column].dt.month_name()
            
            # Ensure proper month ordering
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            
            # Group by month
            crime_by_month = df['Month'].value_counts().reset_index()
            crime_by_month.columns = ['Month', 'Count']
            
            # Reorder months
            crime_by_month['Month'] = pd.Categorical(crime_by_month['Month'], categories=month_order, ordered=True)
            crime_by_month = crime_by_month.sort_values('Month')
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=crime_by_month['Month'],
                y=crime_by_month['Count'],
                mode='lines+markers',
                line=dict(color=line_color, width=line_width),
                marker=dict(color=marker_color, size=marker_size),
                name='Incidents'
            ))
            
            fig.update_layout(
                title='Crime Incidents by Month',
                xaxis=dict(title='Month'),
                yaxis=dict(title='Number of Incidents'),
                hovermode='x',
                plot_bgcolor='rgba(240, 240, 240, 0.5)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Month analysis requires a Date column in your dataset.")

with tab4:
    st.markdown('<p class="subheader">Additional Insights</p>', unsafe_allow_html=True)
    
    insight_type = st.selectbox(
        "Select insight type",
        ["Crime Category by District", "Crime Category by Time of Day", "Custom Analysis"]
    )

    if insight_type == "Crime Category by District":
        # Get top categories for analysis
        top_n_categories = st.slider("Number of categories to analyze", 3, 10, 5)
        top_categories = df['Category'].value_counts().head(top_n_categories).index.tolist()
        
        # Filter data
        filtered_df = df[df['Category'].isin(top_categories)]
        
        # Create pivot table
        pivot_df = pd.crosstab(filtered_df['Category'], filtered_df['PdDistrict'])
        
        # Visualization
        st.write(f"Distribution of Top {top_n_categories} Crime Categories Across Districts")
        
        # Choose between heatmap and stacked bar
        viz_option = st.radio("Visualization type", ["Heatmap", "Stacked Bar Chart"], horizontal=True)
        
        if viz_option == "Heatmap":
            fig = px.imshow(
                pivot_df,
                color_continuous_scale='RdBu_r',
                aspect="auto",
                labels=dict(x="District", y="Crime Category", color="Count")
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.bar(
                pivot_df.reset_index().melt(id_vars='Category', var_name='District', value_name='Count'),
                x='District',
                y='Count',
                color='Category',
                barmode='stack',
                labels={'Count': 'Number of Incidents'}
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    elif insight_type == "Crime Category by Time of Day":
        # Get top categories for analysis
        top_n_categories = st.slider("Number of categories to analyze", 3, 10, 5)
        top_categories = df['Category'].value_counts().head(top_n_categories).index.tolist()
        
        # Filter data
        filtered_df = df[df['Category'].isin(top_categories)]
        
        # Group by category and hour
        hour_cat_df = filtered_df.groupby(['Category', 'Hour']).size().reset_index(name='Count')
        
        fig = px.line(
            hour_cat_df,
            x='Hour',
            y='Count',
            color='Category',
            labels={'Count': 'Number of Incidents', 'Hour': 'Hour of Day'},
            title=f'Crime Patterns Throughout the Day for Top {top_n_categories} Categories'
        )
        
        fig.update_layout(
            xaxis=dict(tickmode='linear', tick0=0, dtick=1),
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
        )
        
        st.plotly_chart(fig, use_container_width=True)

    else:  # Custom Analysis
        st.write("Build your own custom analysis by selecting dimensions to compare:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            x_axis = st.selectbox("X-axis", ['Category', 'PdDistrict', 'Hour', 'DayOfWeek'])
        
        with col2:
            y_axis = st.selectbox("Y-axis", ['Count', 'Percentage'], index=0)
        
        # Optional color dimension
        color_by = st.selectbox("Color by", ['None', 'Category', 'PdDistrict', 'Hour', 'DayOfWeek'])
        
        # Generate analysis
        if x_axis != color_by or color_by == 'None':
            if color_by == 'None':
                # Simple count by x_axis
                if y_axis == 'Count':
                    count_df = df[x_axis].value_counts().reset_index()
                    count_df.columns = [x_axis, 'Count']
                    
                    fig = px.bar(
                        count_df,
                        x=x_axis,
                        y='Count',
                        title=f'Crime Incidents by {x_axis}'
                    )
                else:  # Percentage
                    count_df = df[x_axis].value_counts(normalize=True).reset_index()
                    count_df.columns = [x_axis, 'Percentage']
                    count_df['Percentage'] = count_df['Percentage'] * 100
                    
                    fig = px.bar(
                        count_df,
                        x=x_axis,
                        y='Percentage',
                        title=f'Crime Incidents by {x_axis} (%)'
                    )
            else:
                # Count by x_axis and color_by
                if y_axis == 'Count':
                    count_df = df.groupby([x_axis, color_by]).size().reset_index(name='Count')
                    
                    fig = px.bar(
                        count_df,
                        x=x_axis,
                        y='Count',
                        color=color_by,
                        title=f'Crime Incidents by {x_axis} and {color_by}'
                    )
                else:  # Percentage
                    # Calculate percentage within each x_axis group
                    count_df = df.groupby([x_axis, color_by]).size().reset_index(name='Count')
                    total_by_x = count_df.groupby(x_axis)['Count'].transform('sum')
                    count_df['Percentage'] = count_df['Count'] / total_by_x * 100
                    
                    fig = px.bar(
                        count_df,
                        x=x_axis,
                        y='Percentage',
                        color=color_by,
                        title=f'Crime Incidents by {x_axis} and {color_by} (%)'
                    )
            
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Please select different dimensions for X-axis and Color")

# Footer
st.markdown("---")
st.markdown("### About this app")
st.markdown("""
This interactive dashboard allows you to explore San Francisco crime data through various visualizations.
Upload your own CSV file or use the demo data to analyze crime patterns across categories, districts, and time periods.
""")

# Download options
st.markdown("### Export Visualizations")
st.write("To save any chart, hover over the visualization and click the camera icon.")