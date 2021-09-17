from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View

def hello(request):
    return HttpResponse("Hello")

def add_room(request):
    if request.method == "GET":
        return render(request, "Bookin_conference_room_app/template.html")
    elif request.method == "POST":
        pass