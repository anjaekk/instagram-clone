from django.db               import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, TextField

from user.models import User

class Posting(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    image_url   = models.URLField()
    description = models.TextField()

    class Meta:
        db_table = 'postings'

class Comment(models.Model):
    posting         = models.ForeignKey(Posting, on_delete=models.CASCADE)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    comment_text    = TextField()
    parents_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'comments'


class Like(models.Model):
    posting = models.ForeignKey(Posting, on_delete=CASCADE)
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'