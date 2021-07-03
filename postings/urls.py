from django.urls    import path

from postings.views import LikeView, WriteView, PostingDeleteView, PostingsView, CommentsView, CommentDeleteView

urlpatterns = [
    path('/write', WriteView.as_view()),
    path('/<int:posting_id>/delete', PostingDeleteView.as_view()),
    path('/postings', PostingsView.as_view()),
    path('/<int:posting_id>/comments', CommentsView.as_view()),
    path('/comments/<int:comment_id>', CommentDeleteView.as_view()),
    path('/<int:posting_id>/like', LikeView.as_view()),
    ]