import logging
import time
import threading
import datetime
import subprocess


class Job(object):
	STATE_NEW="New"
	STATE_PAUSED = "Paused"
	STATE_RUNNING = "Running"
	STATE_STOPPED= "Stopped"
	STATE_FINISHED = "Finished"
	STATE_ERROR= "Error"
	
	REQ_TERM="terminate"

	hashTypes = {} # Empty in this abstract baseclass
	attackTypes = {"bruteforce":3}

	def __init__(self):
		self.state = self.STATE_NEW 
		self.hashType = None
		self.hashes = []
		self.params = {}  
		self.attackType = None
		self.reqEvent = threading.Event()
		self.req = []
		self.jr = None
		self.stat = dict(cracked=dict(), started="", finished="")
	
	def setHashType(self, ht):
		if ht in self.hashTypes.keys():
			self.hashType = self.hashTypes[ht]
		else:
			raise ValueError("Invalid hashtype %s for %s" % (ht, self.__class__), ",".join(self.hashTypes.keys()))

	def setAttackType(self, at):
		if at in self.attackTypes.keys():
			self.attackType = self.attackTypes[at]
		else:
			raise ValueError("Invalid attacktype %s for %s, valid: %s" % (at, self.__class__, ",".join(self.attackTypes.keys())))
	
	def setParams(self, params):
		self.validateParams(params)
		self.params.update(params)

	def addHashes(self, hashes):
		self.hashes += hashes

	def reqReady(self):
		while self.reqEvent.is_set():
			time.sleep(0.1)
		
		logging.debug("%s: Ready to make request" % self)

	def send(self, req, param):
		logging.debug("%s: Attempting to send request: %s" % (self, (req, param)))
		self.reqReady()
		self.req = (req, param)
		self.reqEvent.set()
		logging.debug("%s: Sent request: %s" % (self, (req, param)))

	def status(self):
		self.stat['state'] = self.state
		return self.stat

	def processLines(self, lines):
		# gets a list of lines of output from the subprocess, parses them.	
		pass

	def jobRunner(self):
		self.state = self.STATE_RUNNING
		
		argv = self.getCommandLine()
		logging.debug("%s jobRunner thread invoking subprocess: %s" % (self, argv))
		jobp = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		
		self.stat["started"] = datetime.datetime.now()
		
		buf = ""
		lines = []
		
		logging.debug("%s jobRunner thread running subprocess" % (self))
		stdoutdata, stderrdata = jobp.communicate()	#get the results, wait for process to terminate
		logging.debug("%s jobRunner thread stdout:\n %s" % (self, stdoutdata))
		if stderrdata != None:
			logging.error("%s jobRunner thread stderr:\n %s" % (self, stderrdata))
		
		buf = stdoutdata
		if "\n" in buf:
			nl = buf.split("\n")
			if buf.endswith("\n"):
				buf = ""
			else:
				buf = nl[-1]
				nl = nl[:-1]
			lines += nl

		self.processLines(lines)

		if self.state == self.STATE_RUNNING:
			self.state = self.STATE_FINISHED

		self.stat["finished"] = datetime.datetime.now()
		logging.debug("%s jobRunner thread finished subprocess" % (self))


	def start(self):
		jr = threading.Thread(target=self.jobRunner)
		logging.debug("About to start %s" % (jr))
		jr.start()
		self.jr = jr
	
	def pause(self):
		pass

	def stop(self):
		if self.jr != None and self.jr.is_alive():
			self.send(self.REQ_TERM, None)
	
	def validateParams(self, params):
		pass

	def getCommandLine(self):
		pass
	
	def cleanUp(self):
		pass

	def __str__(self):
		return self.__class__.__name__


