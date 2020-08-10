from inloop.medics.models import Notification


def pull_notifications(request):
    if request.is_ajax() or not request.user.is_authenticated:
        return {}
    notification_queryset = Notification.objects.filter(user=request.user, was_read=False)
    notifications = list(notification_queryset)
    notification_queryset.update(was_read=True)
    return {'notifications': notifications}
