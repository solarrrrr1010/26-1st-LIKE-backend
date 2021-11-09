import jwt

from django.conf    import settings
from django.http    import JsonResponse
from django.db      import connection, reset_queries

from users.models   import User

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            data = jwt.decode(access_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            request.user = User.objects.get(id=data['id'])
                        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401)            

        except User.DoesNotExist:
            return JsonResponse({'message' : 'UNKNOWN_USER'}, status = 401)

        return func(self, request, *args, **kwargs)

    return wrapper

def count_queries(func):
    def wrapper(self, request):
        try:
            settings.DEBUG = True   
            func(self, request)
            print(f'query performance count : {len(connection.queries)}')
    
        finally:
            settings.DEBUG = False
            reset_queries()
        return func(self, request)
    return wrapper