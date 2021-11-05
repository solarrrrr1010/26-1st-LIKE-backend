from django.views       import View
from django.http        import JsonResponse
from products.models    import MainCategory, SubCategory, Product, ProductOption

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

        products = [{
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
        } for po in ProductOption.objects.all()]

        results = [product for product in products 
                                if product["main_category"] == category 
                                    and product["color"]    == color 
                                    and product["size"]     == size]

        return JsonResponse({'results' : results}, status = 200)
