import pytest
from rest_framework.test import APIClient
from rest_framework import status

# Marks all tests in this module as Django DB tests
pytestmark = pytest.mark.django_db

class TestStockPredictionAPI:
    def test_predict_endpoint_success(self):
        """
        Tests a successful API call with a valid ticker.
        """
        client = APIClient()
        # Use a well-known ticker that is likely to have data
        response = client.post('/api/v1/predict/', {'ticker': 'AAPL'}, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'success'
        assert 'plot_final_img' in response.data
        assert 'r2Score' in response.data

    def test_predict_endpoint_invalid_ticker(self):
        """
        Tests an API call with a ticker that does not exist.
        """
        client = APIClient()
        # Use a fake ticker that yfinance won't find
        response = client.post('/api/v1/predict/', {'ticker': 'FAKETICKER123'}, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'error' in response.data
        assert response.data['error'] == 'No data found for the given ticker symbol.'

    def test_predict_endpoint_missing_ticker(self):
        """
        Tests an API call with missing data in the payload.
        """
        client = APIClient()
        response = client.post('/api/v1/predict/', {}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'ticker' in response.data
        assert 'This field is required.' in response.data['ticker']
