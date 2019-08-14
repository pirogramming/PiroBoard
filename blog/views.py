from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Post
from users.models import Profile, Group, GroupMember
from .forms import GroupForm, CommentForm, PostForm


@login_required
def home(request):
    profile = Profile.objects.get(user=request.user)
    ctx = {}
    user_groups = profile.group.all()

    if len(user_groups) > 0:
        ctx['user_groups'] = user_groups
        ctx['hasGroup'] = True

    else:
        ctx['hasGroup'] = False

    return render(request, "blog/home.html", ctx)


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
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    posts = Post.objects.all()
    hi = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'blog/group_detail.html', hi)


# @login_required
def profile_revise(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            us = form.save()
            return redirect("accounts:profile")
    else:
        profileform = UserEditForm(instance=request.user)
        forms = {'profileform': profileform}
        return render(request, 'accounts/profile_revise.html', forms)


def about(request):
    # return render(request, 'blog/about.html', {'title': 'About'})
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.group_creator = request.user
            group.created_date = timezone.now()
            group.save()

            GroupMember.objects.create(person=request.user.profile, group=group, status='a')

            return redirect('blog-home')
    else:
        form = GroupForm()
    return render(request, 'blog/about.html', {'form': form})


def login(request):
    return render(request, 'users/login.html')


# sulmo
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form})


def post_new(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST['title']
        post.author = request.user
        post.content = request.POST['content']
        post.photo = request.FILES['photo']
        post.save()
        return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog-home')


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('blog-home')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_new.html', {
        'form': form,
    })
#
# def invite(request):
#     return render(request, 'blog/notification/friends_invite_sent/notice.html')
