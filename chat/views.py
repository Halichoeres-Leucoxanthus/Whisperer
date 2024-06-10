from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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
            return JsonResponse({'success': True, 'message': 'Chatroom created successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid method'})


@login_required
def chatroom_list(request):
    chatrooms = Chatroom.objects.all().values('id', 'name')  # Query only required fields
    return JsonResponse({'success': True, 'chatrooms': list(chatrooms)})


@login_required
def send_message(request, chatroom_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chatroom_id = chatroom_id
            message.user = request.user
            message.save()
            return JsonResponse({'success': True, 'message': 'Message sent successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid method'})


@login_required
def chatroom(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    messages = Message.objects.filter(chatroom=chatroom).values('text', 'user__username')  # Query only required fields
    return JsonResponse({'success': True, 'chatroom': chatroom.name, 'messages': list(messages)})


@login_required
def delete_chatroom(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    if chatroom.creator == request.user:
        chatroom.delete()
        return JsonResponse({'success': True, 'message': 'Chatroom deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'You are not authorized to delete this chatroom'})
