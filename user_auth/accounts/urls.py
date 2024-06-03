from django.urls import path

from accounts.views import IndexView,UserAuthentication

app_name="accounts"
urlpatterns = [
    path("",IndexView.as_view(),name='index'),
    # path("accounts/",,name='accounts')
    path("accounts/login",UserAuthentication.as_view(),name='login'),
    path("accounts/signup",UserAuthentication.as_view(),name='signup'),
    path("accounts/logout",UserAuthentication.as_view(),name='logout'),
    path("accounts/dashboard",UserAuthentication.as_view(),name='dashboard'),
    path('accounts/activate-user/<uidb64>/<token>', UserAuthentication.as_view(), name='activate_user'),
    path("accounts/forget-password",UserAuthentication.as_view(),name='forget_password_request'),
    path("accounts/reset-password/<uidb64>/<token>",UserAuthentication.as_view(),name='reset_password')
]
