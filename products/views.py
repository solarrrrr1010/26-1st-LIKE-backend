from django.views       import View
from django.http        import JsonResponse
from products.models    import MainCategory, SubCategory 

class CategoryListView(View):
    def get(self, request):
        results = [
            {
                "id"   : main.id,
                "name" : main.name,
                "sub_categories" : [
                    {
                        "id"   : sub.id,
                        "name" : sub.name,
                    }
                    for sub in SubCategory.objects.filter(main_category_id=main.id)
                ]
            }
            for main in MainCategory.objects.all() 
        ]
        return JsonResponse({'results' : results}, status = 200)