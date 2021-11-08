import json

from django.views import View
from django.http  import JsonResponse

from orders.models   import Order
from products.models import ProductOption

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
            data = json.loads(request.body)

            # list로 어떻게 들어오는지 확인해보기
            print(data)
            
            product_option = ProductOption.objects.get(product_id=data['product_id'], size__type=data['size'])
            Order.objects.create(
                user_id           = request.user.id,
                product_option_id = product_option.id,
                quantity          = data['quantity'],
                price             = data['price'],
                order_number      = '2021-01-10-0001',
                order_status_id   = '2',                # 주문완료
                shipping_address  = data['address'],
            )
            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)