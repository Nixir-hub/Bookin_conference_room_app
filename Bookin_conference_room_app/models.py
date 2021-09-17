from django.db import models


# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255)
    sets = models.PositiveIntegerField()
    projector = models.BooleanField(default=False)
    def __str__(self):
        return self.name


class Reservation(models.Model):
    date = models.DateField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    def __str__(self):
        return self.room_id


    class Meta:
        unique_together = ('room_id', 'date',)
