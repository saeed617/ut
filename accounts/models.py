from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from django.core.validators import MaxValueValidator, MinValueValidator

from django.db.models.signals import pre_save
from django.dispatch import receiver




class Major(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', verbose_name=_('user'), on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False, verbose_name=_('email_confirmed'))
    student_id = models.IntegerField(validators=[MinValueValidator(10**8), MaxValueValidator(999999999)])
    major = models.ForeignKey(Major)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')


    def __str__(self):
        return _("%(name)s's profile") % {'name': self.user.username}


''''@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
'''