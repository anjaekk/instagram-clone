import json
from django.http   import JsonResponse
from django.views  import View
from django.utils  import timezone

from .models       import User, Posting, Comment, Like
from user.utils    import authorization

class WriteView(View):
    @authorization
    def post(self, request):
        try:
            data = json.loads(request.body)
            Posting.objects.create(
                user        = request.user,
                created_at  = timezone.localtime(),
                image_url   = data['image_url'],
                description = data['description'] 
                )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'error':'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'error':'INVALID_USER'}, status=400)
    
    @authorization
    def patch(self, request):
        try:
            data = json.loads(request.body)
            posting = Posting.objects.get(id = data['posting_id'])
            posting.description = data['description']
            posting.updated_at = timezone.localtime()
            posting.save()
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'error':'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'error':'INVALID_USER'}, status=400)

class PostingDeleteView(View):
    @authorization
    def post(self, request, posting_id):
        try: 
            if Posting.objects.filter(id = posting_id, user = request.user):
                Posting.objects.get(id=posting_id, user = request.user).delete()
                return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'error':'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'error':'INVALID_USER'}, status=400)

class PostingsView(View):
    @authorization
    def get(self, request):
        postings = Posting.objects.all()
        results = [{
            'user'        : posting.user,
            'created_at'  : posting.created_at,
            'image_url'   : posting.image_url,
            'description' : posting.description
        } for posting in postings]
        return JsonResponse({'results':results}, status=200)

class CommentsView(View):
    @authorization
    def post(self, request, posting_id):
        try:
            data = json.loads(request.body)
            posting = Posting.objects.get(id = posting_id)
            Comment.objects.create(
                user               = request.user,
                posting            = posting, 
                created_at         = timezone.localtime(),
                updated_at         = timezone.localtime(),
                comment_text       = data['comment_text'],
                parents_comment_id = data.get('parents_comment', None)
            )
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'error':'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'error':'INVALID_USER'}, status=400)

class LikeView(View):
    @authorization
    def post(self, request, posting_id):
        try:
            posting = Posting.objects.get(id=posting_id)
            if Like.objects.filter(posting=posting, user = request.user):
                Like.objects.get(posting = posting, user = request.user).delete()
                return JsonResponse({'message':'unlike'}, status=200)
            Like.objects.create(posting= posting, user = request.user)
            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'error':'KEY_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'error':'INVALID_USER'}, status=400)