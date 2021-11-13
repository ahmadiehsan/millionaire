import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Create Time"))
    modify_time = models.DateTimeField(auto_now=True, verbose_name=_("Modify Time"))

    auto_cols = ['create_time', 'modify_time']

    class Meta:
        ordering = ('-create_time',)
        get_latest_by = ('create_time',)
        abstract = True
