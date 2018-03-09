from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver




class EmailConfirmedManager(models.Manager):
    def get_queryset(self):
        return super(EmailConfirmedManager, self).get_queryset().filter(email_confirmed=True)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', verbose_name=_('user'), on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False, verbose_name=_('email_confirmed'))

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        default_manager_name = 'objects'

    # adding managers
    objects = models.Manager()
    confirmed = EmailConfirmedManager()

    def __str__(self):
        return _("%(name)s's profile") % {'name': self.user.username}



@receiver(post_save, sender=User)
def create_profile(sender, created, instance, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
