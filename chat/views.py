from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chatroom, Message
from .forms import ChatroomForm, MessageForm


@login_required
def create_chatroom(request):
    if request.method == 'POST':
        form = ChatroomForm(request.POST)
        if form.is_valid():
            chatroom = form.save(commit=False)
            chatroom.creator = request.user
            chatroom.save()
            messages.success(request, 'Chatroom created successfully')
            return redirect('chatroom_list')
    else:
        form = ChatroomForm()
    return render(request, 'chat/create_chatroom.html', {'form': form})


@login_required
def chatroom_list(request):
    chatrooms = Chatroom.objects.all()
    return render(request, 'chat/chatroom_list.html', {'chatrooms': chatrooms})


@login_required
def send_message(request, chatroom_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chatroom = Chatroom.objects.get(id=chatroom_id)
            message.user = request.user
            message.save()
            return redirect('chatroom', chatroom_id=chatroom_id)
    else:
        form = MessageForm()
    return render(request, 'chat/send_message.html', {'form': form, 'chatroom_id': chatroom_id})


@login_required
def chatroom(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    messages = Message.objects.filter(chatroom=chatroom)
    return render(request, 'chat/chatroom.html', {'chatroom': chatroom, 'messages': messages})


@login_required
def delete_chatroom(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    if chatroom.creator == request.user:
        chatroom.delete()
        messages.success(request, 'Chatroom deleted successfully')
        return redirect('chatroom_list')
    else:
        messages.error(request, 'You are not authorized to delete this chatroom')
        return redirect('chatroom_list')
