import os
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from .serializers import StockPredictionSerializer
from .services import PredictionService

plt.switch_backend('AGG')


class StockPredictionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StockPredictionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        ticker = serializer.validated_data['ticker']

        try:
            service = PredictionService(ticker)

            if not service.has_data():
                return Response(
                    {"error": "No data found for the given ticker symbol."},
                    status=status.HTTP_404_NOT_FOUND
                )

            plots = service.generate_plots()
            predictions = service.get_predictions()
            metrics = service.evaluate_model()

            response_data = {
                'status': 'success',
                **plots,
                **predictions,
                **metrics
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except FileNotFoundError:
            return Response(
                {"error": "Prediction model not found. Please contact support."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )