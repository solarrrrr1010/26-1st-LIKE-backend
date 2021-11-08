import json

from django.http        import JsonResponse
from django.views       import View

from orders.models      import ShoppingCart
from products.models    import ProductOption

class CartListView(View):
    # @login_required
    def get(self, request):
        results = [{
            "id"                  : cart.id,
            "product_id"          : cart.product_option.product.id,
            "user_id"             : cart.user_id,
            "product_title"       : cart.product_option.product.title,
            "serial"              : cart.product_option.product.serial,
            "size"                : cart.product_option.size.type,
            "quantity"            : cart.quantity,
            "price"               : float(cart.product_option.product.price * cart.quantity),
            "thumbnail_image_url" : cart.product_option.product.thumbnail_image_url,
		} for cart in ShoppingCart.objects.all()]
        
        return JsonResponse({"results" : results}, status=200)

    # @login_required
    def post(self, request):
        data = json.loads(request.body)

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