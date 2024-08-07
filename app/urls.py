from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register/', csrf_exempt(RegisterView.as_view()), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('symbols/', SymbolListView.as_view(), name='symbol-list'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscription-list'),
    path('device-tokens/', DeviceTokenView.as_view(), name='device-token-list'),

]
