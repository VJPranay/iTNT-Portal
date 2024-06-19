from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MeetingRequest
from .forms import MeetingRequestForm, MeetingRequestUpdateForm,MeetingRequestCancelForm
from profiles.models import User,StartUp,Researcher

from django.http import JsonResponse
from django.contrib import messages

@login_required
def meeting_request_list(request):
    sent_requests_q = MeetingRequest.objects.filter(sender=request.user).exclude(status='accepted').order_by('-id')
    sent_requests = []
    for sent_request in sent_requests_q:
        temp = {
            'pk' : sent_request.id,
            'receiver' : sent_request.receiver,
            'receiver_name' : str(StartUp.objects.get(user_id=sent_request.receiver.id).company_name) if sent_request.receiver.user_role == 6 else str(Researcher.objects.get(user_id=sent_request.receiver.id).name),
            'receiver_id' : str(StartUp.objects.get(user_id=sent_request.receiver.id).id) if sent_request.receiver.user_role == 6 else str(Researcher.objects.get(user_id=sent_request.receiver.id).id),
            'status' : sent_request.status,
            'date' : sent_request.date,
            'time' : sent_request.time,
            'meeting_type' : sent_request.meeting_type,
            'meeting_details' : sent_request.meeting_details,
            'notes' : sent_request.notes,
        }
        sent_requests.append(temp)
    received_requests_q = MeetingRequest.objects.filter(receiver=request.user).exclude(status='accepted').order_by('-id')
    received_requests = []
    for received_request in received_requests_q:
        temp = {
            'pk' : received_request.id,
            'sender' : received_request.sender,
            'sender_name' : str(StartUp.objects.get(user_id=received_request.sender.id).company_name) if received_request.sender.user_role == 6 else str(Researcher.objects.get(user_id=received_request.sender.id).name),
            'sender_id' : str(StartUp.objects.get(user_id=received_request.sender.id).id) if received_request.sender.user_role == 6 else str(Researcher.objects.get(user_id=received_request.sender.id).id),
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
    return render(request, 'smeconnect/meeting_request_list.html', context)


@login_required
def confirmed_meeting_request_list(request):
    sent_requests_q = MeetingRequest.objects.filter(sender=request.user, status='accepted').order_by('-id')
    sent_requests = []
    for sent_request in sent_requests_q:
        temp = {
            'pk' : sent_request.id,
            'receiver' : sent_request.receiver,
            'receiver_name' : str(StartUp.objects.get(user_id=sent_request.receiver.id).company_name) if sent_request.receiver.user_role == 6 else str(Researcher.objects.get(user_id=sent_request.receiver.id).name),
            'receiver_id' : str(StartUp.objects.get(user_id=sent_request.receiver.id).id) if sent_request.receiver.user_role == 6 else str(Researcher.objects.get(user_id=sent_request.receiver.id).id),
            'status' : sent_request.status,
            'date' : sent_request.date,
            'time' : sent_request.time,
            'meeting_type' : sent_request.meeting_type,
            'meeting_details' : sent_request.meeting_details,
            'notes' : sent_request.notes,
        }
        sent_requests.append(temp)
    received_requests_q = MeetingRequest.objects.filter(receiver=request.user, status='accepted').order_by('-id')
    received_requests = []
    for received_request in received_requests_q:
        temp = {
            'pk' : received_request.id,
            'sender' : received_request.sender,
            'sender_name' : str(StartUp.objects.get(user_id=received_request.sender.id).company_name) if received_request.sender.user_role == 6 else str(Researcher.objects.get(user_id=received_request.sender.id).name),
            'sender_id' : str(StartUp.objects.get(user_id=received_request.sender.id).id) if received_request.sender.user_role == 6 else str(Researcher.objects.get(user_id=received_request.sender.id).id),
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
def meeting_request_cancel(request, pk):
    meeting_request = get_object_or_404(MeetingRequest, pk=pk)
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
                    return redirect('researcher_profiles_list')
            elif request.user.id == meeting_request.sender.id:
                if meeting_request.receiver.user_role == 6:
                    return redirect('startup_profiles_list')
                else:
                    return redirect('researcher_profiles_list')
            else:
                return redirect('meeting_request_list')
    else:
        form = MeetingRequestCancelForm(instance=meeting_request)
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
        messages.success(request, 'If you would like to reschedule the meeting, please send a new request.')
    return redirect('meeting_request_detail', pk=pk)

@login_required
def sme_calendar_view(request):
    status = request.GET.get('status')  # Get the status parameter from the request
    if status:
        if status == 'all':
            meeting_requests = MeetingRequest.objects.all()
        else:
            meeting_requests = MeetingRequest.objects.filter(status=status)
    else:
        meeting_requests = MeetingRequest.objects.all()  # Fetch all meeting requests
    return render(request, 'smeconnect/sme_meeting_calendar.html', {'meeting_requests': meeting_requests})

@login_required
def sme_calendar_data(request):
    status = request.GET.get('status')
    if status and status != 'all':
        meeting_requests = MeetingRequest.objects.filter(status=status)
    else:
        meeting_requests = MeetingRequest.objects.all()

    print(f"Total meeting requests fetched: {meeting_requests.count()}")

    # Serialize meeting requests data
    meeting_data = []
    for meeting in meeting_requests:
        print(f"Processing meeting ID: {meeting.id}, Sender Role: {meeting.sender.user_role}, Receiver Role: {meeting.receiver.user_role}")
        if meeting.date and meeting.time:
            if meeting.sender.user_role == '6' :
                sent_by = 'startup'  # Meeting sent by startup to SME
                start_up = meeting.sender.username
                sme_name = meeting.receiver.username
                print(f"Meeting sent by startup: {start_up} to {sme_name}")
                
            elif meeting.sender.user_role == '5':
                sent_by = 'sme'  # Meeting sent by SME to startup
                start_up = meeting.receiver.username
                sme_name = meeting.sender.username
                print(f"Meeting sent by SME: {sme_name} to {start_up}")
            else:
                # Handle other cases if necessary
                print(f"Unknown user_role: {meeting.sender.user_role}")
                continue  # Skip this meeting if user_role is not recognized

            meeting_data.append({
                'meeting_id': meeting.id,
                'start_up': start_up,
                'sme_name': sme_name,
                'meeting_date': meeting.date.strftime('%Y-%m-%d'),  # Format date as string
                'meeting_time': meeting.time.strftime('%H:%M'),  # Format time as string
                'status': meeting.status,
                'sent_by': sent_by
            })

    print(f"Final meeting_data: {meeting_data}")  # Print final meeting_data list

    return JsonResponse(meeting_data, safe=False)


