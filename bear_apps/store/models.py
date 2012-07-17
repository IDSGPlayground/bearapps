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
class Description(models.Model):
	app_name=models.CharField(max_length=200)
	# Matlab_descriptions={"Description": "MATLAB is a programming environment for algorithm development, data analysis, visualization, and numerical computation. Using MATLAB, you can solve technical computing problems faster than with traditional programming languages, such as C, C++, and Fortran.You can use MATLAB in a wide range of applications, including signal and image processing, communications, control design, test and measurement, financial modeling and analysis, and computational biology. For a million engineers and scientists in industry and academia, MATLAB is the language of technical computing.",
	# 				"System Requirements":"Windows: Windows 7 SP1, Vista SP 2, XP SP3, XP x64 Edition SP2, Server 2008 SP2 or R2, Server 2003 R2 SP2. Any Intel or AMD x86 processor supporting SSE2 instruction set. 1 GB for MATLAB only, 3-4 GB for typical installations. At least 1 GB RAM.\n\nLinux: Qualified Distributions: Ubuntu 10.4 LTS, 11.04, 11.10. Red Hat Enterprise Linux 5.x and 6.x. SUSE Linux Enterprise Desktop 11.x. Debian 6.x. Any Intel or AMD x86 processor supporting SSE2 instruction set. 1 GB for MATLAB only, 3-4 GB for a typical installation. At least 1 GB RAM.\n\nMac: Mac OS X 10.7 (Lion) or 10.6.4+ (Snow leopard). All Intel-based Macs with an Intel Core 2 or later. 1 GB for MATLAB only, 3-4 GB for a typical installation. At least 1 GB RAM.",
	# 				"How to Obtain":"Currently available by chart string owner only. Use the request button above to request a copy. Purchasing options are available direct from vendor"}
	Description=models.CharField(max_length=1000)
	Sysreq_windows=models.CharField(max_length=1000)
	Sysreq_linux=models.CharField(max_length=1000)
	Sysreq_mac=models.CharField(max_length=1000)
	obtain=models.CharField(max_length=1000)
	def __unicode__(self):
		return self.app_name
