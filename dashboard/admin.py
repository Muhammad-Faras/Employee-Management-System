from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Attendance)


admin.site.register(LeaveType)
admin.site.register(LeaveSummary)
admin.site.register(LeaveRequest)


admin.site.register(Project)


admin.site.register(Team)
admin.site.register(TeamMembership)


admin.site.register(Task)



