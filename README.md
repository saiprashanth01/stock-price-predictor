Stock Price Predictor
Overview
Stock Price Predictor is a web application built with Flask that allows users to predict the future prices of stocks listed on the BSE (Bombay Stock Exchange) and NSE (National Stock Exchange) in India. Utilizing historical stock data and a linear regression model, the app predicts the stock price for the next day, 100 days, and 200 days. The predictions and current stock prices are displayed on an interactive, visually appealing web interface.

Features
Stock Price Prediction: Predict stock prices for 1 day, 100 days, and 200 days into the future.
Interactive Plots: View interactive graphs of the stock prices for 100 days before and after today.
Dynamic Stock Ticker Input: Enter a stock ticker symbol and get real-time predictions and data visualizations.
User-Friendly Interface: Clean and intuitive interface with background images and tooltips for data points on the graphs.
Responsive Design: Mobile-friendly layout ensuring a seamless experience across devices.
Technology Stack
Backend: Flask
Data Retrieval: yFinance
Machine Learning: Scikit-learn (Linear Regression)
Data Visualization: Matplotlib, mpld3
Frontend: HTML, CSS, JavaScript
Setup and Installation
Clone the repository:

sh
Copy code
git clone https://github.com/yourusername/stock-price-predictor.git
cd stock-price-predictor
Install the required packages:

sh
Copy code
pip install -r requirements.txt
Run the application:

sh
Copy code
python app.py
Open your browser and navigate to http://127.0.0.1:5000/.

File Structure
css
Copy code
stock-price-predictor/
│
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── img/
│       └── img.png
│
├── templates/
│   └── index.html
│
├── app.py
├── requirements.txt
└── README.md
Usage
Enter Stock Details: Select the exchange (BSE or NSE) and enter the stock ticker symbol.
Get Predictions: Click on the "Predict" button to get the current price and predicted prices.
View Graphs: Scroll down to view interactive graphs for the stock prices.
Screenshots

Main page showing the form to enter stock details.


Page displaying predicted prices and interactive graphs.

Contributing
Contributions are welcome! If you have any suggestions or improvements, feel free to create a pull request or open an issue.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
