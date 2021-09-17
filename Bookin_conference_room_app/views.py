from django.shortcuts import render, redirect
from time import *
from Bookin_conference_room_app.models import *
# Create your views here.
from django.http import HttpResponse
from django.views import View

def hello(request):
    return HttpResponse("Hello")

def add_room(request):
    """
    Ado room to databse
    :param request:
    :return: redirect user to page rooms
    """
    if request.method == "GET":
        return render(request, "Bookin_conference_room_app/hello.html")
    elif request.method == "POST":
        name = request.POST["name"]
        sets = int(request.POST["sets"])
        projector = bool(request.POST.get("projector"))
        if not name:
            return HttpResponse("You must set name")
        if sets <= 0:
            return HttpResponse("Sets must be > 0!")
        if Room.objects.filter(name=name).first():
            return HttpResponse("That room exist! Choose difftrent name! ")
        Room.objects.create(name=name, sets=sets, projector=projector)
        return redirect("/rooms")


def show_room_list(request):
    """
    Showa page with all rooms
    :param request:
    :return: page with all rooms
    """
    if request.method == "GET":
        rooms = Room.objects.all()
        return render(request, "Bookin_conference_room_app/list_of_rooms.html",
                      {
                          "rooms": rooms
                      }
                      )


def delete_room(request, id):
    """
    Delete choosed room
    :param request:
    :param id: id of room
    :return: redirect user to page rooms
    """
    if request.method == "GET":
        room = Room.objects.get(id=int(id))
        return render(request, "Bookin_conference_room_app/delete_room.html",
                      {
                          "room": room
                      }
                      )
    else:
        room = Room.objects.get(id=id)
        room.delete()
        HttpResponse("Room deleted")
        return redirect("/rooms")

def edit_room(request, id):
    """
    Edit room parms
    :param request:
    :param id: room
    :return: redirect user to page rooms
    """
    if request.method == "GET":
        room = Room.objects.get(id=int(id))
        return render(request, "Bookin_conference_room_app/hello.html",{
            "room": room
        })

    elif request.method == "POST":
        room = Room.objects.get(id=id)
        name = request.POST["name"]
        sets = int(request.POST["sets"])
        projector = bool(request.POST.get("projector"))
        if not name:
            return HttpResponse("You must set name")
        if sets <= 0:
            return HttpResponse("Sets must be > 0!")
        if Room.objects.filter(name=name).first():
            return HttpResponse("That room exist! Choose difftrent name! ")
        room.name = name
        room.sets = sets
        room.projector = projector
        room.save()
        return redirect("/rooms")