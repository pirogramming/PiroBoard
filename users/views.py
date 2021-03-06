from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import UserRegisterForm, ProfileForm
from .models import Profile, Group, GroupMember
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            region = form.cleaned_data.get('region')
            nickname = form.cleaned_data.get('nickname')
            profile_model, created = Profile.objects.get_or_create(user=user)
            profile_model.email = email
            profile_model.phone_number = phone_number
            profile_model.region = region
            profile_model.nickname = nickname
            profile_model.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            messages.success(request, f'다시 가입 정보를 기입하세요.')

    ctx = {
        'form': UserRegisterForm(),
    }

    return render(request, 'users/register.html', ctx)


@login_required
def profile(request):
    return render(request, 'users/profile.html', )


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, '프로필을 성공적으로 수정하였습니다.')
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/profile_update.html', {'form': form})


def find_user(request, group_id):  # 그룹 내에서 초대할 유저를 검색함
    """
        GET
            params or query
            group_id: params Int!
            terms: query string!
    """
    if request.GET['terms']:
        terms = request.GET['terms']
        profiles = User.objects.filter(username=terms)
        ctx = {
            "profiles": profiles,
            "group_id": group_id
        }

        return render(request, "users/find_users_results.html", ctx)
    else:
        return render(request, "users/find_users.html", )
        #


def invite_member(request):  # 유저를 초대하는 페이지
    """
    POST
    @body: 
        user_id: Int! (초대 해야 하는 사람)
        group_id: Int! (현재 그룹)
    """
    return render(request, 'users/invite.html')


# def accept_member(request):  # 초대를 수락하는 페이지
#     return render(request, 'users/accept.html')


def wait_member(request):  # 초대를 요청한 후 기다리는 페이지
    return render(request, 'users/wait.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })


def password_reset_form(request):
    form = PasswordChangeForm(request.POST or None)
    if request.method == 'POST':
        pass
    return render(request, 'users/password_reset_form.html', {
        'form': form,
    })


# 유저가 참여하고 싶은 그룹을 찾는 페이지
# 비공개 그룹은 뜨지 않도록 변경필요!
def group_find(request):
    if request.method == "POST":
        form = request.POST
        group_id = form.get('group_id')
        group = Group.objects.get(id=group_id)
        group.save()
        GroupMember.objects.create(person=request.user.profile, group=group, status='u')

        return redirect('users:group_manage')

    else:
        profile = Profile.objects.get(user=request.user)
        qs = Group.objects.exclude(group_open_status='n').exclude(group_users=profile)
        q = request.GET.get('q', '')
        if q:
            qs = qs.filter(group_name__icontains=q)

        ctx = {
            'group_list': qs,
            'q': q,
        }

    return render(request, 'users/find_groups.html', ctx)


# def group_apply(request):
#     if request.method == "POST":
#         form = request.POST
#         if form.is_valid():
#             group_id = form.group_id
#             group = Group.objects.get(id=group_id)
#             group.save()
#
#             GroupMember.objects.create(person=request.user.profile, group=group, status='a')
#
#             return redirect('blog-home')
#     else:
#         pass
#     return render(request, 'users/find_groups.html')


def requests_manage(request):
    profile = Profile.objects.get(user=request.user)
    user_requests = [x.group for x in GroupMember.objects.filter(person=profile, status='u')]
    group_requests = [x.group for x in GroupMember.objects.filter(person=profile, status='g')]

    ctx = {}

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

    return render(request, 'users/manage_groups.html', ctx)


#그룹이 유저에 보낸 '초대'수락
#새로 렌더링 하지 없게 수정하기
#가입하시겠냐고 알림창 띄우기
def request_accept(request):
    if request.method == "POST":
        form = request.POST
        group_id = form.get('group_id')
        group = Group.objects.get(id=group_id)
        group.save()

        profile = Profile.objects.get(user=request.user)
        membership=GroupMember.objects.get(group=group, person=profile)

        membership.status='a'
        membership.save()

        return redirect('users:group_manage')
    return redirect('blog-home')


#유저가 그룹에 보낸 '승인요청' 취소
#새로고침 없게 수정하기
def request_cancel(request):
    if request.method == "POST":
        form = request.POST
        group_id = form.get('group_id')
        group = Group.objects.get(id=group_id)
        group.save()

        profile = Profile.objects.get(user=request.user)
        membership=GroupMember.objects.get(group=group, person=profile,)
        membership.delete()

        return redirect('users:group_manage')
    return redirect('users:group_manage')


def user_manage_requests(request):
    person = request.user.profile

    user_requests = [x.group for x in GroupMember.objects.filter(person=person, status='u')]   # u = 가입승인요청
    group_requests = [x.group for x in GroupMember.objects.filter(person=person, status='g')]  # g = 가입요청

    ctx = {

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

    return render(request, 'users/user_manage_request.html', ctx)



# 그룹이 유저에게 보낸 요청을 수락해주는 기능
def group_request_accept(request):
    if request.method == "POST":
        form = request.POST
        person = request.user
        group = form.get('group_p')

        membership = GroupMember.objects.get(group=group, person=person)
        membership.status = 'a'
        membership.save()

        return redirect('users:user_manage_request')
    return redirect('users:user_manage_request')