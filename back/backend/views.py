from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.

# each stub.
def profile(request):
    data = {
        'name': 'Vitor',
        'location': 'Finland',
        'is_active': True,
        'count': 28
    }

    return JsonResponse(data)
