from django.shortcuts import render
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Organization, OrganizationMembership
from .serializers import OrganizationSerializer

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

