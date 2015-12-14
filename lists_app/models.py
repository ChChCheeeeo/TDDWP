from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    def get_absolute_url(self):
        # use it in the view—the redirect function just takes the object we
        # want to redirect to, and it uses get_absolute_url under the hood
        # automagically
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    # to get it deliberately wrong, include the unique constraint
    text = models.TextField(default='')#, unique=True)
    list = models.ForeignKey(List, default=None)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')
