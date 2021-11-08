from django.urls    import path
from products.views import ProductListView, DetailView

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view()),
    path('/details/<int:details_id>', DetailView.as_view()),
]