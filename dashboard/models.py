from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Role(models.Model):
    role_name = models.CharField(max_length=100)
    def __str__(self):
        return self.role_name

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    def __str__(self):
        return self.department_name
            
class Profile(models.Model):
    # Establish a One-to-One relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="The user this profile is associated with")
    
    # ForeignKey relationships for other models
    role = models.ForeignKey('Role', on_delete=models.CASCADE, help_text="Role of the employee in the organization")
    department = models.ForeignKey('Department', on_delete=models.CASCADE, help_text="Department where the employee works")
    
    # Other profile-specific fields
    phone = models.CharField(max_length=15, help_text="Contact number of the employee")
    manager = models.CharField(max_length=100, help_text="Name of the manager")
    location = models.CharField(max_length=100, help_text="Location of the employee")
    
    # Date fields
    joined_date = models.DateField(auto_now_add=True, help_text="Date when the employee joined")
    birthday = models.DateField(help_text="Birthday of the employee")
    
    # Profile image
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, help_text="Profile image of the employee")
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['user__username']
    
    # Method to get email from the User model
    @property
    def email(self):
        return self.user.email


class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    break_start_time = models.TimeField(null=True, blank=True)
    break_end_time = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    
    
    
    

# Leave Types
class LeaveType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Leave Requests
class LeaveRequest(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    apply_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type.name} - {self.status}"

    def total_days(self):
        return (self.end_date - self.start_date).days + 1

# Leave Summary
class LeaveSummary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_leaves_this_month = models.PositiveIntegerField(default=0)
    leaves_left = models.PositiveIntegerField(default=0)
    leave_requests = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - Leave Summary"






class Project(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    # Project Details
    title = models.CharField(max_length=255, help_text="Title of the project")
    client_name = models.CharField(max_length=255, help_text="Name of the client")
    start_date = models.DateField(help_text="Start date of the project")
    end_date = models.DateField(null=True, blank=True, help_text="End date of the project")
    deadline = models.DateField(help_text="Deadline for the project")

    # Many-to-Many relationship for project members
    members = models.ManyToManyField(User, related_name='projects', help_text="Members working on the project")

    # Priority and Progress
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium', help_text="Priority level of the project")
    progress = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Progress of the project in percentage")

    # Status of the project
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started', help_text="Current status of the project")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    @property
    def is_overdue(self):
        """Check if the project is overdue."""
        return self.deadline and self.status != 'Completed' and self.deadline < timezone.now().date()







class Team(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='teams')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.project.title})"

class TeamMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    date_joined = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'team')

    def __str__(self):
        return f"{self.user.username} - {self.role} in {self.team.name}"






class Task(models.Model):
    # Task Number
    task_no = models.AutoField(primary_key=True, verbose_name="Task No")

    # Project the task is associated with
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='tasks', verbose_name="Project")


    # Status of the task
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started', verbose_name="Status")

    # Type of the task
    TYPE_CHOICES = [
        ('Feature', 'Feature'),
        ('Bug', 'Bug'),
        ('Improvement', 'Improvement'),
        ('Documentation', 'Documentation'),
    ]
    task_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Feature', verbose_name="Type")

    # Priority of the task
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium', verbose_name="Priority")

    # Executor (User assigned to the task)
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks', verbose_name="Executor")

    # Joining Date (Date task was assigned)
    joining_date = models.DateField(default=timezone.now, verbose_name="Joining Date")

    # Details of the task
    details = models.TextField(verbose_name="Details")


    def __str__(self):
        return f"Task {self.task_no} - {self.project.title}"

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-priority', 'status', 'joining_date']
