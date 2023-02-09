from django.urls import path,include
from . import views
urlpatterns=[
    path('signup/',views.AccountSignUpView.as_view(),name='signup'),
    path('login/',views.AccountLoginView.as_view(),name='login'),
    path('logout/',views.AccountLogoutView.as_view(),name='logout'),
    path('<int:pk>/',views.AccountDetailView.as_view(),name='detail'),
    path('avator/upload/',views.AccountAvatorUploadView.as_view(),name='avator_upload'),
    path('avator/upload/done',views.AccountAvatorUploadDoneView.as_view(),name='avator_upload_done'),
    path('<int:pk>/follow/',views.post_follow,name='follow'),
]

