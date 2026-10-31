from django.urls import path

from .views import TeamDetailView

urlpatterns = [
    path("<uuid:team_id>/",TeamDetailView.as_view(),name="team-detail"),
]