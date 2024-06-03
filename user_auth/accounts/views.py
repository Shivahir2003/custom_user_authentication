from accounts.forms import UserSignUpForm,UserLoginForm,ChangePasswordForm
from accounts.token import token_generator
from accounts.utils import send_email

from django.contrib import messages
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.request import HttpRequest as HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'accounts/index.html'


class UserAuthentication(TemplateView):

    def dispatch(self,request,**kwargs):
        if request.path == '/accounts/login':
            return self.loginview(request)
        elif request.path == '/accounts/logout':
            return self.logoutview(request)
        elif request.path == '/accounts/signup':
            return self.signupview(request)
        elif request.path == '/accounts/forget-password':
            return self.forget_password_request(request)
        elif '/accounts/reset-password' in request.path :
            return self.reset_password(request,**kwargs)
        elif '/accounts/dashboard' in request.path :
            return self.user_dashboard(request,**kwargs)
        elif '/accounts/activate-user' in request.path:
            return self.activate_user(request,**kwargs)

    def signupview(self,request):
        """ 
            get userdetails for register user,
            register without user activation,
            send mail for user activation
        """
        if request.method == "POST":
            signup_form = UserSignUpForm(request.POST or None)
            if signup_form.is_valid():
                username=signup_form.cleaned_data['username']
                password=signup_form.cleaned_data['password1']
                email=signup_form.cleaned_data['email']

                # check if user is exists then redirect to login view
                if User.objects.filter(username=username).exists():
                    messages.error(request,'you have already signed up ')
                    return redirect('accounts:login')
                # authenticate user and save user
                user= authenticate(request,username=username, password=password,email=email)
                # generate unique id and token 
                uid=urlsafe_base64_encode(force_bytes(user.pk))
                token = token_generator.make_token(user)
                # adding user details

                # sending mail for user activation link 
                subject=f'user activation link for {user.username}'
                html_content = render_to_string('email_templates/user_activation_link.html',{'token':token,'uid':uid})
                text_content = strip_tags(html_content)
                send_email(subject,text_content,request.user,html_content)

                messages.info(request,'check mail for activation link')
                return redirect('accounts:login')
        elif request.method == "GET":
            signup_form = UserSignUpForm()
        return render(request,"accounts/signup.html",{'form':signup_form})

    def loginview(self,request):
        """ 
            User Login View
            
            Required parameter:
                username,password
            
            user can login if user is activate 
            redirect to dashboard with 
        """
        if request.method == "POST":
            login_form =UserLoginForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']

                # check if user is not exists redirect to signup view
                if not User.objects.filter(username=username).exists():
                    messages.error(request,'you have not signed up ')
                    return redirect('accounts:signup')
                elif not User.objects.get(username=username).is_active: 
                    messages.error(request,'user is not active')
                    messages.error(request,'check mail for user activation link')
                    return redirect('accounts:login')

                user = authenticate(request,username=username,password=password)
                if user is None:
                    messages.error(request,'invalid username or password')
                    return redirect('accounts:login')
                else:
                    login(request, user)
                    return redirect(reverse('accounts:dashboard',args=[user.pk]))

        elif request.method =="GET":
            if request.user.is_authenticated:
                return redirect(reverse('accounts:dashboard',args=[request.user.pk]))
            login_form =UserLoginForm()
        return render(request,'accounts/login.html',{'form':login_form})

    @method_decorator(login_required(login_url='accounts:login'))
    def logoutview(self,request):
        """ log out user if your is logged in"""
        logout(request)
        return redirect("accounts:login")

    @method_decorator(login_required(login_url='accounts:login'))
    def forget_password_request(self,request):
        """ 
            get user details,
            generate forget password link,
            send link using email on user's email address
        """
        # generate token and unique id for forgetpassword
        uid=urlsafe_base64_encode(force_bytes(request.user.pk))
        token = token_generator.make_token(request.user)
        # print(f'uid = {uid}, token  = {token}')
        # send mail for forget password link
        subject=f'forget password link for {request.user.username}'
        html_content = render_to_string('email_templates/forget_password_link.html',{'token':token,'uid':uid})
        text_content = strip_tags(html_content)
        send_email(subject,text_content,request.user,html_content)
        messages.info(request,"check mail for forget password link")
        return redirect(reverse('accounts:dashboard',args=[request.user.pk]))

    @method_decorator(login_required(login_url='accounts:login'))
    def reset_password(self,request,uidb64,token):
        """
            get current password and new pssword and reset password,
            change password if current password is correct
        """
        # get user object form unique id 
        user_pk=urlsafe_base64_decode(uidb64).decode('utf-8')
        user= get_object_or_404(User,pk=user_pk)
        if request.method == "POST":
            reset_password_form=ChangePasswordForm(request.POST)
            if reset_password_form.is_valid():
                current_password=reset_password_form.cleaned_data['old_password']
                new_password=reset_password_form.cleaned_data['new_password']

                if not user.check_password(current_password):
                    messages.error(request,"current password does not match")
                elif current_password == new_password:
                    messages.error(request,"new password can't be same as old password")
                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request,"password is changed")
                    return redirect('accounts:logout')

        elif request.method == "GET":
            reset_password_form=ChangePasswordForm()
        return render(request,'accounts/reset_password.html',{'form':reset_password_form})

    @method_decorator(login_required(login_url='accounts:login'))
    def user_dashboard(self,request,user_pk):
        """
            get user primary key,
            show user details
        """
        # get user object from primarkey
        user = get_object_or_404(User, pk=user_pk)
        return render(request, 'accounts/dashboard.html',{'user': user})

    def activate_user(self,request,uidb64,token):
        """
            activate user for login 
        """
        # get user object form unique id 
        user_pk = urlsafe_base64_decode(uidb64).decode('utf-8')
        user= get_object_or_404(User,pk=user_pk)
        user.is_active =True  # activate user for login
        user.save()
        messages.success(request,'user registered susscess fully')
        return redirect('accounts:login')
        