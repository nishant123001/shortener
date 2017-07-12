import time
import random

from django.db import IntegrityError

from shortener import models
from shortener import settings
from shortener import util
from shortener import exceptions

class Shortner:
	def __init__(self):
		pass

	# Try to get a random code. Idea is to use a random number and time
	# Colision can only happen in the request coming in same milisecond. Also
	# multiply it with a random number so as to make it truely random.
	# Idea is to have a random enough number which can cause less colisions.
	def _get_sudorandom(self, req_time_milisecond, try_count):
		# For each try increase the range of random number by 10 folds
		max_random = settings.RANDOM_MAX
		for _ in range(try_count):
			max_random = max_random*10
		unique_number = int(str(random.randint(0, max_random)) + str(req_time_milisecond*random.randint(1, 9)))
		print util.encode(unique_number)
		return util.encode(unique_number)

	def get_code(self, url):
		curr_time_milisec = int(time.time()*1000)
		retry_count = 0
		short_obj = None
		while retry_count < settings.RETRY_COUNT:
			try:
				short_obj = models.UrlShortner.objects.create(url=url, code=self._get_sudorandom(curr_time_milisec, retry_count))
			except IntegrityError as e:
				print e
				retry_count += 1
				continue
			break
		if short_obj is None:
			raise exceptions.ServerError("Unable to create shortned urls")
		return short_obj.code

	def get_url(self, code):
		url_objs = models.UrlShortner.objects.filter(code=code)
		if len(url_objs):
			return url_objs[0].url
		return None

		