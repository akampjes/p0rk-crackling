# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.context_processors import csrf
from models import *
from forms import *
import ajax

def front(req, jobid=None):
	rv = {}
	rv.update(csrf(req))
	#rv["servers"] = JobServer.objects.all()
	rv["jobs"] = Job.objects.all().order_by('-started')
	rv["addJobForm"] = JobForm()
	if jobid != None:
		rv['cracked'] = Cracked.objects.filter(job__exact=jobid).order_by('-when')
	else:
		rv['cracked'] = Cracked.objects.all().order_by('-when')
	if jobid != None:
		rv['jobid'] = int(jobid)
	return render_to_response("front.html", rv, context_instance=RequestContext(req))
