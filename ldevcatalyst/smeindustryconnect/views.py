from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import SmeIndustryMeetingRequest
from .forms import MeetingRequestForm, MeetingRequestUpdateForm,MeetingRequestCancelForm
from profiles.models import User,Researcher,Industry

from django.http import JsonResponse
from django.contrib import messages

@login_required
def smeindustry_meeting_request_list(request):
    # Fetch sent meeting requests
    sent_requests_q = SmeIndustryMeetingRequest.objects.filter(sender=request.user).exclude(status='accepted').order_by('-id')
    sent_requests = []
    for sent_request in sent_requests_q:
        temp = {
            'pk': sent_request.id,
            'receiver': sent_request.receiver,
            'receiver_name': str(Researcher.objects.get(user_id=sent_request.receiver.id).name) if sent_request.receiver.user_role == 5 else str(Industry.objects.get(user_id=sent_request.receiver.id).name),
            'receiver_id': str(Researcher.objects.get(user_id=sent_request.receiver.id).id) if sent_request.receiver.user_role == 5 else str(Industry.objects.get(user_id=sent_request.receiver.id).id),
            'status': sent_request.status,
            'date': sent_request.date,
            'time': sent_request.time,
            'meeting_type': sent_request.meeting_type,
            'meeting_details': sent_request.meeting_details,
            'notes': sent_request.notes,
        }
        sent_requests.append(temp)

    # Fetch received meeting requests
    received_requests_q = SmeIndustryMeetingRequest.objects.filter(receiver=request.user).exclude(status='accepted').order_by('-id')
    received_requests = []
    for received_request in received_requests_q:
        temp = {
            'pk': received_request.id,
            'sender': received_request.sender,
            'sender_name': str(Researcher.objects.get(user_id=received_request.sender.id).name) if received_request.sender.user_role == 5 else str(Industry.objects.get(user_id=received_request.sender.id).name),
            'sender_id': str(Researcher.objects.get(user_id=received_request.sender.id).id) if received_request.sender.user_role == 5 else str(Industry.objects.get(user_id=received_request.sender.id).id),
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
    return render(request, 'smeindustry_connect/meeting_request_list.html', context)


@login_required
def smeindustry_confirmed_meeting_request_list(request):
    sent_requests_q =SmeIndustryMeetingRequest.objects.filter(sender=request.user, status='accepted').order_by('-id')
    sent_requests = []
    for sent_request in sent_requests_q:
        temp = {
            'pk' : sent_request.id,
            'receiver' : sent_request.receiver,
            'receiver_name' : str(Researcher.objects.get(user_id=sent_request.receiver.id).name) if sent_request.receiver.user_role == 5 else str(Industry.objects.get(user_id=sent_request.receiver.id).name),
            'receiver_id' : str(Researcher.objects.get(user_id=sent_request.receiver.id).id) if sent_request.receiver.user_role == 5 else str(Industry.objects.get(user_id=sent_request.receiver.id).id),
            'status' : sent_request.status,
            'date' : sent_request.date,
            'time' : sent_request.time,
            'meeting_type' : sent_request.meeting_type,
            'meeting_details' : sent_request.meeting_details,
            'notes' : sent_request.notes,
        }
        sent_requests.append(temp)
    received_requests_q = SmeIndustryMeetingRequest.objects.filter(receiver=request.user, status='accepted').order_by('-id')
    received_requests = []
    for received_request in received_requests_q:
        temp = {
            'pk' : received_request.id,
            'sender' : received_request.sender,
            'sender_name' : str(Researcher.objects.get(user_id=received_request.sender.id).company_name) if received_request.sender.user_role == 5 else str(Industry.objects.get(user_id=received_request.sender.id).name),
            'sender_id' : str(Researcher.objects.get(user_id=received_request.sender.id).id) if received_request.sender.user_role == 5 else str(Industry.objects.get(user_id=received_request.sender.id).id),
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
    return render(request, 'smeindustry_connect/meeting_request_confirmed.html', context)

@login_required
def smeindustry_meeting_request_detail(request, pk):
    meeting_request = get_object_or_404(SmeIndustryMeetingRequest, pk=pk)
    context = {'meeting_request': meeting_request}
    return render(request, 'smeindustry_connect/meeting_request_details.html', context)



@login_required
def smeindustry_meeting_request_create(request, receiver_id):
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
                return redirect('smeindustry_meeting_request_list')
            except Exception as e:
                print(f"Error saving meeting request: {e}")
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = MeetingRequestForm()
        print("Initialized empty form for GET request")

    return render(request, 'smeindustry_connect/meeting_request_form.html', {'form': form})

@login_required
def smeindustry_meeting_request_update(request, pk):
    meeting_request = get_object_or_404(SmeIndustryMeetingRequest, pk=pk)
    if request.method == 'POST':
        form = MeetingRequestUpdateForm(request.POST, instance=meeting_request)
        if form.is_valid():
            form.save()
            return redirect('smeindustry_meeting_request_detail', pk=pk)
    else:
        form = MeetingRequestUpdateForm(instance=meeting_request)
    return render(request, 'smeindustry_connect/meeting_request_form.html', {'form': form})




@login_required
def smeindustry_meeting_request_cancel(request, pk):
    meeting_request = get_object_or_404(SmeIndustryMeetingRequest, pk=pk)
    if request.method == 'POST':
        form = MeetingRequestCancelForm(request.POST, instance=meeting_request)
        if form.is_valid():
            form.save()
            meeting_request.status = 'rejected'
            meeting_request.save()
            if request.user.id == meeting_request.receiver.id:
                if meeting_request.sender.user_role == 5:
                    return redirect('sme_profiles_list')
                else:
                    return redirect('industry_profiles_list')
            elif request.user.id == meeting_request.sender.id:
                if meeting_request.receiver.user_role == 4:
                    return redirect('sme_profiles_list')
                else:
                    return redirect('industry_profiles_list')
            else:
                return redirect('smeindustry_meeting_request_list')
    else:
        form = MeetingRequestCancelForm(instance=meeting_request)
    return render(request, 'smeindustry_connect/meeting_request_form.html', {'form': form})


@login_required
def smeindustry_meeting_request_accept(request, pk):
    meeting_request = get_object_or_404(SmeIndustryMeetingRequest, pk=pk, receiver=request.user)
    if meeting_request.status == 'sent':
        meeting_request.status = 'accepted'
        meeting_request.save()
        messages.success(request, 'Meeting has been accepted.')
    return redirect('smeindustry_meeting_request_detail', pk=pk)

@login_required
def smeindustry_meeting_request_reject(request, pk):
    meeting_request = get_object_or_404(SmeIndustryMeetingRequest, pk=pk, receiver=request.user)
    if meeting_request.status == 'sent':
        meeting_request.status = 'rejected'
        meeting_request.save()
        messages.success(request, 'If you would like to reschedule the meeting, please send a new request.')
    return redirect('smeindustry_meeting_request_detail', pk=pk)


@login_required
def smeindustry_calendar_data(request):
    status = request.GET.get('status')
    if status and status != 'all':
        meeting_requests = SmeIndustryMeetingRequest.objects.filter(status=status)
    else:
        meeting_requests = SmeIndustryMeetingRequest.objects.all()

    # Serialize meeting requests data
    meeting_data = []
    # Process SmeIndustryMeetingRequest instances
    for meeting in meeting_requests:
        if meeting.date and meeting.time:
            # Determine who sent the meeting request
            if meeting.sender.user_role == 5:  # Assuming 5 represents Reasearcher user_role
                sent_by = 'sme'
                sme_name = meeting.sender.username
                industry_name = meeting.receiver.username
                print(f"Meeting sent by startup: {sme_name} to {industry_name}")
            elif meeting.sender.user_role == 4:  # Assuming 4 represents Industry user_role
                sent_by = 'industry'
                industry_name = meeting.receiver.username
                sme_name = meeting.sender.username
                print(f"Meeting sent by vc: {industry_name} to {sme_name}")
            else:
                # Handle other cases if necessary
                print(f"Unknown user_role: {meeting.sender.user_role}")
                continue  # Skip this meeting if user_role is not recognized

            # Append meeting data to list
            meeting_data.append({
                'meeting_id': meeting.id,
                'sme': sme_name,
                'industry_name': industry_name,
                'meeting_date': meeting.date.strftime('%Y-%m-%d'),  # Format date as string
                'meeting_time': meeting.time.strftime('%H:%M'),  # Format time as string
                'status': meeting.status,
                'sent_by': sent_by
            })

    return JsonResponse(meeting_data, safe=False)



@login_required
def smeindustry_calendar_view(request):
    status = request.GET.get('status')  # Get the status parameter from the request
    if status:
        if status == 'all':
            meeting_requests = SmeIndustryMeetingRequest.objects.all()
        else:
            meeting_requests = SmeIndustryMeetingRequest.objects.filter(status=status)
    else:
        meeting_requests = SmeIndustryMeetingRequest.objects.all()  # Fetch all meeting requests
        print(meeting_requests)
        
    return render(request, 'smeindustry_connect/smeindustry_meeting_calendar.html', {'meeting_requests': meeting_requests})

