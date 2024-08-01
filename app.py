from flask import Flask, render_template, request, jsonify
import yfinance as yf
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import mpld3

app = Flask(__name__)

def get_full_ticker(exchange, ticker):
    if exchange == "BSE":
        return f"{ticker}.BO"
    elif exchange == "NSE":
        return f"{ticker}.NS"
    return ticker

def predict_stock_price(full_ticker, days_ahead=1):
    try:
        stock = yf.Ticker(full_ticker)
        hist = stock.history(period="1y")
        hist['Date'] = hist.index

        hist['Days'] = (hist['Date'] - hist['Date'].min()).dt.days
        X = hist[['Days']]
        y = hist['Close']

        model = LinearRegression()
        model.fit(X, y)

        future_days = pd.DataFrame({'Days': [X['Days'].max() + days_ahead]})
        predicted_price = model.predict(future_days)[0]

        return predicted_price
    except Exception as e:
        print(f"Error predicting stock price: {e}")
        return None

def plot_stock_graph(full_ticker, days_ahead):
    try:
        stock = yf.Ticker(full_ticker)
        today = datetime.today()
        start_date = today - timedelta(days=100)
        end_date = today + timedelta(days=days_ahead)
        hist = stock.history(start=start_date, end=today)
        
        future_dates = pd.date_range(start=today + timedelta(days=1), periods=days_ahead)
        future_prices = [predict_stock_price(full_ticker, days_ahead=i) for i in range(1, days_ahead+1)]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(hist.index, hist['Close'], label='Close Price', color='blue')
        ax.plot(future_dates, future_prices, label='Predicted Price', color='green', linestyle='--')
        ax.set_title(f"{full_ticker} Stock Price (100 days before and {days_ahead} days after today)")
        ax.set_xlabel('Date')
        ax.set_ylabel('Close Price')
        ax.grid(True)
        ax.axvline(x=today, color='red', linestyle='--', label='Today')
        ax.fill_between(hist.index, hist['Close'], color='lightblue', alpha=0.1)
        ax.legend()

        labels = [f"{date}: ${price:.2f}" for date, price in zip(hist.index, hist['Close'])] + \
                 [f"{date}: ${price:.2f}" for date, price in zip(future_dates, future_prices)]
        tooltip = mpld3.plugins.PointLabelTooltip(ax.get_lines()[0], labels=labels)
        mpld3.plugins.connect(fig, tooltip)

        graph_html = mpld3.fig_to_html(fig)
        plt.close()

        return graph_html
    except Exception as e:
        print(f"Error plotting stock graph: {e}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    exchange = request.form['exchange']
    ticker = request.form['ticker']
    full_ticker = get_full_ticker(exchange, ticker)
    
    predicted_price_1_day = predict_stock_price(full_ticker, days_ahead=1)
    predicted_price_100_days = predict_stock_price(full_ticker, days_ahead=100)
    predicted_price_200_days = predict_stock_price(full_ticker, days_ahead=200)
    
    if predicted_price_1_day is None or predicted_price_100_days is None or predicted_price_200_days is None:
        return jsonify({"error": "Error predicting stock prices. Please check the ticker and try again."}), 500
    
    stock = yf.Ticker(full_ticker)
    current_price = stock.history(period='1d')['Close'][0]
    
    graph_html_1_day = plot_stock_graph(full_ticker, days_ahead=1)
    graph_html_100_days = plot_stock_graph(full_ticker, days_ahead=100)
    graph_html_200_days = plot_stock_graph(full_ticker, days_ahead=200)
    
    if not all([graph_html_1_day, graph_html_100_days, graph_html_200_days]):
        return jsonify({"error": "Error generating stock graphs. Please try again later."}), 500
    
    return render_template('index.html', ticker=ticker, current_price=current_price, 
                           predicted_price_1_day=predicted_price_1_day,
                           predicted_price_100_days=predicted_price_100_days,
                           predicted_price_200_days=predicted_price_200_days,
                           exchange=exchange, 
                           graph_html_1_day=graph_html_1_day, 
                           graph_html_100_days=graph_html_100_days, 
                           graph_html_200_days=graph_html_200_days)

if __name__ == '__main__':
    app.run(debug=True)
