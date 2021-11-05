from django.urls    import path
from products.views import (
    ProductAllListView, 
    ProductListView, 
)

app_name = 'products'
urlpatterns = [
    path('', ProductAllListView.as_view()),
    path('/<int:category_id>', ProductListView.as_view()),
]