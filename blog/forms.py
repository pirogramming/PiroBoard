from django import forms
from .models import Comment, Post
from users.models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('group_name', 'group_info', 'group_img', 'group_open_status')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'photo',)
