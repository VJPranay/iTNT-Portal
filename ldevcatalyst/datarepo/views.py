from django.shortcuts import render
from .models import State,District,Institution
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def districts(requsts):
    state_id = requsts.GET.get('state_id')
    if not state_id:
        return JsonResponse([], safe=False)
    districts = District.objects.filter(state_id=state_id)
    return JsonResponse(list(districts.values('id','name')), safe=False)


@csrf_exempt
def institutions(requsts):
    district_id = requsts.GET.get('district_id')
    if not district_id:
        return JsonResponse([], safe=False)
    institutions = Institution.objects.filter(district_id=district_id)
    return JsonResponse(list(institutions.values('id','name')), safe=False)



