#from celery import task
import celery
from porkweb import models

import datetime

@celery.task(ignore_result=True)
def processresults():
	tasks = models.JobTask.objects.exclude(taskstatus__exact='Finished')
	for t in tasks:
		result = celery.result.AsyncResult(t.taskid)
		if result.status == 'SUCCESS':
			res = result.get()
			print res

			if 'cracked' in res and len(res['cracked']) > 0:
				for k,v in res['cracked'].iteritems():
					crack = models.Cracked(hash=k,value=v,job=t.job, when=datetime.datetime.today())
					crack.save()
			t.taskstatus = 'Finished'
			t.save()

			numhashes = t.job.hashesCount
			numcracked = t.job.crackedCount = len(models.Cracked.objects.filter(job__exact=t.job))
			if numcracked >= numhashes:	#finished cracking all the hashes, cancel the tasks in progress
				torevoke = (models.JobTask.objects.filter(job__exact=t.job)
						.exclude(taskstatus__exact='Finished'))
				control = celery.app.control.Control()
				for x in torevoke:
					print 'revoking %s' % x.taskid
					control.revoke(x.taskid, terminate=True)
				t.job.status = 'Finished'
				t.job.finished = datetime.datetime.today()
				t.job.save()

			totaltasks = len(models.JobTask.objects.filter(job__exact=t.job))
			finishedtasks = len(models.JobTask.objects.filter(job__exact=t.job)
					.filter(taskstatus__exact='Finished'))
			if finishedtasks == totaltasks:	#all tasks are finished
				t.job.status = 'Finished'
				t.job.finished = datetime.datetime.today()
				t.job.save()
			t.job.progress = (float(finishedtasks) / float(totaltasks)) * 100.0
			t.job.save()
			#t.delete()	#we delete the finished task after extracting any cracked hashes
