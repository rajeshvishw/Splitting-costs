from django.urls import path
from .views import UserAPIView, ExpenseAPIView, BalanceAPIView

urlpatterns = [
    path('api/users/', UserAPIView.as_view()),
    path('api/users/<uuid:user_id>/', UserAPIView.as_view()),
    path('api/expenses/', ExpenseAPIView.as_view()),
    path('api/expenses/<uuid:expense_id>/', ExpenseAPIView.as_view()),
    path('api/users/<uuid:user_id>/balances/', BalanceAPIView.as_view()),
]
