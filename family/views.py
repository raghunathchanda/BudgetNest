from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def add_family(request):
    return HttpResponse("add family page")