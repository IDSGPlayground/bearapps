from django.db import models

# Create your models here.
# There is a many-to-one relationship between the users and the app.
# Each user is realted to the app, and the user carries along the state (requested,
# downloadable, etc) of their specific app
class User(models.Model):
	name=models.CharField(max_length=200)
	SID=models.IntegerField()
	accepted_user=models.ForeignKey('Apps')
	state=models.CharField(max_length=200)
	def __unicode__(self):
		return self.name+", "+str(self.SID)+", "+self.state

class Apps(models.Model):
	name=models.CharField(max_length=200)
	def __unicode__(self):
		return self.name
