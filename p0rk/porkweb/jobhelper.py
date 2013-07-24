import string
from models import *
from djcelery import celery


def gen_mask(charset, maxlen):
    TUNING = 16 #change this to create larger groups
    l = []
    one = charset
    two = ''
    three = ''
    four = ''
    onemask = '?1' * (maxlen -3)
    customs = [charset[i:i+TUNING] for i in range(0, len(charset), TUNING)]

    for i in range(0, len(customs)):
        for j in range(0, len(customs)):
            for k in range(0, len(customs)):
                l.append({'1': one, '2': customs[i], '3': customs[j], '4': customs[k], 'mask': onemask+'?2?3?4'})

    return l

def gen_charset(charsetname):
	charset = ''                                                                                       
	whitespace = ' '
	if charsetname == 'Lower':
		charset += string.ascii_lowercase + whitespace
	elif charsetname == 'Upper':
		charset += string.ascii_uppercase + whitespace
	elif charsetname == 'Alpha':
		charset += string.ascii_letters + whitespace
	elif charsetname == 'Num':
		charset += string.digits
	elif charsetname == 'AlphaNum':
		charset += string.digits + string.ascii_letters + whitespace
	elif charsetname == 'AlphanumPunc':
		charset += string.digits + string. ascii_letters + string.punctuation + whitespace
	else:
		return None
	return charset

def add_job_hashcat(job, charset, maxlen, minlen, hashtype, attacktype, hashes):
	tooeasy = 4
	for i in range(minlen, maxlen+1):
		if i <= tooeasy:
			print "too easy"
			retval = celery.send_task('crackling.tasks.newjob', ['hashcat', hashtype, attacktype, hashes, dict(minlen=i, maxlen=i, charset=charset, one=charset, mask='?1'*i)], queue='crackling')
			jobtask = JobTask(job=job, taskid=retval)
			jobtask.save()
			print "***task sent*** %s" % str(retval)
		else:
			masks = gen_mask(charset, i)
			for mask in masks:
				retval = celery.send_task('crackling.tasks.newjob', ['hashcat', hashtype, attacktype, hashes, dict(minlen=i, maxlen=i, charset=charset, one=mask['1'], two=mask['2'], three=mask['3'], four=mask['4'], mask=mask['mask'])], queue='crackling')
				jobtask = JobTask(job=job, taskid=retval)
				jobtask.save()
				print "***task sent*** %s" % str(retval)

def add_job_ocllite(job, charset, maxlen, minlen, hashtype, attacktype, hashes):
	ocllitework = 1000000000
	for i in range(minlen, maxlen+1):
		numcombinations = len(charset) ** i
		skip = 0
		limit = 0
		while skip < numcombinations:
			if (limit + ocllitework) > numcombinations:
				limit = numcombinations
			else:
				limit += ocllitework
			print "min,max %d skip %d limit %d mask %s" % (i, skip, limit, ('?1'*i))
			retval = celery.send_task('crackling.tasks.newjob', ['ocllite', hashtype, attacktype, hashes, dict(minlen=i, maxlen=i, one=charset, mask=('?1'*i), skip=skip, limit=limit)], queue='crackling')
			jobtask = JobTask(job=job, taskid=retval)
			jobtask.save()
			print "***task sent*** " + str(retval)
			skip = limit

