from inloop.medics.models import Notification


def pull_notifications(request):
    if request.is_ajax or not request.user.is_authenticated:
        return {}
    notifications = Notification.objects.filter(user=request.user, was_read=False)
    notifications.update('was_read', True)
    print(notifications)
    return {
        'notifications': notifications
    }
