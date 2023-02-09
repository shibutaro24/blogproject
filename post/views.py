from django.shortcuts import render,redirect
from django.views import generic
from .models import Post,Favorite
from .forms import PostForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from account.models import Follow,Account
from django.db.models.query_utils import Q
# Create your views here.


class HomeView(generic.TemplateView):
    template_name='post/home.html'

@login_required
def create_post(request):
    if request.method=='POST':
        content=request.POST['content']
        user=request.user
        post=Post()
        post.content=content
        post.owner=user
        post.visibility=request.POST['visibility']
        if request.FILES:
            post.image=request.FILES['image']
        post.save()
        messages.success(request,'新しいメッセージを投稿しました。')
        return redirect(to='/')

    else:
        form=PostForm()
    params={
        'form':form
    }
    return render(request,'post/create.html',params)

def index(request,num=1):
    data=Post.objects.filter(visibility="PUBLIC")
    page=Paginator(data,5)
    params={
        'object_list':page.get_page(num)
    }
    return render(request,'post/home.html',params)

def detail_post(request,pk):
    data=Post.objects.get(pk=pk)
    params={
        'object':data,
        'is_favorite':False
    }
    if request.user.is_authenticated:
        is_favorite=Favorite.objects.filter(owner=request.user).filter(content_id=data).count()
        if is_favorite>0:
            params['is_favorite']=True
    return render(request,'post/detail.html',params)

@login_required
def post_delete(request,pk):
    if request.method=='POST':
        data=Post.objects.get(pk=pk,owner=request.user)
        data.delete()
        messages.error(request,'メッセージを削除しました')
    else:
        messages.error(request,'正しい方法で削除してください')
    return redirect(to='/')

@login_required
def post_favorite(request,pk):
    if request.method=='POST':
        data=Post.objects.get(pk=pk)
        is_favorite=Favorite.objects.filter(owner=request.user).filter(content_id=data).count()
        if is_favorite>0:
            messages.error(request,'既にそのメッセージはお気に入り登録をしています。')
            return redirect(to='/')

        data.favorite_count += 1
        data.save()
        favorite=Favorite()
        favorite.owner=request.user
        favorite.content_id=data
        favorite.save()
        messages.success(request,'メッセージをお気に入り登録しました')
    else:
        messages.error(request,'正しい方法でお気に入り登録してください')
    return redirect(to='/')

def home_timeline(request,num=1):
    followings=Follow.objects.filter(follow_id=request.user)
    following_account=Account.objects.filter(Q(pk__in=followings.values_list('follow_id',flat=True)))
    data=Post.objects.filter(Q(owner__in=following_account)|Q(owner=request.user))
    page=Paginator(data,5)
    params={
        'object_list':page.get_page(num)
    }
    return render(request,'post/timeline.html',params)

