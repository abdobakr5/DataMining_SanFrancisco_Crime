# San Francisco Crime Data Visualization

## Overview

This interactive dashboard allows users to explore and visualize crime data in San Francisco. You can upload your own dataset or use the provided demo data to analyze crime patterns across categories, districts, and time periods.

## Features

- **Crime Categories Distribution**: Visualize the distribution of crime types in San Francisco.
- **District Distribution**: Understand crime occurrences across various districts.
- **Time Analysis**: Analyze crime data by hour of the day, day of the week, or month.
- **Additional Insights**: Explore custom insights such as crime category distribution across districts or time analysis for selected crime categories.

## Prerequisites

- Python 3.7+
- Streamlit
- Plotly
- Pandas
- Seaborn
- Matplotlib

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/sf-crime-data-visualization.git
    ```

2. Navigate to the project directory:

    ```bash
    cd sf-crime-data-visualization
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the Streamlit app:

    ```bash
    streamlit run streamlit_app.py
    ```

5. Open your browser and visit the URL shown in your terminal to access the app.

## Features

### 1. Crime Categories Distribution

- **Slider**: Adjust the number of top crime categories to display.
- **Chart Type**: Choose between Bar Chart, Horizontal Bar, or Treemap.
- **Color Palette**: Customize the color scheme for the chart.

### 2. Crime Distribution by District

- **Visualization Type**: Choose between Pie Chart, Bar Chart, or Map.
- **Controls**: Adjust color schemes, sort order, and customize map styles.

### 3. Time Analysis

- **Analyze by**: Select to view crimes based on Hour of Day, Day of Week, or Month.
- **Customize**: Choose line and marker colors, marker size, and line width for better data visualization.

### 4. Additional Insights

- **Crime Category by District**: Visualize crime category distribution across districts.
- **Crime Category by Time of Day**: Analyze crime patterns across different times of the day.
- **Custom Analysis**: Create custom visualizations by comparing different data dimensions.

## How to Use

1. **Upload Data**: You can upload your own SF crime data CSV file by clicking the file uploader on the sidebar(NOT DEVELOPED YET!).
   
2. **Demo Mode**: If no file is uploaded, the app will load a demo dataset. This allows you to explore the features even if you don't have your own dataset.

3. **Customization**: Adjust visualization settings like the number of crime categories, color palettes, and the type of chart to get the insights you need.

## Export Visualizations

You can download any of the visualizations directly from the app. Simply hover over the chart and click the camera icon to save it.

## About the Dataset

The dataset contains the following columns:

- `Category`: The type of crime.
- `Dates`: The date and time of the crime.
- `PdDistrict`: The police district where the crime occurred.
- `X`, `Y`: Coordinates for the crime location (used for map visualizations).
- Other columns related to crime characteristics and timestamps.

## Contributing

Feel free to fork this repository and create a pull request for any improvements, fixes, or features you would like to add.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses the [Plotly](https://plotly.com) library for interactive visualizations.
- Special thanks to the [San Francisco Police Department](https://data.sfgov.org) for providing the crime data.

## Contact us

For any questions or feedback, please open an issue on GitHub or reach out to [bedobakr65@gmail.com](mailto:bedobakr65@gmail.com).

