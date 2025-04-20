# 🏅 Olympics Analysis Dashboard

This interactive dashboard provides an in-depth analysis of the Olympics dataset, offering insights into medal tallies, athlete statistics, country-wise performance, and trends over time. Built with **Streamlit**, it serves as a comprehensive tool for exploring Olympics data visually and interactively.

[LIVE DEMO](https://aryansachan12-olympic-analysis-app-iykjpl.streamlit.app/)

## Features

1. **Medal Tally**: View medal tallies for specific years or countries.
2. **Overall Analysis**:
   - Key statistics (editions, host cities, sports, events, nations, athletes).
   - Participation trends over time for nations, events, and athletes.
   - Event distribution heatmap across years and sports.
   - Most successful athletes by sport.
3. **Country-wise Analysis**:
   - Historical performance trends of a selected country.
   - Heatmap of events participated in by the selected country.
   - Top 10 athletes of the country.
4. **Athlete-wise Analysis**:
   - Age distribution of athletes (categorized by medal status).
   - Age analysis for popular sports (gold medalists).
   - Height vs Weight scatter plot segmented by medal and gender.
   - Male vs Female participation trends over the years.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AryanSachan12/olympic-analysis.git
   ```
2. Navigate to the project directory:
   ```bash
   cd olympic-analysis
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Dataset

- **`athlete_events.csv`**: Contains details about Olympic athletes, their events, and results.
- **`noc_regions.csv`**: Provides region mapping for National Olympic Committees (NOCs).

Make sure these datasets are placed in the `datasets/` directory within the project root.

## Preprocessing

Data preprocessing is handled by the `preprocessor.py` module, which:

- Merges the athlete events dataset with the NOC regions dataset.
- Cleans and formats the data for visualization.

## Visualizations

The dashboard leverages the following visualization libraries:

- **Plotly**: Interactive line and scatter plots.
- **Seaborn**: Statistical heatmaps.
- **Matplotlib**: Supporting visual elements.

## Custom Styling

Streamlit customizations include:

- A streamlined layout with additional CSS styling.
- Sidebar navigation for easy exploration of different analyses.

## How to Use

1. Launch the dashboard by running:
   ```bash
   streamlit run app.py
   ```
2. Use the sidebar to select one of the following options:
   - **Medal Tally**: Choose a year and/or country to view the medal tally.
   - **Overall Analysis**: Gain insights into historical trends and key statistics.
   - **Country-wise Analysis**: Explore performance metrics for individual countries.
   - **Athlete-wise Analysis**: Dive into athlete-specific analyses, including age distributions, height-weight relationships, and participation trends.

## Contributing

Contributions are welcome! If you'd like to enhance the dashboard or add new features:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature"
   ```
4. Push to your fork:
   ```bash
   git push origin feature-branch-name
   ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

### Acknowledgements

Special thanks to:

- The creators of the Olympic datasets for providing a comprehensive resource.
- The open-source community for tools like Streamlit, Plotly, Seaborn, and Matplotlib.

> "Let the data tell the story of the world's greatest sporting event!" 🎉
