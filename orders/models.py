from django.db import models

class ShoppingCart(models.Model):
    product_option = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    quantity       = models.IntegerField(default=0)
    class Meta:
        db_table = 'shopping_carts'
    
class Order(models.Model):
    product_option   = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)
    user             = models.ForeignKey('users.User', on_delete=models.CASCADE)
    order_status     = models.ForeignKey('OrderStatus', on_delete=models.CASCADE)
    order_number     = models.CharField(max_length=100, unique=True)
    shipping_address = models.CharField(max_length=2000)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

class OrderStatus(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'order_status'
        
class Review(models.Model):
    product_option = models.ForeignKey('products.ProductOption', on_delete=models.CASCADE)
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    title          = models.CharField(max_length=100)
    text           = models.CharField(max_length=2000)
    rating         = models.DecimalField(max_digits=1, decimal_places=1)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    deleted_at     = models.DateTimeField(null=True)

    class Meta:
        db_table = 'reviews'


class ReviewImage(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE)
    url    = models.CharField(max_length=2000)

    class Meta:
        db_table = 'review_images'

