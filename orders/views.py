import json

from django.http        import JsonResponse
from django.views       import View

from orders.models      import ShoppingCart
from products.models    import ProductOption
from core.utils         import login_required

class CartListView(View):
    @login_required
    def get(self, request):
        results = [{
            "cart_id"             : cart.id,
            "product_id"          : cart.product_option.product.id,
            "user_id"             : cart.user_id,
            "product_title"       : cart.product_option.product.title,
            "serial"              : cart.product_option.product.serial,
            "size"                : cart.product_option.size.type,
            "quantity"            : cart.quantity,
            "price"               : float(cart.product_option.product.price * cart.quantity),
            "thumbnail_image_url" : cart.product_option.product.thumbnail_image_url,
		} for cart in ShoppingCart.objects.filter(user_id=request.user.id)
                                            .select_related('product_option__product')
                                            .select_related('product_option__size')]
        
        return JsonResponse({"results" : results}, status=200)

    @login_required
    def post(self, request):
        data = json.loads(request.body)

        print('data :',data)

        try:
            product_option = ProductOption.objects.get(product_id=data['product_id'], size__type=data['size'])
            
            ShoppingCart.objects.create(
                user_id           = request.user.id,
                product_option_id = product_option.id,
                quantity          = data['quantity'],
            )
            return JsonResponse({"message" : "SUCCESS"}, status=201)
            
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except ProductOption.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST_PRODUCT_OPTION"}, status=400)


    @login_required
    def delete(self, request):
        data = json.loads(request.body)

        try:
            ShoppingCart.objects.get(id=data['cart_id']).delete()

            return JsonResponse({"message" : "SUCCESS"}, status=204)
            
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except ProductOption.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST_PRODUCT_OPTION"}, status=400)