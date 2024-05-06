@login_required
def startup_registration_details(request, pk):
    try:
        startup = StartUpRegistrations.objects.get(pk=pk)
        return render(request, 'dashboard/profiles/v2/startup_profile_details.html', {'startup': startup})
    except StartUpRegistrations.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    

