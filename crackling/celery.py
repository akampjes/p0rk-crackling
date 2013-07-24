from __future__ import absolute_import

import sys
import logging

from celery import Celery

import crackling.config as config

CELERY_TRACK_STARTED = True

celery = Celery('crackling.celery',
				broker=config.CRACKLING_BROKER,
				backend=config.CRACKLING_BACKEND,
				include=['crackling.tasks'],
				)

celery.conf.update(
		#CELERY_REDIRECT_STDOUTS_LEVEL = 'WARNING'
		CELERYD_CONCURRENCY = 1,
		#CELERYD_PREFETCH_MULTIPLIER = 2,	#setting CELERYD_PREFETCH_MULTIPLIER causes intermitent crashes
		)


if __name__ == '__main__':
	# run celery
	celery.start()

