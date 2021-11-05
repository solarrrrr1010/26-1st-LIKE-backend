from django.views       import View
from django.http        import JsonResponse
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

class ProductAllListView(View):
    def get(self, request):
        results = [{
            "id"                  : product.id,
            "serial"              : product.serial,
            "title"               : product.title,
            "sub_title"           : product.sub_title,
            "price"               : product.price,
            "thumbnail_image_url" : product.thumbnail_image_url,
            "eco_friendly"        : product.eco_friendly,
            "sub_category"        : product.sub_cateory_id
        } for product in Product.objects.all()]
        return JsonResponse({'results' : results}, status = 200)

class ProductListView(View):
    def get(self, request, category):
        results = [{
            "id"                  : product.id,
            "serial"              : product.serial,
            "title"               : product.title,
            "sub_title"           : product.sub_title,
            "price"               : product.price,
            "thumbnail_image_url" : product.thumbnail_image_url,
            "eco_friendly"        : product.eco_friendly
        } for product in Product.objects.filter(sub_category_id=category)]
        return JsonResponse({'results' : results}, status = 200)
