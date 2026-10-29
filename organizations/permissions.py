from .models import OrganizationMembership,Organization
from rest_framework.permissions import BasePermission


ROLE_PERMISSIONS = {
    OrganizationMembership.ROLE_OWNER: {
        "users.read",
        "users.invite",
        "users.update",
        "projects.read",
        "projects.write",
        "billing.read",
    },

    OrganizationMembership.ROLE_ADMIN: {
        "users.read",
        "users.invite",
        "users.update",
        "projects.read",
        "projects.write",
    },

    OrganizationMembership.ROLE_MEMBER: {
        "projects.read",
        "projects.write",
    },

    OrganizationMembership.ROLE_VIEWER: {
        "projects.read",
    },
}


def has_permission(membership, permission):
    """
    Check whether a membership's role grants a permission.
    """
    if membership is None:
        return False
    allowed_permissions = ROLE_PERMISSIONS.get(membership.role,set())
    return permission in allowed_permissions

class HasOrganizationPermission(BasePermission):
    """
    Check whether the requesting user has a required
    permission within the requested organization.
    """

    def has_permission(self, request, view):

        # this determines which permission does this endpoint require 
        required_permission = getattr(view,"required_permission",None)#reads attribute from the APIVIew
        if not required_permission:
            return False

        #finds organization id 
        organization_id = (view.kwargs.get("org_id")
            or view.kwargs.get("organization_id")
            or view.kwargs.get("pk"))
        if not organization_id:
            return False

        organization = Organization.objects.filter(
            pk=organization_id
        ).first()
        if organization is None:
            return False

        #find this user's membership in the organizatio
        membership = OrganizationMembership.objects.filter(user=request.user,organization=organization).first()
        if membership is None:
            return False

        #save the membership for possible use by the view
        request.organization_membership = membership

        # Check the required permission.
        return has_permission(membership,required_permission)