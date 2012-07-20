from django.db import models

app_status=(('AVAILABLE', 'AVAILABLE'),
	('REQUESTED','REQUESTED'),
	('DOWNLOADABLE' , 'DOWNLOADABLE'),
	('UPDATES AVAILABLE', 'UPDATES AVAILABLE'))

class User(models.Model):
	name = models.CharField(max_length=200)
	password = models.CharField(max_length=200)
	SID = models.IntegerField()
	owner = models.BooleanField()
	groups = models.ForeignKey('Group')
	notifications = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name + ", " + str(self.SID)

class User_Apps(models.Model):
	user = models.ForeignKey('User')
	app_name = models.CharField(max_length=200)
	available=models.BooleanField(default=True)
	requested=models.BooleanField()
	downloadable=models.BooleanField()
	href_name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.app_name

class App(models.Model):
	app_name = models.CharField(max_length=200)
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

class Notification(models.Model):
	user = models.ForeignKey('User')
	message = models.CharField(max_length=200)

	def __unicode__(self):
		return self.message