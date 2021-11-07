from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Sum

from products.models    import MainCategory, SubCategory, Product

class CategoryListView(View):
    def get(self, request):
        results = [{
            "id"   : main.id,
            "name" : main.name,
            "sub_categories" : [{
                "id"   : sub.id,
                "name" : sub.name,
            } for sub in SubCategory.objects.filter(main_category_id=main.id)]
        } for main in MainCategory.objects.all() ]
        return JsonResponse({'results' : results}, status = 200)

class ProductListView(View):
    def get(self, request):
        filter_field = {
            'main_category' : "sub_category__main_category__id__in",  
            'sub_category'  : "sub_category__id__in",
            'color'         : "productoption__color__name__in",
            'size'          : "productoption__size__type__in",
        }
        filter_set = {
            filter_field.get(key) : value for (key, value) in dict(request.GET).items() if filter_field.get(key)
        }

        sort     = request.GET.get('sort', '-id')
        ordering = f'{sort}'
        if '-' in sort:
            ordering = f"-{ordering.replace('-','')}" 
        
        results = [{
            "product"             : product.id,
            "serial"              : product.serial,
            "title"               : product.title,
            "sub_title"           : product.sub_title,
            "price"               : product.price,
            "thumbnail_image_url" : product.thumbnail_image_url,
            "eco_friendly"        : product.eco_friendly,
            "color"               : product.productoption_set.first().color.name,
            "size"                : [po.size.type for po in product.productoption_set.all()],
            "quantity"            : product.productoption_set.values('quantity').aggregate(Sum('quantity'))['quantity__sum'],
            "sub_category"        : product.sub_category.name,  
            "main_category"       : product.sub_category.main_category.name
        } for product in Product.objects.filter(**filter_set).order_by(ordering)]

        return JsonResponse({'results' : results}, status = 200)