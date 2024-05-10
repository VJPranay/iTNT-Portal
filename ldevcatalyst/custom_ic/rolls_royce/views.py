from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def challenge_details(request):
    return render(request,'custom_ic/rolls_royce/details.html')


def proposal_form(request):
    return render(request,'custom_ic/rolls_royce/proposal_form.html')