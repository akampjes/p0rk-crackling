from django.db import models
import xmlrpclib

class JobServer(models.Model):
	STATUS_CHOICES = ["Offline", "Online", "Disabled"]

	ipaddr = models.IPAddressField(max_length=16)
	port = models.IntegerField(default=8117)
	hostname = models.CharField(max_length=255, blank=True)
	os = models.CharField(max_length=32)
	status = models.CharField(max_length=16, choices=[(x,x) for x in STATUS_CHOICES], default="Offline")
	details = models.CharField(max_length=255, blank=True)

	def changeStatus(status, reason=""):
		js.status = status
		js.save()
		Log("%s went %s (%s)" % (self, self.status, reason)).save()

	def __unicode__(self):
		return "Jobserver %s:%d" % (self.ipaddr, self.port)

	def xmlrpc(self):	
		return xmlrpclib.ServerProxy("http://%s:%d"  % (self.ipaddr, self.port))	

class AttackType(models.Model):
	name = models.CharField(max_length=64)
	notes = models.TextField(blank=True)
	
	def __unicode__(self):
		return self.name
	

class Param(models.Model):
	name = models.CharField(max_length=64)
	value = models.CharField(max_length=64)
	
	def __unicode__(self):
		return "%s: %s" % (self.name, self.value)

class AttackParam(Param):
	attack = models.ForeignKey("AttackType", related_name="params")
	
class JobParam(Param):
	job = models.ForeignKey("Job", related_name="params")

class AttackCharset(models.Model):
	attack = models.ForeignKey('AttackType', related_name='charsets')
	name = models.CharField(max_length=64, default='Charset')
	#CHARSET_CHOICES = ['Lower', 'Upper', 'Alpha', 'Num', 'AlphaNum', 'AlphaNumPunc']
	#charset = models.CharField(max_length=16, choices=[(x,x) for x in CHARSET_CHOICES], default='AlphaNum')
	CHARSET_CHOICES = ['Lower', 'Upper', 'Alpha', 'Num', 'AlphaNum', 'AlphaNumPnuc']
	charset = models.CharField(max_length=16, choices=[(x,x) for x in CHARSET_CHOICES], default='AlphaNum')

class HashType(models.Model):
	name = models.CharField(max_length=32)
	hashcatType = models.IntegerField(blank=True, null=True)
	hashcat = models.BooleanField()
	ocllite = models.BooleanField()
	oclplus = models.BooleanField()

	def __unicode__(self):
		return self.name

class Cracked(models.Model):
	when = models.DateTimeField()
	hash = models.CharField(max_length=255)
	value = models.CharField(max_length=255)
	job = models.ForeignKey("Job")

class JobTask(models.Model):
	job = models.ForeignKey('Job')
	taskid = models.CharField(max_length=36)	#task UUID (36chars, 4 of which are dashes)
	STATUS_CHOICES = ['New', 'Paused', 'Running', 'Stopped', 'Finished', 'Error']
	taskstatus = models.CharField(max_length=16, choices=[(x,x) for x in STATUS_CHOICES], default='New')
	taskresults = models.TextField(blank=True)

class Job(models.Model):
	STATUS_CHOICES =["New", "Queued", "Running", "Paused", "Cancelled", "Finished", "Error"]
	hashes = models.TextField(help_text="Paste in your hashes...")
	hashType = models.ForeignKey("HashType")
	attackType = models.ForeignKey("AttackType")
	jobServer = models.ForeignKey("JobServer",null=True, blank=True)
	status = models.CharField(max_length=16, choices=[(x,x) for x in STATUS_CHOICES], default="New")
	progress = models.FloatField(default=0)
	started = models.DateTimeField(blank=True, null=True)
	finished = models.DateTimeField(blank=True, null=True)
	eta = models.DateTimeField(blank=True, null=True)	#currently unused
	results = models.TextField(blank=True)
	speed = models.IntegerField(blank=True, null=True)	#currently unused
	hashesCount = models.IntegerField(blank=True, null=True)
	crackedCount = models.IntegerField(blank=True, null=True)

	def addCrack(self, h, p):
		if h not in self.hashes:
			Log("%s got addCrack called with a hash that wasnt in its hashlist. %s:%s" % (h, p)).save()
		
		if len(self.cracked.objects.filter(hash=h)) == 0:
			self.cracked.create(hash=h, value=p)

class Log(models.Model):
	when = models.DateTimeField(auto_now=True)
	line = models.TextField()

