import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

# Generate synthetic data
np.random.seed(42)
n_samples = 1000

fuel_consumption = np.random.uniform(5, 20, n_samples)  # liters/100km
vehicle_types = np.random.choice(['car', 'truck', 'bus'], n_samples)
distance = np.random.uniform(10, 500, n_samples)  # km
engine_size = np.random.uniform(1000, 5000, n_samples)  # cc
country_factor = np.random.uniform(1, 5, n_samples)  # emission factor

# Simulate emissions: some formula
emissions = (fuel_consumption * 2.3 + engine_size / 1000 + country_factor * 10 + np.random.normal(0, 5, n_samples))

data = pd.DataFrame({
    'fuel_consumption': fuel_consumption,
    'vehicle_type': vehicle_types,
    'distance': distance,
    'engine_size': engine_size,
    'country_factor': country_factor,
    'emissions': emissions
})

# Features and target
X = data[['fuel_consumption', 'vehicle_type', 'distance', 'engine_size', 'country_factor']]
y = data['emissions']

# Preprocessing: OneHot for vehicle_type
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), ['vehicle_type'])
    ],
    remainder='passthrough'
)

# Pipeline
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

# Save model
with open('carbon_emission_prediction_app/model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved as model.pkl")
