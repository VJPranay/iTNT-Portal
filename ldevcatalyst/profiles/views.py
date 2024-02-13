from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def vc_list(request):
    return render(request,'dashboard/vc/list.html')