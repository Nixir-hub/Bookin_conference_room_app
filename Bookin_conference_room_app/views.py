from django.shortcuts import render
from Bookin_conference_room_app.models import *
# Create your views here.
from django.http import HttpResponse
from django.views import View

def hello(request):
    return HttpResponse("Hello")

def add_room(request):
    if request.method == "GET":
        return render(request, "Bookin_conference_room_app/hello.html")
    elif request.method == "POST":
        name = request.POST["name"]
        sets = int(request.POST["sets"])
        projector = bool(request.POST["projector"])
        Room.objects.create(name=name, sets=sets, projector=projector)
        return HttpResponse("Room added")


def show_room_list(request):
    if request.method == "GET":
        rooms = Room.objects.all()
        return render(request, "Bookin_conference_room_app/list_of_rooms.html",
                      {
                          "rooms": rooms
                      }
                      )
