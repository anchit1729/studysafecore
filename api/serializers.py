from os import access
from rest_framework import serializers

from .models import VisitRecord
from .models import Venue
from .models import HKUMember

# Here, we define all the custom serializers required for the API

"""
Author: Anchit Mishra
This class defines the custom serializer to be used for the VisitRecord model.
"""
class VisitRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitRecord
        fields = '__all__'

"""
Author: Peng Yinglun
This class defines the custom serializer to be used for the venue model.
"""
class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        exclude = ['members',]


"""
Author: Shao Rui
This class defines the custom serializer only extracting the venue code.
"""
class VenueCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ['venue_code']


"""
Author: Shao Rui
This class defines the custom serializer only extracting the HKUMember uid
"""
class HKUMemberUIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = HKUMember
        fields = ['uid']


"""
Author: Shao Rui
This class defines the custom serializer to be used for the HKUMember model.
"""
class HKUMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = HKUMember
        fields = '__all__'