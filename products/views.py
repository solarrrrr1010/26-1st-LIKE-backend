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
        main_category = request.GET.get('category', None)
        colors        = request.GET.getlist('color')
        sizes         = request.GET.getlist('size')
        sort          = request.GET.get('sort', '-id')
        
        condition = Q()
        ordering  = f'product__{sort}'

        if main_category:
            condition &= Q(product__sub_category__main_category__name=main_category) 
        if colors:
            [condition.add(Q(color__name=color), Q.OR) for color in colors]
        if sizes:
            [condition.add(Q(size__type=size), Q.OR) for size in sizes]

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
        } for po in ProductOption.objects.filter(condition).order_by(ordering)]

        return JsonResponse({'results' : results}, status = 200)

class ProductGroupListView(View):
    def get(self, request, sub_category_id):
        colors = request.GET.getlist('color')
        sizes  = request.GET.getlist('size')
        sort   = request.GET.get('sort', '-id')
        
        condition = Q()
        ordering = f'product__{sort}'

        if sub_category_id:
            condition &= Q(product__sub_category__id=sub_category_id) 
        if colors:
            [condition.add(Q(color__name=color), Q.OR) for color in colors]
        if sizes:
            [condition.add(Q(size__type=size), Q.OR) for size in sizes]

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
        } for po in ProductOption.objects.filter(condition).order_by(ordering)]

        return JsonResponse({'results' : results}, status = 200)