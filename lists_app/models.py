from django.db import models
from django.core.urlresolvers import reverse

class List(models.Model):
    def get_absolute_url(self):
        # use it in the view—the redirect function just takes the object we
        # want to redirect to, and it uses get_absolute_url under the hood
        # automagically
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)