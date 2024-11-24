import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd
from sklearn.linear_model import LinearRegression
from PIL import Image, ImageTk


API_KEY = 'YOUR_API_KEY'
STOCK_SYMBOLS = ['TATAMOTORS.BSE', 'ADANIPORTS.BSE']

def fetch_historical_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact"
    response = requests.get(url)
    data = response.json()
    try:
        time_series = data['Time Series (Daily)']
        df = pd.DataFrame.from_dict(time_series, orient='index', dtype=float)
        df = df.reset_index().rename(columns={'index': 'date'})
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        return df[['date', '4. close']]
    except KeyError:
        print(f"Error fetching data for {symbol}: {data}")
        return None

def predict_future_price(df):
    df['days'] = (df['date'] - df['date'].min()).dt.days
    model = LinearRegression()
    model.fit(df[['days']], df['4. close'])
    future_days = 30
    future_date = df['days'].max() + future_days
    predicted_price = model.predict([[future_date]])[0]
    return predicted_price

def display_stock_prices():
    prices = []
    for symbol in STOCK_SYMBOLS:
        df = fetch_historical_data(symbol)
        if df is not None:
            current_price = df['4. close'].iloc[-1]
            future_price = predict_future_price(df)
            prices.append(f"{symbol}: \nCurrent Price: {current_price:.2f} INR, \nPredicted Price (30 days): {future_price:.2f} INR")
        else:
            prices.append(f"{symbol}: Data not available")
    price_label.config(text=f"Current and Predicted Stock Prices:\n{'\n'.join(prices)}")


root = tk.Tk()
root.title("Stock Price Display")
root.geometry("400x400")


canvas = tk.Canvas(root, width=400, height=400)
canvas.pack(fill="both", expand=True)


bg_image = ImageTk.PhotoImage(Image.open("1724738547-8169.png"))
canvas.create_image(0, 0, image=bg_image, anchor="nw")


price_label = tk.Label(root, text="Current and Predicted Stock Prices: ", font=("Helvetica", 16), bg="lightblue", wraplength=380, justify="left")
price_window = canvas.create_window(10, 100, anchor="nw", window=price_label)


fetch_button = tk.Button(root, text="Fetch Stock Prices", command=display_stock_prices, font=("Helvetica", 14), bg="green", fg="white")
button_window = canvas.create_window(120, 300, anchor="nw", window=fetch_button)


root.mainloop()
