from django.urls import path

from .views import OrganizationListCreateView,OrganizationDetailView,OrganizationMembers,OrganizationMemberdetailView


urlpatterns = [
    path('',OrganizationListCreateView.as_view(),name='organization-list-create'),
    path('<uuid:pk>/',OrganizationDetailView.as_view(),name='organization-detail'),
    path('<uuid:org_id>/members/',OrganizationMembers.as_view(),name='organization-members'),
    path('<uuid:org_id>/members/<int:user_id>',OrganizationMemberdetailView.as_view(),name='organization-member-detail'),
]