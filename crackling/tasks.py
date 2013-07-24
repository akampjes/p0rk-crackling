from __future__ import absolute_import

#from crackling.celery import celery
import crackling.celery

import time
import logging

from crackling.hashcatjob import HashCatJob
from crackling.ocllitejob import OclLiteJob


@crackling.celery.celery.task
def newjob(engine, hashtype, attacktype, hashes, params):
	logging.info("Job starting")
	logging.debug(str(hashtype))
	logging.debug(str(attacktype))
	logging.debug(str(hashes))
	logging.debug(str(params))
	if engine == 'hashcat':
		j = HashCatJob()
		j.setHashType(hashtype)
		j.setAttackType(attacktype)
		j.setParams(params)
		j.addHashes(hashes)
		j.start()
	elif engine == 'ocllite':
		j = OclLiteJob()
		j.setHashType(hashtype)
		j.setAttackType(attacktype)
		j.setParams(params)
		j.addHashes(hashes)
		j.start()
	else:
		logging.critical("Unrecognised engine: %s" % engine)
		return None

	while j.status()['state'] != 'Finished':
		logging.debug("Job Status: %s" % j.status()['state'])
		time.sleep(2)
	logging.info("Job finished")
	result = j.status()
	logging.debug("Job Results: %s" % str(result))

	return result

