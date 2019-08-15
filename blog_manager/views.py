from django.shortcuts import render

# Create your views here.


def group_manage(request, pk):
    return render(request, 'blog_manager/group_manage.html')