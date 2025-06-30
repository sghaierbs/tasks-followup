# mixins.py

from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm

class CommentableObjectMixin:
    comment_form_class = CommentForm

    def get_comments(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return Comment.objects.filter(content_type=content_type, object_id=obj.id).order_by('-created_at')

    def get_comment_form(self):
        return self.comment_form_class()

    def save_comment(self, request, obj):
        form = self.comment_form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.content_object = obj
            comment.save()
