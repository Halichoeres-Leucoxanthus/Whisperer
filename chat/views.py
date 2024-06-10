from .models import Chatroom, Message
import json
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def get_available_users(request):
    users = User.objects.filter(is_superuser=False).values('id', 'username')
    return JsonResponse({'success': True, 'users': list(users)})


@csrf_exempt
@login_required
def create_chatroom(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        chatroom_name = data.get('name')
        chatroom_description = data.get('description')
        chatroom_type = data.get('type')
        chatroom_users = data.get('users')

        # Ensure the creator is included in the users list for private chatrooms
        if chatroom_type == 'private':
            chatroom_users.append(request.user.id)

        # Create chatroom
        chatroom = Chatroom.objects.create(
            name=chatroom_name,
            description=chatroom_description,
            creator=request.user,
            type=chatroom_type
        )

        # Add users to the chatroom
        chatroom.users.add(*chatroom_users)

        return JsonResponse({'success': True, 'message': 'Chatroom created successfully'})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid method'})


@login_required
def chatroom_list(request):
    # Fetch chatrooms for the user
    chatrooms = Chatroom.objects.filter(Q(type='global') | Q(creator=request.user) | Q(users=request.user)).distinct()
    chatroom_data = [{'id': chatroom.id, 'name': chatroom.name, 'type': chatroom.type} for chatroom in chatrooms]
    return JsonResponse({'success': True, 'chatrooms': chatroom_data})


@login_required
def chatroom(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    messages = Message.objects.filter(chatroom=chatroom).values('text', 'user__username')
    return JsonResponse({'chatroom': chatroom.name, 'messages': list(messages)})


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
def delete_chatroom(request, chatroom_id):
    chatroom = Chatroom.objects.get(id=chatroom_id)
    if chatroom.creator == request.user:
        chatroom.delete()
        return JsonResponse({'success': True, 'message': 'Chatroom deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'You are not authorized to delete this chatroom'})
