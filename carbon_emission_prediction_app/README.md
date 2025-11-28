# Carbon Emission Prediction App

A modern web application to predict carbon emissions based on user inputs using machine learning.

## Features

- **User Inputs**: Fuel consumption, vehicle type, distance, engine size, country factor
- **ML Model**: Linear Regression trained on synthetic data
- **Beautiful UI**: Dark/green theme with Streamlit
- **Predictions**: Real-time carbon emission predictions
- **Visualizations**: Gauge meter, comparison charts
- **Tips**: Suggestions to reduce emissions
- **History**: Track previous predictions
- **Export**: PDF report generation

## Installation

1. Clone or download the project.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Train the model (optional, already trained):
   ```
   python train_model.py
   ```

## Usage

Run the app:
```
streamlit run app.py
```

Open your browser to `http://localhost:8501`

## Project Structure

```
carbon_emission_prediction_app/
├── app.py                 # Main Streamlit app
├── train_model.py         # Model training script
├── requirements.txt       # Dependencies
├── README.md              # This file
├── model/
│   └── model.pkl          # Trained model
├── utils/
│   └── preprocess.py      # Input preprocessing
└── assets/                # Static assets (optional)
```

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- Plotly
- FPDF

## Contributing

Feel free to fork and contribute!

## License

MIT License
