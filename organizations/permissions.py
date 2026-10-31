from .models import OrganizationMembership,Organization,Team
from rest_framework.permissions import BasePermission


ROLE_PERMISSIONS = {
    OrganizationMembership.ROLE_OWNER: {
        "users.read",
        "users.invite",
        "users.update",
        "projects.read",
        "projects.write",
        "billing.read",
        "teams.read",
        "teams.write",
    },

    OrganizationMembership.ROLE_ADMIN: {
        "users.read",
        "users.invite",
        "users.update",
        "projects.read",
        "projects.write",
        "teams.read",
        "teams.write",
    },

    OrganizationMembership.ROLE_MEMBER: {
        "projects.read",
        "projects.write",
        "teams.read",
    },

    OrganizationMembership.ROLE_VIEWER: {
        "projects.read",
        "teams.read",
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
    permission within the requested organization and team.

    """
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Different HTTP methods can require different permissions.
        required_permission = getattr(
            view,
            "required_permission",
            None,
        )

        if isinstance(required_permission, dict):
            required_permission = required_permission.get(
                request.method
            )

        # Deny if the HTTP method has no configured permission.
        if not required_permission:
            return False

        organization_id = view.kwargs.get("org_id")

        # Organization-scoped endpoints provide org_id directly.
        if organization_id is None:
            team_id = view.kwargs.get("team_id")

            if team_id is None:
                return False

            try:
                team = Team.objects.only(
                    "organization_id"
                ).get(pk=team_id)

                organization_id = team.organization_id

            except Team.DoesNotExist:
                return False

        membership = OrganizationMembership.objects.filter(
            user=user,
            organization_id=organization_id,
        ).first()

        if membership is None:
            return False

        allowed_permissions = ROLE_PERMISSIONS.get(
            membership.role,
            set(),
        )

        return required_permission in allowed_permissions

