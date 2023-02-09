from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import views as auth_views
from .forms import AccountSignupForm,AccountLoginForm 
from .models import Account
from .forms import (AccountLoginForm,AccountAvatorUploadForm)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from. models import Account,Follow
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

class AccountSignUpView(generic.CreateView):
    form_class=AccountSignupForm
    success_url=reverse_lazy('login')
    template_name='account/signup.html'

class AccountLoginView(auth_views.LoginView):
    form_class=AccountLoginForm
    template_name='account/login.html'

class AccountLogoutView(auth_views.LogoutView):
    template_name='account/logout.html'

class AccountDetailView(generic.DetailView):
    model=Account
    template_name='account/detail.html'

class AccountAvatorUploadView(LoginRequiredMixin,generic.FormView):
    template_name='account/avator_upload_form.html'
    form_class=AccountAvatorUploadForm

    def form_valid(self,form):
        user=self.request.user
        avator=form.cleaned_data['avator']
        account=Account.objects.get(username=user)
        account.avator=avator
        account.save()
        return redirect('avator_upload_done')

class AccountAvatorUploadDoneView(LoginRequiredMixin,generic.TemplateView):
    template_name='account/avator_upload_done.html'

@login_required
def post_follow(request,pk):
    if request.method=='POST':
        follow_user=Account.objects.get(pk=pk)
        if request.user==follow_user:
            messages.error(request,'自分に対してはフォローできません。')
            return redirect(to='/')

        follow_user.follower_count=+1
        follow_user.save()

        request.user.following_count=+1
        request.user.save()

        follow=Follow()
        follow.follow_id=request.user
        follow.follower_id=follow_user
        follow.save()

        messages.success(request,'ユーザーをフォローしました')
    else:
        messages.error(request,'正しい方法でフォローしてください')
    return redirect(to='/')
