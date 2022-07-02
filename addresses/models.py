from django.db import models
from django_countries.fields import CountryField


class Address(models.Model):
    user = models.ForeignKey('auth.User', related_name='addresses', on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=False)

    country = CountryField(blank_label='(select country)')
    state = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=False)
    postal_code = models.CharField(max_length=16, blank=False)
    address_1 = models.CharField(max_length=1024, blank=False)
    address_2 = models.CharField(max_length=1024, blank=True)

    phone_number = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']
        get_latest_by = 'updated'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'country', 'state', 'city', 'address_1', 'address_2'],
                name='unique_user_address',
            ),
        ]
