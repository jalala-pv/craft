from django.shortcuts import render,redirect
from .forms import *
from django.views.generic import FormView,CreateView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login,logout
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin



from django.contrib import messages

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('username')
            pswd = form.cleaned_data.get('password')
            user = authenticate(request, username=uname, password=pswd)
            if user:
                login(request, user)
                
                return redirect('shop')
            else:
                messages.error(request, "Invalid username or password.")  # ✅ Show error
        else:
            messages.error(request, "Please correct the errors below.")  # Optional

        return render(request, 'login.html', {'form': form})

        

        


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
    
