from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

from users.models import Group


class Post(models.Model):
    group = models.ForeignKey(Group, related_name='G_post', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_photo = ProcessedImageField(blank=True,
                                     format='JPEG',
                                     options={'quality': 100},
                                     null=True, )
    photo = ProcessedImageField(blank=True,
                                processors=[Thumbnail(300, 300)],
                                format='JPEG',
                                options={'quality': 60},
                                null=True, )
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    CATEGRORY_CHOICES = (
        ('음식', '음식'),
        ('취미', '취미'),
        ('인물', '인물'),
        ('etc', 'etc'),
        ('없음', '없음'),
    )
    category = models.CharField(max_length=10, choices=CATEGRORY_CHOICES, default='없음', )

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
