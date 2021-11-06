from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Q
from products.models    import MainCategory, SubCategory, ProductOption

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
            'category' : "product__sub_category__main_category__name__in",  
            'color'    : "color__name__in",
            'size'     : "size__type__in",
        }
        filter_set = {
            filter_field.get(key) : value for (key, value) in dict(request.GET).items() if filter_field.get(key)
        }

        sort     = request.GET.get('sort', '-id')
        ordering = f'product__{sort}'
        if '-' in sort:
            ordering = f"-{ordering.replace('-','')}" 

        results = [{
            "product"             : po.product_id,
            "color"               : po.color.name,
            "size"                : po.size.type,
            "serial"              : po.product.serial,
            "title"               : po.product.title,
            "sub_title"           : po.product.sub_title,
            "price"               : po.product.price,
            "thumbnail_image_url" : po.product.thumbnail_image_url,
            "eco_friendly"        : po.product.eco_friendly,
            "sub_category"        : po.product.sub_category.name,  
            "main_category"       : po.product.sub_category.main_category.name
        } for po in ProductOption.objects.filter(**filter_set).order_by(ordering)]

        return JsonResponse({'results' : results}, status = 200)

class ProductGroupListView(View):
    def get(self, request, sub_category_id):
        filter_field = {
            'color'    : "color__name__in",
            'size'     : "size__type__in",
        }
        filter_set = {
            filter_field.get(key) : value for (key, value) in dict(request.GET).items() if filter_field.get(key)
        }

        sort     = request.GET.get('sort', '-id')
        ordering = f'product__{sort}'
        if '-' in sort:
            ordering = f"-{ordering.replace('-','')}" 

        results = [{
            "product"             : po.product_id,
            "color"               : po.color.name,
            "size"                : po.size.type,
            "serial"              : po.product.serial,
            "title"               : po.product.title,
            "sub_title"           : po.product.sub_title,
            "price"               : po.product.price,
            "thumbnail_image_url" : po.product.thumbnail_image_url,
            "eco_friendly"        : po.product.eco_friendly,
            "sub_category"        : po.product.sub_category.name,  
            "main_category"       : po.product.sub_category.main_category.name
        } for po in ProductOption.objects.filter(product__sub_category__id=sub_category_id).filter(**filter_set).order_by(ordering)]

        return JsonResponse({'results' : results}, status = 200)