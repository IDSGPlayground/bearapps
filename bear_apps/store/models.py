from django.db import models

app_status = (
    ('AVAILABLE', 'AVAILABLE'),
    ('REQUESTED','REQUESTED'),
    ('DOWNLOADABLE' , 'DOWNLOADABLE'),
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
        return self.name + ", " + str(self.SID)

class User_Apps(models.Model):
    user = models.ForeignKey('User')
    date = models.DateField(auto_now=True, auto_now_add=True)
    app_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=app_status)
    href_name = models.CharField(max_length=200)
    chartstring = models.ForeignKey('Chartstring', null=True, blank=True)
    group = models.ForeignKey('Group', null=True, blank=True)

    def __unicode__(self):
        return "Name: " + str(self.user.name) + "\nID:  " + str(self.user.SID)+ "\nApp Name: "+self.app_name

class App(models.Model):
    app_name = models.CharField(max_length=200)
    price = models.IntegerField()
    href_name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    Sysreq_windows = models.TextField(max_length=1000)
    Sysreq_linux = models.TextField(max_length=1000)
    Sysreq_mac = models.TextField(max_length=1000)
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
    group = models.ForeignKey('Group')
    budget = models.IntegerField()

    def __unicode__(self):
        return self.nickname

class Notification(models.Model):
    user = models.ForeignKey('User')
    message = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message
