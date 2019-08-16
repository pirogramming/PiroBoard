from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from blog_manager.forms import GroupForm
from users.models import Group, Profile, GroupMember


def group_manage(request, pk):
    profile = Profile.objects.get(user=request.user)

    group = Group.objects.get(id=pk)
    members = Profile.objects.filter(group=group)

    ctx = {
        'pk': pk,
        'group': group,
        'members': members,
    }

    return render(request, 'blog_manager/group_manage.html', ctx)


def group_info_update(request, pk):
    group = Group.objects.get(id=pk)
    if request.method == 'POST':
        form = GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, '그룹 정보를 성공적으로 수정하였습니다.')
            return redirect("group_manage", pk)
    else:
        form = GroupForm(instance=group)
    return render(request, 'blog_manager/group_info_update.html', {'form': form})


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
