from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserChangeForm
# Create your views here.

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('fristwebapp:index'))

def register(request):
    #register new user
    if request.method != 'POST':
        form = UserChangeForm()
    else:
        form = UserChangeForm(data = request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username = new_user.username,
                password = request.POST["password1"])
            login(request,authenticated_user)
            return HttpResponseRedirect(reverse('fristwebapp:index'))
    
    context = {'form':form}
    return  render(request,'registration/register.html',context)
