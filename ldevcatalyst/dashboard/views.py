from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.urls import reverse

def custom_login(request,):
    if request.user.is_authenticated:
        print("working")
        return redirect('dashboard_index')
    else:
        print("not working")
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False})
        elif request.method == 'GET':
            return render(request, 'login.html')
    


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))
    

@login_required
def dashboard_index(request):
    return render(request,'dashboard/dashboard.html')

