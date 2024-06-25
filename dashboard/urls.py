from django.urls import path
from .views import (
    DashboardView,
    ProfileView,
    AttendanceView,
    LeavesView,
    ProjectsView,
    TeamView,
    TeamDetailView,
    TaskView,
    # NotificationsView,
    # HelpAndSupportView,
    # ReportView,
    # CalendarView,
    # login_view
)
from django.contrib.auth import views as auth_views

app_name = "dashboard"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('attendance/', AttendanceView.as_view(), name='attendance'),
    path('leaves/', LeavesView.as_view(), name='leaves'),
    path('projects/', ProjectsView.as_view(), name='projects'),
    path('team/', TeamView.as_view(), name='team'),
    path('team/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('todos/', TaskView.as_view(), name='todos'),
    # path('notifications/', NotificationsView.as_view(), name='notifications'),
    # path('help-and-support/', HelpAndSupportView.as_view(), name='help-and-support'),
    # path('report/', ReportView.as_view(), name='report'),
    # path('calendar/', CalendarView.as_view(), name='calendar'),
]