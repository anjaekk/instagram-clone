import json, re, bcrypt

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError

from user.models  import User
from user.utils   import encode_jwt

REGEX = {
    'email'    : '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    'password' : '[A-Za-z0-9@#$%^&+=]{8,}'
    }

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not re.match(REGEX['email'], email):
                return JsonResponse({'error':'INVALID_EMAIL'}, status=400)
            if not re.match(REGEX['password'], password):
                return JsonResponse({'error':'INVALID_PASSWORD'}, status=400)

            User.objects.create(
            email        = email,
            phone_number = data['phone_number'],
            name         = data['name'],
            nickname     = data['nickname'],
            password     = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            )

            user_id = User.objects.get(email=email).id
            return JsonResponse({'message':'SUCCESS', 'token':encode_jwt(user_id)}, status=201) 
        except KeyError:
            return JsonResponse({'error':'KEY_ERROR'}, status=400)
        except IntegrityError:
            return JsonResponse({'error':'DUPLICATE_ENTRY'}, status=400)

class SignInView(View):
    def post(self, request):
        data = json.loads(request.body)
        try: 
            email    = data['email']
            password = data['password'].encode('utf-8')
            user_id  = User.objects.get(email=email).id
            user_pw  = User.objects.get(email=email).password.encode('utf-8')

            if bcrypt.checkpw(password, user_pw):
                return JsonResponse({'message':'SUCCESS', 'token':encode_jwt(user_id)}, status=200) # 성공
            return JsonResponse({'error': 'INVALID_USER'}, status=401) # 비밀번호 일치 안할떄 

        except KeyError:
            return JsonResponse({'error': 'KEY_ERROR'}, status=400) # 이메일이나 비밀번호 입력 안했을 떄 
        except User.DoesNotExist:
            return JsonResponse({'error': 'INVALID_USER'}, status=401) #이메일이 없는 이메일 때 