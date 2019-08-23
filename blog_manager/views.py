import functools

from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from blog_manager.forms import GroupForm
from users.models import Group, Profile, GroupMember


def group_head_required(func):
    @functools.wraps(func)
    def wrapper(request, pk):
        group = get_object_or_404(Group, pk=pk)
        user = request.user.profile
        group_member = GroupMember.objects.get(group=group, person=user)
        if not group_member.is_manager or not group_member.is_member or group.group_head != request.user:
            return HttpResponse("그룹장 권한이 필요합니다.")
        return func(request, pk)

    return wrapper

def manager_required(func):
    @functools.wraps(func)
    def wrapper(request, pk):
        group = get_object_or_404(Group, pk=pk)
        user = request.user.profile

        group_member = GroupMember.objects.get(group=group, person=user)
        if not group_member.is_manager or not group_member.is_member:
            return HttpResponse("관리자 권한이 필요합니다.")
        return func(request, pk)

    return wrapper

# 그룹 관리자페이지 들어가기
@manager_required
def group_manage(request, pk):
    group = Group.objects.get(id=pk)
    members = [x.person for x in GroupMember.objects.filter(group=group, status='a')]

    ctx = {
        'pk': pk,
        'group': group,
        'members': members,
    }

    return render(request, 'blog_manager/group_manage.html', ctx)

# 그룹 수정
@manager_required
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

# 그룹장 매니저 권한 관리 페이지
@manager_required
def group_member_manage(request, pk):
    group = Group.objects.get(id=pk)
    users = [x.person for x in GroupMember.objects.filter(group=group, status='a', group_role='m')]

    head = group.group_head
    print(head)
    print(type(head))

    managers = [x.person for x in GroupMember.objects.filter(group=group, status='a', group_role='h')]

    ctx = {
        'pk': pk,
        'profiles': users,
        'head': head,
        "managers": managers,
    }

    return render(request, 'blog_manager/manage_group_member.html', ctx)

# 그룹장 넘기기
@group_head_required
def baton_touch(request, pk):
    group = Group.objects.get(id=pk)
    group.save()

    ctx = {
        'pk': pk,
    }

    if request.method == "POST":
        form = request.POST

        profile_name = form.get('user_p')
        user = User.objects.get(username=profile_name)

        group.group_head = user
        group.save()

    return redirect('group_member_manage', pk)

# 매니저 권한 뻇기
@group_head_required
def byebye_manager(request, pk):
    group = Group.objects.get(id=pk)
    group.save()

    ctx = {
        'pk': pk,
    }

    if request.method == "POST":
        form = request.POST

        profile_name = form.get('user_p')
        user = User.objects.get(username=profile_name)
        profile = Profile.objects.get(user=user)

        oldManager = GroupMember.objects.get(group=group, person=profile)
        oldManager.group_role = 'm'
        oldManager.save()

    return redirect('group_member_manage', pk)

# 매니저 권한 부여
@group_head_required
def welcome_manager(request, pk):
    group = Group.objects.get(id=pk)
    group.save()

    ctx = {
        'pk': pk,
    }

    if request.method == "POST":
        form = request.POST

        profile_name = form.get('user_p')
        user = User.objects.get(username=profile_name)
        profile = Profile.objects.get(user=user)

        oldManager = GroupMember.objects.get(group=group, person=profile)
        oldManager.group_role = 'h'
        oldManager.save()

    return redirect('group_member_manage', pk)

# 유저가 보낸 가입신청서를 거절하는 기능 차단차단
@manager_required
def user_request_refuse(request, pk):
    group = Group.objects.get(id=pk)
    group.save()

    if request.method == "POST":
        form = request.POST

        profile_name = form.get('user_p')
        user = User.objects.get(username=profile_name)
        profile = Profile.objects.get(user=user)

        membership = GroupMember.objects.get(group=group, person=profile)
        membership.status = 'r'
        membership.save()

    members = [x.person for x in GroupMember.objects.filter(group=group, status='a')]

    ctx = {
        'pk': pk,
        'group': group,
        'members': members,
    }

    return render(request, 'blog_manager/group_manage.html', ctx)


# 차단 유저 관리 페이지
@group_head_required
def chadan_member_manage(request, pk):
    group = Group.objects.get(id=pk)
    users = [x.person for x in GroupMember.objects.filter(group=group, status='r')]

    ctx = {
        'pk': pk,
        'profiles': users,
    }

    return render(request, 'blog_manager/chadan_manage.html', ctx)


# 차단 유저와의 GroupMember 삭제 -> 실행 후 초대하기/신청받기 가능
@group_head_required
def unblock(request, pk):
    group = Group.objects.get(id=pk)

    if request.method == "POST":
        form = request.POST

        profile_name = form.get('user_p')
        user = User.objects.get(username=profile_name)
        profile = Profile.objects.get(user=user)

        membership = GroupMember.objects.get(person=profile, group=group, status='r')
        membership.delete()

    return redirect('chadan_member_manage', pk)


# 그룹장이 유저 초대하는 페이지
@manager_required
def invite_member_page(request, pk):
    group = Group.objects.get(pk=pk)
    users = Profile.objects.exclude(group=group)

    q = request.GET.get('q', '')
    if q:
        users = users.filter(user__username__icontains=q)
    ctx = {
        'pk': pk,
        'profiles': users,
        'q': q,
    }
    return render(request, 'blog_manager/invite_member.html', ctx)

# 그룹장이 유저에게 초대를 요청하는 기능
@manager_required
def invite(request, pk):
    group = Group.objects.get(id=pk)
    group.save()

    if request.method == "POST":
        form = request.POST

        profile_name = form.get('user_p')
        user = User.objects.get(username=profile_name)
        profile = Profile.objects.get(user=user)

        GroupMember.objects.create(person=profile, group=group, status='g')

    return redirect('invite_member_page', pk)

# 그룹이 받은 가입신청 요청들/ 그룹이 보낸 가입신청 요청들 을 보여주는 페이지
@manager_required
def manage_requests(request, pk):
    group = Group.objects.get(id=pk)

    user_requests = [x.person for x in GroupMember.objects.filter(group=group, status='u')]
    group_requests = [x.person for x in GroupMember.objects.filter(group=group, status='g')]

    ctx = {
        'pk': pk,
    }

    if len(user_requests) > 0:
        ctx['user_requests'] = user_requests
        ctx['userRequest'] = True
        ctx['user_requests_count'] = len(user_requests)

    else:
        ctx['userRequest'] = False

    if len(group_requests) > 0:
        ctx['group_requests'] = group_requests
        ctx['groupRequest'] = True
        ctx['group_requests_count'] = len(group_requests)

    else:
        ctx['groupRequest'] = False

    return render(request, 'blog_manager/manage_requests.html', ctx)


# 코드가 좀 조잡하다. 좀 더 예뻤으면 좋겠다.
# 유저가 그룹에 보낸 '가입승인요청'을 수락하는 기능
# 새로 렌더링 하지 없게 수정하기
# 정말이냐고 알림창 띄우기
@manager_required
def user_request_accept(request, pk):
    if request.method == "POST":
        form = request.POST
        group = Group.objects.get(id=pk)
        group.save()

        profile_name = form.get('user_p')
        user = User.objects.get(username=profile_name)
        profile = Profile.objects.get(user=user)

        membership = GroupMember.objects.get(group=group, person=profile)
        membership.status = 'a'
        membership.save()

        return redirect('manage_requests', pk)
    return redirect('manage_requests', pk)


# 그룹이 유저에 보낸 '가입요청' 취소
# 새로고침 없게 수정하기
@manager_required
def group_request_cancel(request, pk):
    if request.method == "POST":
        form = request.POST
        group = Group.objects.get(id=pk)
        group.save()

        profile_name = form.get('user_p')
        user = User.objects.get(username=profile_name)
        profile = Profile.objects.get(user=user)

        membership = GroupMember.objects.get(group=group, person=profile)
        membership.status = 'r'
        membership.save()

        return redirect('manage_requests', pk)
    return redirect('manage_requests', pk)


# 차단은 아니고 거절만
@manager_required
def request_refuse(request):
    if request.method == "POST":
        form = request.POST
        group_id = form.get('group_id')
        group = Group.objects.get(id=group_id)
        group.save()

        profile = Profile.objects.get(user=request.user)
        membership = GroupMember.objects.get(group=group, person=profile, status='u')
        membership.delete()

        return redirect('manage_requests')
    return redirect('manage_requests')
