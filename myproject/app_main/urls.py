from django.urls import path
from . import views

urlpatterns = [
    # Ścieżka do widoku
    path('stock/', views.fetch_stock_data, name='stock_data'),
    path('', views.home, name='home'),  # Strona główna
    path('introduction/', views.introduction, name='introduction'),  # Wprowadzenie
    path('stocks/', views.stocks, name='stocks'),  # Akcje
    path('technical-analysis/', views.technical_analysis, name='technical_analysis'),  # Analiza Techniczna
    path('real-estate/', views.real_estate, name='real_estate'),  # Nieruchomości
    path('login-panel/', views.login_panel, name='login_panel'),  # Panel logowania
]