from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from autoslug import AutoSlugField

class Issue(models.Model):
    Autor = models.ForeignKey(User)
    Assign = models.ForeignKey(
        User,
        related_name=_("assign"),
        null=True,
    )
    Title = models.CharField(
        max_length=100,
        default=_('titre')
    )
    slug = AutoSlugField(populate_from='Title')
    UserRequest = models.TextField()
    Answer = models.TextField()
    CreateDate = models.DateTimeField(auto_now_add=True)
    LastActivity = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(
        max_length=20,
        default="open",
        choices=(
            ("open", _("open")),
            ("progress", _("in_progress")),
            ("close", _("status")),
        )
    )

    def __str__(self):
        return self.Title