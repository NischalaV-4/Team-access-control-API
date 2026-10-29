from django.shortcuts import render
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Organization, OrganizationMembership
from .serializers import OrganizationSerializer,MembershipSerializer

# Create your views here.
class OrganizationListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        organizations = Organization.objects.filter(
            memberships__user=request.user
        ).distinct()
        serializer = OrganizationSerializer(organizations,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganizationSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            #here the creation of organization and membership creation both operations take place in same transaction
            organization = serializer.save()

            OrganizationMembership.objects.create(
                user=request.user,
                organization=organization,
                role=OrganizationMembership.ROLE_OWNER
            )

        return Response(OrganizationSerializer(organization).data,status=status.HTTP_201_CREATED)


class OrganizationDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        organization = get_object_or_404(
            Organization.objects.filter(
                memberships__user=request.user
            ),
            pk=pk
        )

        serializer = OrganizationSerializer(organization)

        return Response(serializer.data,status=status.HTTP_200_OK)

class OrganizationMembers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,org_id):
        organization = get_object_or_404(Organization,id=org_id)
        memberships = OrganizationMembership.objects.filter(
            organization = organization
        ).select_related('user')
        serializer = MembershipSerializer(memberships,many=True)
        return Response(serializer.data)


class OrganizationMemberdetailView(APIView):
    permissions_classes = [IsAuthenticated]
    def patch(self,request,org_id,user_id):
        organization = get_object_or_404(
            Organization,
            id=org_id
        )
        membership = get_object_or_404(
            OrganizationMembership,organization=organization,user_id=user_id
            )
        requested_role = request.data.get("role")

        if not isinstance(requested_role, str) or not requested_role.strip():
            return Response(
                {"message": "Role is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        new_role = requested_role.strip().upper()
        allowed_roles = dict(OrganizationMembership.MEMBERSHIP_CHOICES).keys()
        if new_role not in allowed_roles:
            return Response({"message":"The requested role does not exist in defined organization roles"},status = status.HTTP_400_BAD_REQUEST)
        
        membership.role = new_role
        membership.save(updated_fields=["role"])
        return Response({"message":"Role updated successfully!"},status=status.HTTP_200_OK)

    def delete(self,request,org_id,user_id):
        organization = get_object_or_404(Organization,id=org_id)
        membership = get_object_or_404(OrganizationMembership,organization = organization,user_id = user_id)
        membership.delete()
        return Response(
            status=status.HTTP_200_OK
        )



