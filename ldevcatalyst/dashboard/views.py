from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                return JsonResponse({'success': True})
            else:
                # Handle invalid login credentials
                form.add_error(None, 'Invalid login credentials')
                return JsonResponse({'success': False})
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})