from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.core.context_processors import csrf
from models import *
from forms import *
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
import urlparse

from djcelery import celery
import string
import datetime

import jobhelper

@dajaxice_register
def updateJobs(req):
	dajax = Dajax()

	out = render_to_string("jobs.html", dict(jobs=Job.objects.all().order_by('-started')))

	dajax.assign('#jobsHole','innerHTML', out)
	return dajax.json()
		

@dajaxice_register
def attackParams(request, atid=''):
	dajax = Dajax()

	if atid != '':
		at = get_object_or_404(AttackType, pk=atid)
		out = render_to_string("jobparamform.html", dict(at=at))
	else:
		out = ""

	dajax.assign('#jobParamFormHole','innerHTML', out)
	return dajax.json()

@dajaxice_register
def deleteJob(request, jobid):
	dajax = Dajax()
	print "delete job " + str(jobid)
	job = Job.objects.get(id=int(jobid)).delete()
	dajax.remove("#job"+str(jobid))
	return dajax.json()

@dajaxice_register
def cancelJob(request, jobid):
	dajax = Dajax()
	print "cancel job " + str(jobid)
	job = Job.objects.get(id=int(jobid))
	jobtasks = JobTask.objects.filter(job__exact=jobid).exclude(taskstatus__exact='Finished')
	control = celery.control
	print str(control)
	print 'passed control'
	for task in jobtasks:
		print "revoking %s" % task.taskid
		control.revoke(task.taskid, tereminate=True)
	job.status = 'Finished'
	job.save()
	dajax.script("Dajaxice.porkweb.updateJobs(Dajax.process)")
	return dajax.json()

@dajaxice_register
def addJob(request, form=None):
	dajax = Dajax()
	x = {}
	for k,v in urlparse.parse_qs(form).iteritems():
		x[k] = v[0]
	form = x		

	print form
	ajf = JobForm(form)
	params = {}
	for k,v in form.iteritems():
		if k.startswith("attackParam_"):
			params[k] = v
	print params
	if ajf.is_valid():
		#saving all the params to the database
		dajax.script("$('#addJobModal').modal('hide')")
		job = ajf.save()
		for n,v in params.iteritems():
			job.params.create(name=k,value=v)
		#need some codez to setup our job
		hashes = form['hashes'].split()
		hashtype =	HashType.objects.get(pk=int(form['hashType']))
		if 'attackParam_Charset' in params:
			charset = jobhelper.gen_charset(params['attackParam_Charset'])
		if len(hashes) == 1 and hashtype.ocllite == True and True:
			print "use ocllite"
			jobhelper.add_job_ocllite(job, charset, int(params['attackParam_maxLen']), int(params['attackParam_minLen']), hashtype.name, 'bruteforce', hashes)
			job.started = datetime.datetime.today()
			job.hashesCount = len(hashes)
			job.crackedCount = 0
			job.save()
		elif len(hashes) > 1 and hashtype.oclplus == True and False:
			#disabled
			#waiting for the lastest version of oclplus and the structure documentation to simulate a resume
			#instead of generating masks
			print "use oclplus"
		elif len(hashes) > 0 and hashtype.hashcat == True:
			print "use hashcat"
			jobhelper.add_job_hashcat(job, charset, int(params['attackParam_maxLen']), int(params['attackParam_minLen']), hashtype.name, 'bruteforce', hashes)
			job.started = datetime.datetime.today()
			job.hashesCount = len(hashes)
			job.crackedCount = 0
			job.save()
		else:
			print "Not supported."

		dajax.script("Dajaxice.porkweb.updateJobs(Dajax.process)")
	else:
		#dajax.remove_css_class('#addJobModal .controlgroup','error')
		for error in ajf.errors:
			#dajax.add_css_class('#%s_cg' % error,'error')
			dajax.script("$('#%s_cg').addClass('error')" % error)

	return dajax.json()
	
