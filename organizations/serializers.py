from rest_framework import serializers

from .models import Organization,OrganizationMembership,Team


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

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model= Team
        fields = ['id','name','description','created_at']
        read_only_fields = ['id','created_at']

        def validate_name(self,value):
            value=value.strip()
            if not value:
                raise serializers.ValidationError("Team name cannot be empty.")

            organization =  self.context.get("organization")
            if organization is None:
                raise serializers.ValidationError("Organization context is required")

            existing_teams = Team.objects.filter(
                organization = organization,
                name__iexact = value,
            )

            # During PATCH, exclude the current team.
            if self.instance:
                existing_teams = existing_teams.exclude(
                    pk=self.instance.pk
                )

            if existing_teams.exists():
                raise serializers.ValidationError("A team with this name already exists in this organization.")
            
            return value