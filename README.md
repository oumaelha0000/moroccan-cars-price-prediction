# Moroccan Cars Price Prediction

This project is a Streamlit web application that predicts the price of a used car in Morocco using a trained machine learning model.

## Features

- User-friendly interface built with Streamlit
- Car details inputs such as brand, model, year, mileage, fuel type, and condition
- Automatic preprocessing using a saved scaler
- Prediction using a trained Random Forest model
- Price displayed in Moroccan Dirham (MAD)

## Project structure

- `app.py` — Streamlit application
- `random_forest_model.pkl` — trained ML model
- `scaler.pkl` — feature scaler
- `columns.pkl` — model input columns
- `image.png` — background image

## Requirements

Install the dependencies:

```bash
pip install streamlit pandas joblib
```

## Run the app

```bash
streamlit run app.py
```

Then open the local URL displayed in the terminal, typically:

```text
http://localhost:8501
```

## Example

The app asks for information such as:

- localised area
- model year
- brand and model
- gearbox type
- fuel type
- mileage
- number of doors
- fiscal power
- origin
- first owner status
- vehicle condition

It then estimates the vehicle price in MAD.

## License

This project is intended for educational and personal use.
