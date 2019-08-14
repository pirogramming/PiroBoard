from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .models import Profile, Group
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')

def find_user(request, group_id): #그룹 내에서 초대할 유저를 검색함 
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
    
    


def invite_member(request):   #유저를 초대하는 페이지
    """
    POST
    @body: 
        user_id: Int! (초대 해야 하는 사람)
        group_id: Int! (현재 그룹)
    """
    
    return render(request, 'users/invite.html')


def accept_member(request):   #초대를 수락하는 페이지
    return render(request, 'users/accept.html')


def wait_member(request):    #초대를 요청한 후 기다리는 페이지
    return render(request, 'users/wait.html')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {
        'form': form
    })


def revise_profile(request):
    return render(request, 'users/revise_profile.html')



