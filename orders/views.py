from json

from django.views import View
from django.http  import JsonResponse

class OrderListView(View):
    def get(self, request):
        return JsonResponse({"results" : "results"}, status=200)
        
    def post(self, request):
        return JsonResponse({"message" : "SUCCESS"}, status=201)
        