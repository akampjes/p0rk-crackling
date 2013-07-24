from models import Job,Log
import socket



def pollJobServer(js):
	x = js.xmlrpc()
	try:
		jl = x.listJobs()
		
		jobs = {}
		for j in jl:
			jr = x.jobStatus(j[0])
			try:
				job = Job.objects.get(pk=jr["refid"])
				if job.jobServer != js:
					Log(line="Got job status from %s with jobrefid %d, but job is on %s" % (js, jr["refid"], job.jobServer)).save()
				else:
					job.speed = jr["speed"]
					job.progress = jr["progress_pc"]
					job.started = jr["started"]
					job.finished = jr["finished"]
					job.status = jr["state"]
					
					
					if jr["finished"] == None:
						d,h,m,s = jr["estimated"].split(":")
						td = datetime.timedelta(days=d, hours=h, mins=m, seconds=s)
						job.eta = job.started + td
					
					for h,p in jr["cracked"]:
						job.addCrack(h,p)
				
			except Job.DoesNotExist:
				Log(line="Got job status from %s with nonexistant refid: %s" % (js, jr)).save()
			
	except socket.error:
		js.changeStatus("Offline", "Socket error during job poll")
	
