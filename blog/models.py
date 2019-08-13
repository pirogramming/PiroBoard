from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    photo = ProcessedImageField(blank=True,
                                processors=[Thumbnail(300, 300)],
                                format='JPEG',
                                options={'quality': 60})
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
