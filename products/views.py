from django.views           import View
from django.http            import JsonResponse
from django.db.models       import Sum
from django.core.exceptions import MultipleObjectsReturned
from django.core.cache      import cache

from products.models        import MainCategory, SubCategory, Product, ProductOption
from core.utils             import measure_run_time

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
    @measure_run_time
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
        ordering = request.GET.get('sort', '-id')
        
        # redis cache
        if not cache.get('products'):
            results = [{
                "product"             : product.id,
                "serial"              : product.serial,
                "title"               : product.title,
                "sub_title"           : product.sub_title,
                "price"               : float(product.price),
                "thumbnail_image_url" : product.thumbnail_image_url,
                "eco_friendly"        : product.eco_friendly,
                "color"               : product.productoption_set.first().color.name,
                "size"                : [po.size.type for po in product.productoption_set.all()],
                "quantity"            : product.productoption_set.values('quantity').aggregate(Sum('quantity'))['quantity__sum'],
                "sub_category"        : product.sub_category.name,  
                "main_category"       : product.sub_category.main_category.name
            } for product in Product.objects.filter(**filter_set).order_by(ordering)]
            data = cache.set('products', results)
        data=cache.get('products')
        return JsonResponse({'results' : data}, status = 200)

class DetailView(View):
    def get(self, request, details_id):
        try:
            product   = Product.objects.get(id=details_id)
            images    = [image['url'] for image in product.productimage_set.filter(
                product_id=product.id).values('url')]
            po_sort   = ProductOption.objects.all().order_by('size_id')
            size_quan = [{
                "sizeName" : po.size.type, "quantity" : po.quantity
                } for po in po_sort.filter(product_id=product.id)]
            results   = {
                "product_id"        : product.id,
                "price"             : product.price,
                "product_images"    : images,
                "sub_title"         : product.sub_title,
                "title"             : product.title,
                "price"             : int(product.price),
                "eco_friendly"      : product.eco_friendly,
                "size_quan"         : size_quan,
                "description_title" : product.description_title,
                "description"       : product.description,
                "current_color"     : product.current_color,
                "serial"            : product.serial
            }

            return JsonResponse({'results' : results}, status = 200)
            
        except Product.DoesNotExist:
            return JsonResponse({"message" : "Product does not exist"}, status=400)        

        except MultipleObjectsReturned:
            return JsonResponse({"message" : "MultipleObjectsReturned"}, status=400)    

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=401)        