from django.urls    import path
from products.views import ProductListView, ProductGroupListView 

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view()),
    path('/<int:sub_category_id>', ProductGroupListView.as_view()),
]