import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from sklearn.metrics import mean_squared_error, r2_score

from .utils import save_plot


class PredictionService:

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, '..', 'model', 'stock_prediction_model.keras')


    YEARS_OF_DATA = 10
    TRAIN_TEST_SPLIT = 0.70
    LOOK_BACK_DAYS = 100

    def __init__(self, ticker):
        self.ticker = ticker
        self.model = load_model(self.MODEL_PATH)
        self.df = self._fetch_data()
        self.scaler = MinMaxScaler(feature_range=(0, 1))

        self._predictions = None
        self._evaluation_metrics = None

    def _fetch_data(self):
        end = datetime.now()
        start = end - timedelta(days=365 * self.YEARS_OF_DATA)
        data = yf.download(self.ticker, start=start, end=end)
        return data.reset_index()

    def has_data(self):
        return not self.df.empty

    def _create_plot(self, filename_suffix, title, plots):
        plt.figure(figsize=(12, 6))
        for data, label in plots:
            plt.plot(data, label=label)

        plt.title(title)
        plt.xlabel('Time')
        plt.ylabel('Close Price (USD)')
        plt.legend()
        plt.grid(True)

        plot_path = f'{self.ticker}_{filename_suffix}.png'
        url_path = save_plot(plot_path)
        plt.close()
        return url_path

    def generate_plots(self):
        close_prices = self.df['Close']
        ma100 = close_prices.rolling(100).mean()
        ma200 = close_prices.rolling(200).mean()

        plot_img = self._create_plot('closing_price', f"Closing Price of {self.ticker}",
                                     [(close_prices, 'Closing Price')])

        plot_100dma_img = self._create_plot('100dma', f"100-Day MA vs. Closing Price",
                                            [(close_prices, 'Closing Price'), (ma100, '100-Day MA')])

        plot_200dma_img = self._create_plot('200dma', f"200-Day MA vs. Closing Price",
                                            [(close_prices, 'Closing Price'), (ma200, '200-Day MA')])

        return {
            'plot_img': plot_img,
            'plot_100dma_img': plot_100dma_img,
            'plot_200dma_img': plot_200dma_img
        }

    def get_predictions(self):
        if self._predictions is not None:
            return self._predictions

        close_df = pd.DataFrame(self.df['Close'])
        training_size = int(len(close_df) * self.TRAIN_TEST_SPLIT)
        data_training = close_df[:training_size]
        data_testing = close_df[training_size:]

        past_100_days = data_training.tail(self.LOOK_BACK_DAYS)
        final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
        input_data = self.scaler.fit_transform(final_df)

        x_test, y_test = [], []
        for i in range(self.LOOK_BACK_DAYS, len(input_data)):
            x_test.append(input_data[i - self.LOOK_BACK_DAYS:i])
            y_test.append(input_data[i, 0])
        x_test, y_test = np.array(x_test), np.array(y_test)

        y_predicted = self.model.predict(x_test)
        self.y_predicted_scaled_back = self.scaler.inverse_transform(y_predicted).flatten()
        self.y_test_scaled_back = self.scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()

        plot_final_img = self._create_plot('final_prediction', f"Prediction vs. Original for {self.ticker}", [
            (self.y_test_scaled_back, 'Original Price'),
            (self.y_predicted_scaled_back, 'Predicted Price')
        ])

        self._predictions = {'plot_final_img': plot_final_img}
        return self._predictions

    def evaluate_model(self):
        if self._predictions is None:
            self.get_predictions()

        mse = mean_squared_error(self.y_test_scaled_back, self.y_predicted_scaled_back)
        rmse = np.sqrt(mse)
        r2 = r2_score(self.y_test_scaled_back, self.y_predicted_scaled_back)

        self._evaluation_metrics = {'mse': mse, 'rmse': rmse, 'r2Score': r2}
        return self._evaluation_metrics
