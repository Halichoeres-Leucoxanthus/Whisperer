from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Chatroom, Message


@login_required
def create_chatroom(request):
    if request.method == 'POST':
        chatroom_name = request.POST.get('name')
        chatroom_description = request.POST.get('description')

        # Create chatroom
        chatroom = Chatroom.objects.create(name=chatroom_name, description=chatroom_description, creator=request.user)
        return JsonResponse({'success': True, 'message': 'Chatroom created successfully'})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid method'})



@login_required
def chatroom_list(request):
    chatrooms = Chatroom.objects.all().values('id', 'name')
    return JsonResponse({'success': True, 'chatrooms': list(chatrooms)})


@login_required
def send_message(request, chatroom_id):
    if request.method == 'POST':
        message_text = request.POST.get('text')

        # Create message
        message = Message.objects.create(text=message_text, chatroom_id=chatroom_id, user=request.user)
        return JsonResponse({'success': True, 'message': 'Message sent successfully'})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid method'})


@login_required
def chatroom(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    messages = Message.objects.filter(chatroom=chatroom).values('text', 'user__username')
    return JsonResponse({'success': True, 'chatroom': chatroom.name, 'messages': list(messages)})


@login_required
def delete_chatroom(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    if chatroom.creator == request.user:
        chatroom.delete()
        return JsonResponse({'success': True, 'message': 'Chatroom deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'You are not authorized to delete this chatroom'})
