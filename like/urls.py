"""like URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from products.views import CategoryListView
from orders.views import CartListView, ReviewView, ReviewPostDeleteView

urlpatterns = [
    path('users', include('users.urls')),
    path('products', include('products.urls')),
    path('orders', include('orders.urls')),
    path('categories', CategoryListView.as_view()),
    path('carts', CartListView.as_view()),
    path('reviews/#<int:product_id>', ReviewView.as_view()), 
    path('reviews_post_delete', ReviewPostDeleteView.as_view())
]
