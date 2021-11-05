from django.db import models

class MainCategory(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'main_categories'


class SubCategory(models.Model):
    name          = models.CharField(max_length=100)
    main_category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sub_categories'


class Product(models.Model):
    sub_category        = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    serial              = models.CharField(max_length=200, unique=True)
    title               = models.CharField(max_length=100)
    sub_title           = models.CharField(max_length=100)
    price               = models.DecimalField(max_digits=9, decimal_places=2)
    thumbnail_image_url = models.CharField(max_length=2000, blank=True)
    eco_friendly        = models.BooleanField(default=False)
    current_color       = models.CharField(max_length=2000)
    description_title   = models.CharField(max_length=2000)
    description         = models.CharField(max_length=2000)

    class Meta:
        db_table = 'products'
    
class ProductOption(models.Model):
    product  = models.ForeignKey('Product', on_delete=models.CASCADE)
    color    = models.ForeignKey('Color', on_delete=models.CASCADE)
    size     = models.ForeignKey('Size', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    class Meta:
        db_table = 'product_options'

class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    url     = models.CharField(max_length=2000)

    class Meta:
        db_table = 'product_images'

class Size(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        db_table = 'sizes'

class Color(models.Model):
    name = models.CharField(max_length=2000)
    hex  = models.CharField(max_length=2000)

    class Meta:
        db_table = 'colors'

