from django.shortcuts import render,redirect,get_object_or_404
import datetime
# some_app/views.py
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
)
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import *

from datetime import datetime

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["my_projects"] = Project.objects.filter(members=user).count()
        user_projects = Project.objects.filter(members=user)
        context['my_teams'] = Team.objects.filter(project__in=user_projects).distinct()
        today = datetime.today().date()
        total_working_days = Attendance.objects.filter(
            user=user,
            date__lte=today,
        ).count()

        present_days = Attendance.objects.filter(
            user=user,
            date__lte=today,
            status='Present'
        ).count()

        if total_working_days > 0:
            attendance_percentage = (present_days / total_working_days) * 100
        else:
            attendance_percentage = 0
        context['my_tasks'] = Task.objects.filter(executor=user)
        context['attendance_percentage'] = attendance_percentage
        context['total_leaves_approved'] = LeaveRequest.objects.filter(status='Approved').count()
        context['total_tasks'] = Task.objects.filter(executor=user).count()
        
        return context
    
    
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/my_profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user        
        context["profile"] = get_object_or_404(Profile, user=current_user)
        return context
    
class AttendanceView(LoginRequiredMixin, ListView):
    template_name = "dashboard/my_attendence.html"
    model = Attendance
    context_object_name = 'attendance_list'
    ordering = ['date']
    
class LeavesView(LoginRequiredMixin, ListView):
    template_name = "dashboard/my_leaves.html"
    model = LeaveRequest
    context_object_name = 'leaves_list'
    ordering = ['apply_date']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['leaves_requests'] = LeaveRequest.objects.count()
        context['total_leaves_approved'] = LeaveRequest.objects.filter(status='Approved').count()
        context['total_leaves_rejected'] = LeaveRequest.objects.filter(status='Rejected').count()
        context['total_leaves_pending'] = LeaveRequest.objects.filter(status='Pending').count()
        return context
    
    
class ProjectsView(LoginRequiredMixin,ListView):
    model = Project
    template_name = 'dashboard/my_projects.html'  
    context_object_name = 'projects_list'
    ordering = ['start_date']

    def get_queryset(self):
        user = self.request.user
        
        return Project.objects.filter(members=user).distinct() 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_projects = self.get_queryset()
        
        context['total_projects'] = user_projects.count()
        context['completed_projects'] = user_projects.filter(status='Completed').count()
        context['in_progress_projects'] = user_projects.filter(status='In Progress').count()
        context['overdue_projects'] = user_projects.filter(
            deadline__lt=timezone.now().date(),
            status__in=['Not Started', 'In Progress']
        ).count()
        return context
    
class TeamView(LoginRequiredMixin, ListView):
    model = Team
    template_name = "dashboard/my_team.html"
    context_object_name = 'team_list'
    
    def get_queryset(self):
        user = self.request.user
        user_projects = Project.objects.filter(members=user)
        return Team.objects.filter(project__in=user_projects).distinct()

class TeamDetailView(LoginRequiredMixin, DetailView):
    model = Team
    template_name = 'dashboard/my_team_detail.html'
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.get_object()
        user = self.request.user
        context['project'] = team.project
        projects = Project.objects.filter(members=user).distinct()
    
        project_members = {project: project.members.all() for project in projects}
    
        context['project_members'] = project_members
        
        return context

class TaskView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "dashboard/my_todos.html"
    context_object_name = 'task_list'
    

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(executor=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['total_tasks'] = Task.objects.filter(executor=user).count()
        context['completed_tasks'] = Task.objects.filter(executor=user, status='Completed').count()
        context['in_progress_tasks'] = Task.objects.filter(executor=user, status='In Progress').count()
        
        context['projects'] = Project.objects.all()
        context['task_type_choices'] = Task.TYPE_CHOICES
        context['task_priority_choices'] = Task.PRIORITY_CHOICES
        context['task_status_choices'] = Task.STATUS_CHOICES
        context['users'] = User.objects.all()

        return context
    

# class NotificationsView(TemplateView):
#     template_name = "dashboard/my_notifications.html"
    
# class HelpAndSupportView(TemplateView):
#     template_name = "dashboard/help_and_support.html"

# class ReportView(TemplateView):
#     template_name = "dashboard/reports.html"
    
# class CalendarView(TemplateView):
#     template_name = "dashboard/calendar.html"
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         days = range(1, 32)
#         today = datetime.date.today()
#         context = {
#         'days': days,
#         'today': today,
#         } 
#         return context
    