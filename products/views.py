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
        category = request.GET.get('category', None)
        color    = request.GET.get('color', None)
        size     = request.GET.get('size', None)

        condition = Q()

        if category:
            condition.add(Q(product__sub_category__main_category__name=category), Q.AND)
        if color:
            condition.add(Q(color__name=color), Q.AND)
        if size:
            condition.add(Q(size__name=category), Q.AND)


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
            "main_category"       : po.product.sub_category.main_category.name
        } for po in ProductOption.objects.filter(condition)]

        return JsonResponse({'results' : results}, status = 200)
