from django.shortcuts import render

# Create your views here.
from users.models import Group, Profile, GroupMember


def group_manage(request, pk):
    profile = Profile.objects.get(user=request.user)

    group = Group.objects.get(id=pk)
    members = Profile.objects.filter(group=group)

    ctx = {
        'group': group,
        'members': members,
    }
    return render(request, 'blog_manager/group_manage.html', ctx)
