from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MeetingRequest
from .forms import MeetingRequestForm, MeetingRequestUpdateForm
from profiles.models import User

from django.contrib import messages

@login_required
def meeting_request_list(request):
    sent_requests = MeetingRequest.objects.filter(sender=request.user).exclude(status='accepted').order_by('-id')
    received_requests = MeetingRequest.objects.filter(receiver=request.user).exclude(status='accepted').order_by('-id')
    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'smeconnect/meeting_request_list.html', context)


@login_required
def confirmed_meeting_request_list(request):
    sent_requests = MeetingRequest.objects.filter(sender=request.user, status='accepted').order_by('-id')
    received_requests = MeetingRequest.objects.filter(receiver=request.user, status='accepted').order_by('-id')
    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'smeconnect/meeting_request_confirmed.html', context)

@login_required
def meeting_request_detail(request, pk):
    meeting_request = get_object_or_404(MeetingRequest, pk=pk)
    context = {'meeting_request': meeting_request}
    return render(request, 'smeconnect/meeting_request_detail.html', context)

@login_required
def meeting_request_create(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)
    
    if request.method == 'POST':
        form = MeetingRequestForm(request.POST)
        if form.is_valid():
            meeting_request = form.save(commit=False)
            meeting_request.sender = request.user
            meeting_request.receiver = receiver
            meeting_request.save()
            return redirect('meeting_request_list')
    else:
        form = MeetingRequestForm()

    return render(request, 'smeconnect/meeting_request_form.html', {'form': form})

@login_required
def meeting_request_update(request, pk):
    meeting_request = get_object_or_404(MeetingRequest, pk=pk)
    if request.method == 'POST':
        form = MeetingRequestUpdateForm(request.POST, instance=meeting_request)
        if form.is_valid():
            form.save()
            return redirect('meeting_request_detail', pk=pk)
    else:
        form = MeetingRequestUpdateForm(instance=meeting_request)
    return render(request, 'smeconnect/meeting_request_form.html', {'form': form})


@login_required
def meeting_request_accept(request, pk):
    meeting_request = get_object_or_404(MeetingRequest, pk=pk, receiver=request.user)
    if meeting_request.status == 'sent':
        meeting_request.status = 'accepted'
        meeting_request.save()
        messages.success(request, 'Meeting has been accepted.')
    return redirect('meeting_request_detail', pk=pk)

@login_required
def meeting_request_reject(request, pk):
    meeting_request = get_object_or_404(MeetingRequest, pk=pk, receiver=request.user)
    if meeting_request.status == 'sent':
        meeting_request.status = 'rejected'
        meeting_request.save()
        messages.success(request, 'Meeting has been rejected.')
    return redirect('meeting_request_detail', pk=pk)
