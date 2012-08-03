""" Methods for managing user notification system. """
from store.models import Notification

MESSAGES = {
    'request': ' has requested a license for ',
    'approve': 'Your request has been approved for ',
    'reject': 'Your request has been denied for ',
    'revoke': 'Your license has been revoked for ',
    'new_user': ' has been added to ',
}


def get_Notifications(user):
    """ Retrieves all a user's current getNotifications.
            **each notification will have a unique primary key.
            args:
                user = a User object
            returns a list object of message strings.
    """
    messages = []
    try:
        messages = user.notification_set.all()
    except:
        pass
    return messages


def add_Notification(user, code, info):
    """ Adds a new message to a User in the database.
            args:
            user = a User object
            code = a key to one of the predefined message above.
            info = dictionary of information necesssary for message.
        returns nothing
    """
    if code == 'request':
        message = info['requestor'].name + MESSAGES[code] + info['app'].app_name
    elif code == 'approve' or code == 'reject' or code == 'revoke':
        message = MESSAGES[code] + info['app'].app_name
    elif code == 'new_user':
        message = info['requestor'].name + MESSAGES[code] + info['group'].name

    notification = Notification(user=user, message=message, viewed=False)
    notification.user = user
    notification.save()


def delete_Notifications(user):
    """ Deletes ALL messages for a user.
    """
    messages = get_Notifications(user)

    for message in messages:
        message.delete()
    user.notifications = 0
    user.save()
