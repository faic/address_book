from rest_framework import serializers
from django_countries.serializers import CountryFieldMixin

from addresses.models import Address


class AddressSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    country = CountryFieldMixin()

    class Meta:
        model = Address
        fields = [
            'id',
            'name',
            'country',
            'state',
            'city',
            'postal_code',
            'address_1',
            'address_2',
            'phone_number',
            'email',
        ]
