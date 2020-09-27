from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Blog
from .form import Blogpost
# Create your views here.



def home(request):
    blogs = Blog.objects
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 3)
    page = request.GET.get('page') #request 된 변수가 뭔지 알아옴
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'blogs': blogs, 'posts': posts})


def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog': blog_detail})


def new(request):
    return render(request, 'new.html')


def map(request):
    return render(request, 'map.html')


def create(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save() #DB에 저장해라
    return redirect('/blog/'+str(blog.id)) #위에 다 처리하고 넘기세여


def blogpost(request):
    #1. 입력된 내용 처리하는 기능 -> Post
    if request.method == "POST":
        form = Blogpost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')

    #2. 빈 페이지 띄워주는 기능 -> Get
    else:
        form = Blogpost()
        return render(request, 'new.html', {'form': form})


def update(request, blog_id):

    #뭘 가져와서 수정할지 정하기
    blog = get_object_or_404(Blog, pk=blog_id)

    #불러와서 수정할 거 가져오기
    form = Blogpost(request.POST, instance=blog)
    if form.is_valid():
        form.save()
        return redirect('/blog/'+str(blog.id))

    return render(request, 'new.html', {'form': form})


# def delete(request, blog_id):
#     blog = get_object_or_404(Blog, pk=blog_id)
#     blog.delete()
#     return redirect('home')


class BlogDelete(DeleteView):
    template_name = 'delete.html'
    model = Blog
    success_url = reverse_lazy('home')

    def get_object(self):
        return get_object_or_404(Blog, pk=self.kwargs['blog_id'])

