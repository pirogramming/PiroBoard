from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm


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


@login_required
def profile_update(request):
    if request.POST == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        print("벨리드 전")
        if form.is_valid():
            print("벨리드 후")
            modified_profile = form.save()
            messages.success(request, '프로필을 성공적으로 수정하였습니다.')
            #return redirect("users:profile")
            return redirect(modified_profile)
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})


