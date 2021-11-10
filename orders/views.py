import json
import uuid

from django.views           import View
from django.http            import JsonResponse
from json.decoder           import JSONDecodeError
from django.core.exceptions import MultipleObjectsReturned

from orders.models          import Order, ShoppingCart
from products.models        import ProductOption
from core.enums             import OrderStatus
from core.utils             import login_required 

class OrderListView(View):
    @login_required
    def get(self, request):
        results = [{
            "order_id"            : order.id,
            "order_number"        : order.order_number,
            "status"              : order.order_status.name,
            "shipping_address"    : order.shipping_address,
            "product_id"          : order.product_option.product.id,
            "user_id"             : order.user_id,
            "user_name"           : order.user.name,
            "user_email"          : order.user.email,
            "user_phone_number"   : order.user.phone_number, 
            "product_title"       : order.product_option.product.title,
            "serial"              : order.product_option.product.serial,
            "size"                : order.product_option.size.type,
            "quantity"            : order.quantity,
            "price"               : order.price,
            "thumbnail_image_url" : order.product_option.product.thumbnail_image_url,
            "created_at"          : order.created_at
        } for order in Order.objects.filter(user_id=request.user.id)\
                                    .select_related('product_option__product', 'product_option__size', 'order_status', 'user')]

        return JsonResponse({"results" : results}, status=200)
        
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            order_number = uuid.uuid4()
            
            for order in data['order']:
                product_option = ProductOption.objects.get(product_id=order['product_id'], size__type=order['size'])

                if order['quantity'] < 1 or order['quantity'] > product_option.quantity:
                    return JsonResponse({"message" : "INVALID_QUANTITY"}, status=400) 

                Order.objects.create(
                    user_id           = request.user.id,
                    product_option_id = product_option.id,
                    quantity          = order['quantity'],
                    price             = order['price'],
                    order_number      = order_number,
                    order_status_id   = OrderStatus.Completed.value,
                )
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        
        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except MultipleObjectsReturned:
            return JsonResponse({"message" : "MULTIPLE_OBJECTS_RETURNED"}, status=400)
        except ProductOption.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST_PRODUCT_OPTION"}, status=400)

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
		} for cart in ShoppingCart.objects.filter(user_id=request.user.id)\
                                          .select_related('product_option__product','product_option__size')]
        
        return JsonResponse({"results" : results}, status=200)

    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_option = ProductOption.objects.get(product_id=data['product_id'], size__type=data['size'])
            
            if data['quantity'] < 1 or data['quantity'] > product_option.quantity:
                return JsonResponse({"message" : "INVALID_QUANTITY"}, status=400)

            ShoppingCart.objects.create(
                user_id           = request.user.id,
                product_option_id = product_option.id,
                quantity          = data['quantity'],
            )
            return JsonResponse({"message" : "SUCCESS"}, status=201)
            
        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except MultipleObjectsReturned:
            return JsonResponse({"message" : "MULTIPLE_OBJECTS_RETURNED"}, status=400)
        except ProductOption.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST_PRODUCT_OPTION"}, status=400)

    @login_required
    def delete(self, request):
        try:
            data = json.loads(request.body)
            ShoppingCart.objects.get(id=data['cart_id']).delete()

            return JsonResponse({"message" : "SUCCESS"}, status=200)

        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except ProductOption.DoesNotExist:
            return JsonResponse({"message": "DOES_NOT_EXIST_PRODUCT_OPTION"}, status=400)