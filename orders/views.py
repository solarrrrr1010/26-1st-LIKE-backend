from json

from django.views import View
from django.http  import JsonResponse

from orders.models import Order

class OrderListView(View):
    # @login_required
    def get(self, request):
        results = [{
            "id"                  : order.id,
            "order_number"        : order.order_number,
            "status"              : order.order_status.name,
            "shipping_address"    : order.shipping_address,
            "product_id"          : order.product_option.product.id,
            "user_id"             : order.user_id,
            "product_title"       : order.product_option.product.title,
            "serial"              : order.product_option.product.serial,
            "size"                : order.product_option.size.type,
            "quantity"            : order.quantity,
            "price"               : order.price,
            "thumbnail_image_url" : order.product_option.product.thumbnail_image_url,
        } for order in Order.objects.filter(user_id=request.user.id)]
        return JsonResponse({"results" : results}, status=200)
        
    # @login_required
    def post(self, request):
        try:

            return JsonResponse({"message" : "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        