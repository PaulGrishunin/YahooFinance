from django.conf import settings
from django.urls import path, include
from .views import (
    PricesListView,

)
from app import views

app_name = 'app'

urlpatterns = [
    # path('create/<name>', views.create_prices),            #collect data
    path('', views.hello),
    path('prices/<str:name>', PricesListView.as_view(), name='prices_list'),


]