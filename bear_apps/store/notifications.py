""" Methods for managing user notification system. """
from store.models import Notification

MESSAGES = {
    'request': ' has requested a license for ',
    'approve': 'Your request has been approved for ',
    'reject': 'Your request has been denied for ',
    'revoke': 'Your license has been revoked for ',
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

def add_Notification(user, app, code):
    """ Adds a new message to a User in the database.
            args:
            user = a User object
            app = an App object (NOT a UserApp object)
            code = a key to one of the predefined message above.
        returns nothing
    """
    if code == 'request':
        message = user.Name + MESSAGES[code] + app.app_name
    elif code == 'approve' or code == 'reject' or code == 'revoke':
        message = MESSAGES[code] + app.app_name

    notification = Notification(user=user, message=message, viewed=False)
    notification.user = user
    notification.save()
