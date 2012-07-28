from django.db import models

app_status = (
    ('AVAILABLE', 'AVAILABLE'),
    ('REQUESTED','REQUESTED'),
    ('APPROVED' , 'APPROVED'),
    ('UPDATES AVAILABLE', 'UPDATES AVAILABLE'),
)

user_types = (('GENERAL', 'GENERAL'), ('ADMIN', 'ADMIN'), ('MANAGER', 'MANAGER'))

class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    SID = models.IntegerField()
    user_type = models.CharField(max_length=10, choices=user_types)
    groups = models.ManyToManyField('Group', null=True, blank=True)

    def __unicode__(self):
        return self.name

class User_Apps(models.Model):
    user = models.ForeignKey('User')
    app = models.ForeignKey('App')
    chartstring = models.ForeignKey('Chartstring', null=True, blank=True)
    group = models.ForeignKey('Group', null=True, blank=True)
    date = models.DateField(auto_now=True, auto_now_add=True)
    status = models.CharField(max_length=20, choices=app_status)

    def __unicode__(self):
        return "User: " + str(self.user.name) +  "\nApp Name: " + str(self.app.app_name) + "\nStatus: " + str(self.status)

class App(models.Model):
    app_name = models.CharField(max_length=200)
    href_name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(max_length=1000)
    windows = models.TextField(max_length=1000)
    linux = models.TextField(max_length=1000)
    mac = models.TextField(max_length=1000)
    obtain = models.TextField(max_length=1000)

    def __unicode__(self):
        return self.app_name

class Group(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class Chartstring(models.Model):
    nickname = models.CharField(max_length=200, default="")
    chartstring = models.CharField(max_length=200, default="")
    manager = models.ForeignKey('User')
    group = models.ForeignKey('Group')
    budget = models.IntegerField()
    remaining = models.IntegerField()

    def __unicode__(self):
        return self.nickname

class Notification(models.Model):
    user = models.ForeignKey('User')
    message = models.CharField(max_length=200)
    viewed = models.BooleanField()
    date = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return self.message
