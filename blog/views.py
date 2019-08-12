from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from users.models import Profile
from blog.forms import GroupForm


@login_required
def home(request):
    # profile = request.user.profile
    profile = Profile.objects.create(user=request.user)
    ctx = {}
    user_groups = profile.group.all()

    if len(user_groups):
        ctx['user_groups'] = user_groups
        ctx['hasGroup'] = True

    else:
        ctx['hasGroup'] = False

    return render(request, "blog/home.html", {
        'pk': id
    }, ctx)


# from .models import Group, Post
#
#
# def home(request):
#     context = {
#         'posts': Post.objects.all(),
#         'groups': Group.objects.all()
#     }
#     return render(request, 'blog/home.html', context)
#
#
# def group_detail(request, pk):
#     group = get_object_or_404(Group, pk=pk)
#     return render(request, 'blog/group_detail.html', {'group': group})
#
#

def about(request):
    # return render(request, 'blog/about.html', {'title': 'About'})
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.group_creator = request.user

            group.created_date = timezone.now()
            group.save()
            return redirect('blog-home')
    else:
        form = GroupForm()
    return render(request, 'blog/about.html', {'form': form})


def login(request):
    return render(request, 'users/login.html')

#
# def invite(request):
#     return render(request, 'blog/notification/friends_invite_sent/notice.html')
