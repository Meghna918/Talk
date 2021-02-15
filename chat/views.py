from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })
