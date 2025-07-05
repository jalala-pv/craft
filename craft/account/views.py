from django.shortcuts import render,redirect
from .forms import *
from django.views.generic import FormView,CreateView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login,logout
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin



class LoginView(FormView):
    template_name='login.html'
    form_class=LoginForm
    def post(self,request):
        form=LoginForm(data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pswd=form.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                return redirect('shop')
            else:
                return redirect('login')
        return render(request,'login.html',{'form':form})
        

        


class RegistrationView(CreateView):
    template_name='registration.html'
    form_class=RegistrationForm
    success_url=reverse_lazy('login')

    def form_valid(self, form):
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)
    
class LogOutView(View):
    def get(self,request):
        logout(request)
        return redirect('shop')
    
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password if an account exists with the email you entered. You should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')