from django.db import models
from django.contrib.auth.models import User
from records.models import Genre

from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomerAccount(models.Model):
    """
    This model handles the storage of the default personal
    information submitted by the customer when they want to
    save it upon checkout.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_full_name = models.CharField(max_length=50, null=True, blank=True)
    account_email = models.EmailField(max_length=254, null=True, blank=True)
    account_postcode = models.CharField(max_length=20, null=True, blank=True)
    account_town_or_city = models.CharField(
        max_length=40, null=True, blank=True
    )
    account_street_address1 = models.CharField(
        max_length=80, null=True, blank=True
    )
    account_street_address2 = models.CharField(
        max_length=80, null=True, blank=True
    )
    account_county = models.CharField(max_length=80, null=True, blank=True)
    favoured_genre = models.ForeignKey(Genre, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def create_or_amend_account(sender, instance, created, **kwargs):
    """
    Method to check whether the created parameter is true.
    If true, create an instace of the above model.
    Otherwise, just save the instance to the model as it
    will be an amendment to the CustomerAccount instance.
    """
    if created:
        CustomerAccount.objects.create(user=instance)
    # instance.User.save()
