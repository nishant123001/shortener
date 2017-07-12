from django.db import models
from django.utils.timezone import now


class UrlShortner(models.Model):
	url = models.TextField(null=False)
	code = models.CharField(null=False, db_index=True, unique=True, max_length=20)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
