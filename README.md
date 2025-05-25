# WeatherWizard
WeatherWizard is an intelligent weather forecasting tool designed to clean and prepare real-world weather data. It predicts temperature, understands **natural language queries**, and provides users with up-to-date weather information. This project is showcased within a [Jupyter Notebook presentation](https://github.com/ClassicCollins/WeatherWizard/blob/classic/presentation.ipynb)

## Features
- [**Natural Language Processing (NLP)**](https://github.com/ClassicCollins/WeatherWizard/blob/classic/nlp.py) for weather queries
- [**Machine Learning Models**](https://github.com/ClassicCollins/WeatherWizard/blob/classic/ml_model.py) for temperature forecasting
- **Interactive Widgets** for easy input in Jupyter Notebooks
- **Exploratory Data Analysis (EDA)** for deeper insights
- **Multi-city weather support**

## Installation

Ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```
If using Anaconda, run:
```bash
conda install --file requirements.txt
```
Usage
1. Import the necessary modules
2. Interactive Weather Query in Jupyter Notebook

Enhancements & Future Improvements
- World cities database as a fallback if spaCy misses city detection
- Hourly temperature predictions for more granular forecasting
- Cached results to reduce API calls and improve performance
- Handling vague phrases like "this weekend"
- AI-powered misspelling corrections (e.g., "Lonodn" → "London")
- [Agentic AI (LangChain Agents)](https://github.com/ClassicCollins/WeatherWizard/blob/classic/agentic_ai.py) to call weather functions dynamically and improve context

License
This project is licensed under the [MIT License](https://github.com/ClassicCollins/WeatherWizard/blob/classic/LICENSE)

WeatherWizard—making weather forecasting smarter!

Acknoledgement
**Python**
**openweatherAPI**
