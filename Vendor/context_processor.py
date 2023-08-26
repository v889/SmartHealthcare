from django.contrib import messages

def notification_count(request):
    return {
        'notification_count': len(messages.get_messages(request)),
    }
