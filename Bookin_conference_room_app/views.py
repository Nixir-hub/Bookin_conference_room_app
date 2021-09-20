from django.shortcuts import render, redirect
import datetime
from Bookin_conference_room_app.models import *
from django.http import HttpResponse
from django.views import View


def main_menu_bookin(request):
    return render(request, "Bookin_conference_room_app/main_menu_bookin.html")


def hello(request):
    return HttpResponse("Hello, Welcome to Bookin Room")


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
            return HttpResponse("That room exist! Choose different name! ")
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
        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.reservation_set.all()]
            room.reserved = datetime.date.today() in reservation_dates
        return render(request, "Bookin_conference_room_app/list_of_rooms.html",
                          {"rooms": rooms},)


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
        room.save()
        room.sets = sets
        room.projector = projector
        room.save()
        return redirect("/rooms")


def take_reservation(request, id):
    if request.method == "GET":
        rooms = Room.objects.all()
        room = Room.objects.get(id=int(id))
        reserv = room.reservation_set.get_queryset()
        return render(request, "Bookin_conference_room_app/make_reservation.html",
                      {
                          "rooms": rooms,
                          "reserv": reserv,
                      })

    elif request.method == "POST":
        comment = request.POST["comment"]
        date = request.POST.get("date")
        room = Room.objects.get(id=int(id))
        reserv = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        if Reservation.objects.filter(room_id=room, date=date):
            return HttpResponse("Room is busy in that day choose other day!")
        if date < str(datetime.date.today()):
            return HttpResponse("Data from past!")
        Reservation.objects.create(room_id=room, date=date, comment=comment)
        return redirect("/rooms")


def room_detail(request, id):
    """
    Show room details to user all reservations
    :param request:
    :param id:
    :return: view of site
    """
    if request.method == "GET":
        room = Room.objects.get(id=int(id))
        rese = room.reservation_set.get_queryset().order_by("date")
        return render(request, "Bookin_conference_room_app/room_details.html",
                      {
                          "room": room,
                          "res": rese
                      })


def make_reservation(request):
    """
    Make a reservation
    :param request:
    :return: Add reservationm to db
    """
    if request.method == "GET":
        rooms = Room.objects.all()
        return render(request, "Bookin_conference_room_app/shortcut_make_reservations.html",
                      {
                          "rooms": rooms,

                      })
    elif request.method == "POST":
        comment = request.POST["comment"]
        date = request.POST.get("date")
        room = Room.objects.get(id=request.POST["room"])
        reserv = room.reservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
        if Reservation.objects.filter(room_id=room, date=date):
            return HttpResponse("Room is busy in that day choose other day!")
        if date < str(datetime.date.today()):
            return HttpResponse("Data from past!")
        Reservation.objects.create(room_id=room, date=date, comment=comment)
        return redirect("/rooms")


def search_room(request):
    """
    Simple search
    :param request:
    :return: list of rooms with choosen parm
    """
    name = request.GET.get("name")
    set = request.GET.get("sets")
    set = int(set) if set else 0
    projector = request.GET.get("projector")
    rooms = Room.objects.all()
    if projector:
        rooms = rooms.filter(projector=bool(projector))
    if set:
        rooms = rooms.filter(sets__contains=set)
    if name:
        rooms = rooms.filter(name__contains=name)
    return render(request, "Bookin_conference_room_app/list_of_search.html", context={"rooms": rooms, "date": datetime.date.today()})
