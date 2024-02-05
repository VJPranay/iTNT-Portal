from django.shortcuts import render

# Create your views here.
def industry_registration(request):
    return render(request, 'registrations/industry_registration.html')


def industry_registrations(request):
    return render(request,'dashboard/registrations/industry/list.html')