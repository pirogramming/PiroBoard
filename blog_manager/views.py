from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from users.models import Group, Profile, GroupMember


def group_manage(request, pk):
    profile = Profile.objects.get(user=request.user)

    group = Group.objects.get(id=pk)
    members = Profile.objects.filter(group=group)

    ctx = {
        'pk':pk,
        'group': group,
        'members': members,
    }

    return render(request, 'blog_manager/group_manage.html', ctx)


def group_info_update(request, pk):
    return HttpResponse('그룹 업데이트를 해줄 친절한 누군가를 찾아요')

def group_member_manage(request, pk):
    ctx = {
        'pk': pk,
    }
    return render(request, 'blog_manager/manage_group_member.html', ctx)

def invite_member(request, pk):
    ctx = {
        'pk': pk,
    }
    return render(request, 'blog_manager/invite_member.html', ctx)

def manage_requests(request, pk):
    ctx = {
        'pk': pk,
    }
    return render(request, 'blog_manager/manage_requests.html', ctx)
