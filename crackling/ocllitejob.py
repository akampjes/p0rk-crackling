import os.path
import logging
import string
import tempfile

from job import Job

import crackling.config as config

class OclLiteJob(Job):
	hashTypes = {"MD5":0}
	path = config.OCLLITE_PATH
	validParams = ["minlen", "maxlen", "charset", "threads"]
	MSG_STATUS = "\n"

	def validateParams(self, params):
		for k,v in params.iteritems():
			if k == "charset":
				for c in v:
					if c not in string.printable:
						raise ValueError("Param 'charset' has non printable character 0x%02x, which, uh, I dont wanna stick into some argv" % ord(c))

	def getCommandLine(self):
		c = [self.path, "-m%d" % self.hashType]
		c.append("--pw-min=%d" % self.params["minlen"])
		c.append("--pw-max=%d" % self.params["maxlen"])
		c.append("--pw-skip=%d" % self.params['skip'])
		c.append("--pw-limit=%d" % self.params['limit'])
		try:
			c.append('-1 "%s"' % self.params['one'])
		except:
			logging.debug("no custom charsets for us")
		c.append(self.hashes[0])	#ocllite there is only one hash
		c.append(self.params['mask'])
		logging.debug("Command string %s" % str(c))
		return c
	
	def processLines(self, lines):
		for l in lines:
			for h in self.hashes:
				if l.startswith(h):
					self.stat['cracked'][h] = l.split(':',1)[1]
					logging.info("Cracked %s:%s" % (h, str(self.stat['cracked'][h])))


