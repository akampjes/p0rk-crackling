import os.path
import logging
import string
import tempfile

from job import Job

import crackling.config as config

class HashCatJob(Job):
	hashTypes = {"MD5":0}
	path = config.HASHCAT_PATH
	validParams = ["minlen", "maxlen", "charset", "threads"]
	MSG_STATUS = "\n"

	def validateParams(self, params):
		for k,v in params.iteritems():
			if k == "charset":
				for c in v:
					if c not in string.printable:
						raise ValueError("Param 'charset' has non printable character 0x%02x, which, uh, I dont wanna stick into some argv" % ord(c))

	def getCommandLine(self):
		c = [self.path, "-a%d" % self.attackType, "-m%d" % self.hashType]
		c.append("--disable-potfile")
		if self.attackType == self.attackTypes["bruteforce"]:
			c.append("--pw-min=%d" % self.params["minlen"])
			c.append("--pw-max=%d" % self.params["maxlen"])
		try:
			c.append('-1 %s' % self.params['one'])
			if 'two' in self.params:
				c.append('-2 %s' % self.params['two'])
				if 'three' in self.params:
					c.append('-3 %s' % self.params['three'])
					if 'four' in self.params:
						c.append('-4 %s' % self.params['four'])
		except:
			logging.critical("no custom charsets for us")
		# Write hashes down to a tempfile
		f = tempfile.NamedTemporaryFile(delete=False)
		for h in self.hashes:
			f.write(h + "\n")
		f.flush()
		c.append(f.name)
		# Keep it open with a handle, it'll get deleted when we get destroyed.
		self.ftmp = f
		c.append(self.params['mask'])
		logging.debug("Command string %s" % str(c))
		return c
	
	def processLines(self, lines):
		for l in lines:
			for h in self.hashes:
				if l.startswith(h):
					self.stat['cracked'][h] = l.split(':',1)[1]
					logging.info("Cracked %s:%s" % (h, str(self.stat['cracked'][h])))


