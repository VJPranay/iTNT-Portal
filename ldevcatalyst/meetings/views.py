from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def vc_meeting_requests(request):
    return render(request,'dashboard/meetings/vc/meeting_requests.html')