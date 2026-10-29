from rest_framework import serializers

from .models import Organization,OrganizationMembership


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization

        fields = ['id','name','created_at',]
        read_only_fields = ['id','created_at',]

class MembershipSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id',read_only = True)
    username = serializers.CharField(source = 'user.username',read_only=True)
    class Meta:
        model = OrganizationMembership
        fields = ['id','user_id','username','role']

