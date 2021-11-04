from django.urls    import path
from products.views import (
    ProductListView, 
    # ProductDetailView, 
)

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view()),
    # path('/<int:product_id>', ProductDetailView.as_view()),
    # path('/<int:main_id>' , ProductTypeView.as_view()),
    # path('/<int:main_id>/<int:sub_id>' , ProductView.as_view()),
]