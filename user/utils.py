import jwt
from datetime           import datetime, timedelta

from django.http        import JsonResponse

from westagram.settings import SECRET_KEY
from .models            import User

def encode_jwt(user_id):
    token = jwt.encode(
        {'user_id':user_id, 
        'exp':datetime.utcnow() + timedelta(days=3)}, 
        SECRET_KEY, 
        algorithm='HS256'
    )
    return token

def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token == None:
            return JsonResponse({'error':'Enter the token'}, status=401)
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
            if User.objects.get(id=payload['user_id']):
                signed_user = User.objects.get(id=payload['user_id'])
                request.user = signed_user  # request에 user 속성으로 넣어서 보낸다.
                return func(self, request, *args, **kwargs)

        except jwt.InvalidSignatureError:
            return JsonResponse({'error':'Invalid token'}, status=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error':'Expried Signature'})
        except jwt.DecodeError:
            return JsonResponse({'error':'Invalid token'}, status=401)
    return wrapper