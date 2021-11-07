from django.urls import path
from orders.views import CartListView
app_name = 'orders'
urlpatterns = [
    path('', CartListView.as_view()),
]