from django import forms

from users.models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('group_name', 'group_info', 'group_img')