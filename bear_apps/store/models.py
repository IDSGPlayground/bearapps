"""The database models used for Bearapps. The models describe
the app, users, groups, charstrings, and notifications used
within the store."""

from django.db import models

app_status = (
    ('AVAILABLE', 'AVAILABLE'),
    ('REQUESTED', 'REQUESTED'),
    ('APPROVED', 'APPROVED'),
    ('UPDATES', 'UPDATES'),
)

user_types = (
    ('GENERAL', 'GENERAL'),
    ('ADMIN', 'ADMIN'),
    ('MANAGER', 'MANAGER')
)


class User(models.Model):
    """ Model to describe all users of bearapps, contains the
        user's name, SID, password, group(s) the user is associated
        with, and the user type (either user, manager, or admin).
    """

    name = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    SID = models.IntegerField(unique=True)
    user_type = models.CharField(max_length=10, choices=user_types)
    groups = models.ManyToManyField('Group', null=True, blank=True)

    def __unicode__(self):
        return self.name


class User_Apps(models.Model):
    """ Model to describe the apps that a user has requested. Contains
        information about the user requesting the app, the status (either
        'available', 'requested', or 'downloadable'), the date accepted,
        and group and chartstring associated with an accepted app.
    """

    user = models.ForeignKey('User')
    app = models.ForeignKey('App')
    chartstring = models.ForeignKey('Chartstring', null=True, blank=True)
    group = models.ForeignKey('Group', null=True, blank=True)
    date = models.DateField('Date Accepted', null=True, blank=True)
    status = models.CharField(max_length=20, choices=app_status)

    def __unicode__(self):
        return ('User: ' + self.user.name + '\nApp Name: ' +
            self.app.app_name + '\nStatus: ' + self.status)


class App(models.Model):
    """ Model that provides the information about an app. Contains information
        such as the name, price, system requirements, the href name, and how
        to obtain it.
    """

    app_name = models.CharField(max_length=200, unique=True)
    href_name = models.CharField(max_length=200, unique=True)
    price = models.IntegerField()
    description = models.TextField(max_length=1000)
    windows = models.TextField(max_length=1000)
    linux = models.TextField(max_length=1000)
    mac = models.TextField(max_length=1000)
    obtain = models.TextField(max_length=1000)

    def __unicode__(self):
        return self.app_name


class Group(models.Model):
    """ Model that describes the group a user is in,
        includes the name of the group.
    """

    name = models.CharField(max_length=200, unique=True)

    def __unicode__(self):
        return self.name


class Chartstring(models.Model):
    """ Model that describes a chartstring. It includes the name, chartstring
        number, the group and owner it is associated with, the initial budget,
        and how much of the budget remains.
    """

    nickname = models.CharField(max_length=200, default='', unique=True)
    chartstring = models.CharField(max_length=200, default='', unique=True)
    manager = models.ForeignKey('User')
    group = models.ForeignKey('Group')
    budget = models.IntegerField()
    remaining = models.IntegerField()

    def __unicode__(self):
        return self.nickname


class Notification(models.Model):
    """ Model that describes the notifications a user recieves, includes
        the user that it is directed to, the message body, the date received,
        and whether the message has been viewed.
    """
    user = models.ForeignKey('User')
    message = models.CharField(max_length=200)
    viewed = models.BooleanField()
    date = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return self.message
