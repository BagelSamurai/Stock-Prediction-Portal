from django.urls import path, include


from .views import StockPredictionAPIView

urlpatterns = [
    path('predict/', StockPredictionAPIView.as_view(), name='stock_prediction'),
]