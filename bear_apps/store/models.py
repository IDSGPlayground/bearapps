from django.db import models

# Create your models here.
# There is a many-to-one relationship between the users and the app.
# Each user is realted to the app, and the user carries along the state (requested,
# downloadable, etc) of their specific app
# class User(models.Model):
# 	name=models.CharField(max_length=200)
# 	SID=models.IntegerField()
# 	accepted_user=models.ForeignKey('Apps')
# 	state=models.CharField(max_length=200)
# 	def __unicode__(self):
# 		return self.name+", "+str(self.SID)+", "+self.state

# class Apps(models.Model):
# 	name=models.CharField(max_length=200)
# 	def __unicode__(self):
# 		return self.name

class User(models.Model):
	name=models.CharField(max_length=200)
	SID=models.IntegerField()
	# groups=models.ForeignKey('AdminUser')
	# PI=models.CharField(max_length=200)
	# accepted_user=models.ForeignKey('Apps')
	
	def __unicode__(self):
		return self.name+", "+str(self.SID)

class Apps(models.Model):
	accepted_app=models.ForeignKey('User')
	name=models.CharField(max_length=200)
	state=models.CharField(max_length=200)
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
