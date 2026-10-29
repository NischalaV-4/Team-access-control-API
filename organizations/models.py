from django.db import models
from django.conf import settings
from uuid import uuid4

# Create your models here.
class Organization(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class OrganizationMembership(models.Model):
    ROLE_ADMIN = 'A'
    ROLE_OWNER='O'
    ROLE_MEMBER = 'M'
    ROLE_VIEWER = 'V'
    MEMBERSHIP_CHOICES = [
        (ROLE_ADMIN,'admin'),
        (ROLE_OWNER,'owner'),
        (ROLE_MEMBER,'member'),
        (ROLE_VIEWER,'viewer')
    ]
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='organization_memberships')
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
        models.UniqueConstraint(
            #this ensures that the combination of user and organization is unique
            fields=['user', 'organization'],
            name='unique_user_organization_membership'
        )
        ]
    def __str__(self):
        return f"{self.user} - {self.organization} ({self.get_role_display()})"
