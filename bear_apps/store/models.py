from django.db import models


class User(models.Model):
	name = models.CharField(max_length=200)
	SID = models.IntegerField()
	password = models.CharField(max_length=200)
	owner = models.BooleanField()
	# groups=models.ForeignKey('AdminUser')
	# PI=models.CharField(max_length=200)
	# accepted_user=models.ForeignKey('Apps')
	
	def __unicode__(self):
		return self.name + ", " + str(self.SID)

class User_Apps(models.Model):
	accepted_app = models.ForeignKey('User')
	name = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name+", "+self.state
	def change_state(self):
		if self.state.upper()=="REQUESTED":
			self.state="downloadable"
		elif self.state.upper()=="UNAVAILABLE":
			self.state="requested"

#This will be implemented when we get the PI part done
# class AdminUser(models.Model):
# 	name=models.charField(max_length=200)
# 	ID=models.IntegerField()
# 	def __unicode__(self):
# 		return self.name+", "+str(self.ID)

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
