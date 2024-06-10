from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chatroom
from .forms import ChatroomForm


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
