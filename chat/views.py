import socket
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from chat.models import ChatRoom
from django.contrib.sessions.backends.db import SessionStore

def index(request):
    context = {
        'chats': ChatRoom.objects.order_by('name')[:5]
    }
    return render(request, 'chat/index.html', context)

def chat_room(request, chat_room_id):
    context = {
        'chat': get_object_or_404(ChatRoom, pk=chat_room_id)
    }
    return render(request, 'chat/chat_room.html', context)

def longpoll_chat_room(request, chat_room_id):
    context = {
        'chat': get_object_or_404(ChatRoom, pk=chat_room_id)
    }
    return render(request, 'chat/longpoll_chat_room.html', context)
