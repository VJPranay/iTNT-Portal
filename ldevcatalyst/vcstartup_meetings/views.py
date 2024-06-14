from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import vcstartup_MeetingRequest
from .forms import MeetingRequestForm, MeetingRequestUpdateForm,MeetingRequestCancelForm
from profiles.models import User,StartUp,VC

from django.http import JsonResponse
from django.contrib import messages

@login_required
def vcstartup_meeting_request_list(request):
    # Fetch sent meeting requests
    sent_requests_q = vcstartup_MeetingRequest.objects.filter(sender=request.user).exclude(status='accepted').order_by('-id')
    sent_requests = []
    for sent_request in sent_requests_q:
        temp = {
            'pk': sent_request.id,
            'receiver': sent_request.receiver,
            'receiver_name': str(StartUp.objects.get(user_id=sent_request.receiver.id).company_name) if sent_request.receiver.user_role == 6 else str(VC.objects.get(user_id=sent_request.receiver.id).name),
            'receiver_id': str(StartUp.objects.get(user_id=sent_request.receiver.id).id) if sent_request.receiver.user_role == 6 else str(VC.objects.get(user_id=sent_request.receiver.id).id),
            'status': sent_request.status,
            'date': sent_request.date,
            'time': sent_request.time,
            'meeting_type': sent_request.meeting_type,
            'meeting_details': sent_request.meeting_details,
            'notes': sent_request.notes,
        }
        sent_requests.append(temp)

    # Fetch received meeting requests
    received_requests_q = vcstartup_MeetingRequest.objects.filter(receiver=request.user).exclude(status='accepted').order_by('-id')
    received_requests = []
    for received_request in received_requests_q:
        temp = {
            'pk': received_request.id,
            'sender': received_request.sender,
            'sender_name': str(StartUp.objects.get(user_id=received_request.sender.id).company_name) if received_request.sender.user_role == 6 else str(VC.objects.get(user_id=received_request.sender.id).name),
            'sender_id': str(StartUp.objects.get(user_id=received_request.sender.id).id) if received_request.sender.user_role == 6 else str(VC.objects.get(user_id=received_request.sender.id).id),
            'status': received_request.status,
            'date': received_request.date,
            'time': received_request.time,
            'meeting_type': received_request.meeting_type,
            'meeting_details': received_request.meeting_details,
            'notes': received_request.notes,
        }
        received_requests.append(temp)

    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'vcstartup_connect/meeting_request_list.html', context)


@login_required
def vcstartup_confirmed_meeting_request_list(request):
    sent_requests_q =vcstartup_MeetingRequest.objects.filter(sender=request.user, status='accepted').order_by('-id')
    sent_requests = []
    for sent_request in sent_requests_q:
        temp = {
            'pk' : sent_request.id,
            'receiver' : sent_request.receiver,
            'receiver_name' : str(StartUp.objects.get(user_id=sent_request.receiver.id).company_name) if sent_request.receiver.user_role == 6 else str(VC.objects.get(user_id=sent_request.receiver.id).name),
            'receiver_id' : str(StartUp.objects.get(user_id=sent_request.receiver.id).id) if sent_request.receiver.user_role == 6 else str(VC.objects.get(user_id=sent_request.receiver.id).id),
            'status' : sent_request.status,
            'date' : sent_request.date,
            'time' : sent_request.time,
            'meeting_type' : sent_request.meeting_type,
            'meeting_details' : sent_request.meeting_details,
            'notes' : sent_request.notes,
        }
        sent_requests.append(temp)
    received_requests_q = vcstartup_MeetingRequest.objects.filter(receiver=request.user, status='accepted').order_by('-id')
    received_requests = []
    for received_request in received_requests_q:
        temp = {
            'pk' : received_request.id,
            'sender' : received_request.sender,
            'sender_name' : str(StartUp.objects.get(user_id=received_request.sender.id).company_name) if received_request.sender.user_role == 6 else str(VC.objects.get(user_id=received_request.sender.id).name),
            'sender_id' : str(StartUp.objects.get(user_id=received_request.sender.id).id) if received_request.sender.user_role == 6 else str(VC.objects.get(user_id=received_request.sender.id).id),
            'status' : received_request.status,
            'date' : received_request.date,
            'time' : received_request.time,
            'meeting_type' : received_request.meeting_type,
            'meeting_details' : received_request.meeting_details,
            'notes' : received_request.notes,
        }
        received_requests.append(temp)  
    context = {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'vcstartup_connect/meeting_request_confirmed.html', context)

@login_required
def vcstartup_meeting_request_detail(request, pk):
    meeting_request = get_object_or_404(vcstartup_MeetingRequest, pk=pk)
    context = {'meeting_request': meeting_request}
    return render(request, 'vcstartup_connect/meeting_request_details.html', context)


@login_required
def vcstartup_meeting_request_create(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)
    user = request.user

    print("Creating a meeting request")
    print(f"Sender: {user.username}, Receiver: {receiver.username}")

    if request.method == 'POST':
        form = MeetingRequestForm(request.POST)
        print("POST data received")
        print("Form data:", request.POST)
        
        if form.is_valid():
            print("Form is valid")
            try:
                meeting_request = form.save(commit=False)
                meeting_request.sender = user
                meeting_request.receiver = receiver
                meeting_request.save()
                print(f"Meeting request saved: {meeting_request}")
                return redirect('vcstartup_meeting_request_list')
            except Exception as e:
                print(f"Error saving meeting request: {e}")
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = MeetingRequestForm()
        print("Initialized empty form for GET request")

    return render(request, 'vcstartup_connect/meeting_request_form.html', {'form': form})
@login_required
def vcstartup_meeting_request_update(request, pk):
    meeting_request = get_object_or_404(vcstartup_MeetingRequest, pk=pk)
    if request.method == 'POST':
        form = MeetingRequestUpdateForm(request.POST, instance=meeting_request)
        if form.is_valid():
            form.save()
            return redirect('vcstartup_meeting_request_detail', pk=pk)
    else:
        form = MeetingRequestUpdateForm(instance=meeting_request)
    return render(request, 'vcstartup_connect/meeting_request_form.html', {'form': form})




@login_required
def vcstartup_meeting_request_cancel(request, pk):
    meeting_request = get_object_or_404(vcstartup_MeetingRequest, pk=pk)
    if request.method == 'POST':
        form = MeetingRequestCancelForm(request.POST, instance=meeting_request)
        if form.is_valid():
            form.save()
            meeting_request.status = 'rejected'
            meeting_request.save()
            if request.user.id == meeting_request.receiver.id:
                if meeting_request.sender.user_role == 6:
                    return redirect('startup_profiles_list')
                else:
                    return redirect('vc_profiles_list')
            elif request.user.id == meeting_request.sender.id:
                if meeting_request.receiver.user_role == 6:
                    return redirect('startup_profiles_list')
                else:
                    return redirect('vc_profiles_list')
            else:
                return redirect('vcstartup_meeting_request_list')
    else:
        form = MeetingRequestCancelForm(instance=meeting_request)
    return render(request, 'vcstartup_connect/meeting_request_form.html', {'form': form})


@login_required
def vcstartup_meeting_request_accept(request, pk):
    meeting_request = get_object_or_404(vcstartup_MeetingRequest, pk=pk, receiver=request.user)
    if meeting_request.status == 'sent':
        meeting_request.status = 'accepted'
        meeting_request.save()
        messages.success(request, 'Meeting has been accepted.')
    return redirect('vcstartup_meeting_request_detail', pk=pk)

@login_required
def vcstartup_meeting_request_reject(request, pk):
    meeting_request = get_object_or_404(vcstartup_MeetingRequest, pk=pk, receiver=request.user)
    if meeting_request.status == 'sent':
        meeting_request.status = 'rejected'
        meeting_request.save()
        messages.success(request, 'If you would like to reschedule the meeting, please send a new request.')
    return redirect('vcstartup_meeting_request_detail', pk=pk)



@login_required
def vcstartup_calendar_data(request):
    status = request.GET.get('status')
    if status:
        if status == 'all':
            meeting_requests = vcstartup_MeetingRequest.objects.all()
        else:
            meeting_requests = vcstartup_MeetingRequest.objects.filter(status=status)
    else:
        meeting_requests = vcstartup_MeetingRequest.objects.all()

    # Serialize meeting requests data
    meeting_data = []
    for meeting in meeting_requests:
        if meeting.date and meeting.time is not None and (meeting.sender.role == 'startup' and meeting.receiver.role == 'vc' or meeting.sender.role == 'vc' and meeting.receiver.role == 'startup'):
            meeting_data.append({
                'meeting_id': meeting.id,
                'start_up': meeting.sender.username,  # Assuming sender is the start_up
                'vc_name': meeting.receiver.username,  # Assuming receiver is the researcher
                'meeting_date': meeting.date,
                'meeting_time': meeting.time,
                'status': meeting.status,
                'sent_by': 'startup' if meeting.sender.role == 'startup' else 'vc' 
            })

    return JsonResponse(meeting_data, safe=False)
