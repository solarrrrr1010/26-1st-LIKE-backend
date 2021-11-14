import json
import uuid

from django.views            import View
from django.http             import JsonResponse
from json.decoder            import JSONDecodeError
from django.db.models        import Avg
from django.core.exceptions import MultipleObjectsReturned
     
from orders.models           import Order, ShoppingCart, ReviewImage, Review
from products.models         import ProductOption

from core.enums              import OrderStatus
from core.utils              import login_required, count_queries
from django.utils.dateformat import DateFormat

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
                
                # delete shopping cart data
                cart_id = order.get('cart_id', None)
                if cart_id:
                    ShoppingCart.objects.get(id=cart_id).delete()
                
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

class ReviewView(View):
    def get(self, request, product_id):
        reviews    = Review.objects.filter(product_option__product__id=product_id)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
              
        result = {
            "total_number_of_reviews": len(reviews),
            "average_rating": float(avg_rating) if avg_rating != None else 0,
            "reviews": [{
                "title"  : review.title,
                "rating" : float(review.rating) if review.rating != None else 0,
                "name"   : review.user.name,
                "date"   : DateFormat(review.created_at).format('Y.m.d'),
                "serial" : review.product_option.product.serial,
                "size"   : review.product_option.size.type,
                "text"   : review.text,
                "image"  : ReviewImage.objects.filter(review_id=review.id)[0].url
            } for review in reviews if ReviewImage.objects.filter(
                review_id=review.id)[0].url]
        }

        return JsonResponse({"result" : result}, status = 200)

class ReviewPostDeleteView(View):
    @login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            product_option_id = Order.objects.filter(
                user_id=request.user.id)[0].product_option_id
                
            Review.objects.create(
                title = data["title"],
                rating = data["rating"],
                text = data["text"],
                user_id = request.user.id,
                product_option_id = product_option_id
            )

            return JsonResponse({"message" : "SUCCESS"}, status=201)

        except IndexError:
            return JsonResponse({"message" : "구매 이력 없음"}, status=400) 
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400) 

    @login_required
    def delete(self, request):
        try:
            data = json.loads(request.body)
            Review.objects.get(id=data['review_id']).delete()
            return JsonResponse({"message" : "SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        except JSONDecodeError:
            return JsonResponse({"message" : "JSON_DECODE_ERROR"}, status=400)
        except Review.DoesNotExist:
            return JsonResponse({"message" : "DOES_NOT_EXIST_REVIEW"}, status=400)
        except MultipleObjectsReturned:
            return JsonResponse({"message" : "MULTIPLE_OBJECTS_RETURNED"}, status=400)