<a id="readme-top"></a>
# WeatherWizard
WeatherWizard is an intelligent weather forecasting tool designed to clean and prepare real-world weather data. It predicts temperature, understands **natural language queries**, and provides users with up-to-date weather information. This project is summarized and showcased within a [Jupyter Notebook presentation](https://github.com/ClassicCollins/WeatherWizard/blob/classic/presentation.ipynb) . You can explore detailed coding by clicking on each feature's link below.

![Product Name Screen Shot][product-screenshot]

## Features
- [**Exploratory Data Analysis (EDA)**](https://github.com/ClassicCollins/WeatherWizard/blob/classic/eda.ipynb) for deeper insights
- [**Machine Learning Models**](https://github.com/ClassicCollins/WeatherWizard/blob/classic/ml_model.py) for temperature forecasting
- [**Natural Language Processing (NLP)**](https://github.com/ClassicCollins/WeatherWizard/blob/classic/nlp.py) for weather queries
- [**Agentic AI**](https://github.com/ClassicCollins/WeatherWizard/blob/classic/agentic_ai.py) enables deep contextual understanding of NLP-based weather queries.
- **Interactive Widgets** for easy input in Jupyter Notebooks. However, a fallback option is available if this does not display properly.
- **Multi-city weather support** features robust functions such as `get_weather_info` and `fetch_weather_data` which accept multiple cities as input.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- INSTALLATION -->
## Installation:
Creating a virtual environment is recommended:

```bash
python -m venv myenv
```
Activate it on Windows:

```bash
myenv\Scripts\activate
```
Activate it on macOS/Linux:

```bash
source myenv/bin/activate
```
Clone the repo (You can install the dependacies one by one or use requirements.txt):
```bash
git clone https://github.com/ClassicCollins/WeatherWizard.git
```
```bash
cd WeatherWizard
```

Ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```
If using Anaconda, run:
```bash
conda install --file requirements.txt
```
## Usage
1. Import the necessary modules
2. Enter a valid city and dates to download the weather data and forecast the temperature using trained model
3. Interactive Weather Query in Jupyter Notebook
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Suggested Enhancements & Future Improvements
- **World cities database** as a fallback if spaCy misses city detection
- **Hourly temperature predictions** for more granular forecasting
- **Cached results** to reduce API calls and improve performance
- **Handling vague phrases** like "this weekend"
- **AI-powered** misspelling corrections (e.g., "Lonodn" → "London")
- More robust [Agentic AI (LangChain Agents)](https://github.com/ClassicCollins/WeatherWizard/blob/classic/agentic_ai.py) to call weather functions dynamically and improve context and user experience

<!-- LICENCE -->
## License
* `MIT` This project is licensed under the [MIT License](https://github.com/ClassicCollins/WeatherWizard/blob/classic/LICENSE)
  
<p align="right">(<a href="#readme-top">back to top</a>)</p>
WeatherWizard—making weather forecasting smarter!
  - @ClassicCollins 2025

## Acknowledgement
- **Python**
- **[Open-meteo API](https://open-meteo.com/)**

<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]:screenshot.png
