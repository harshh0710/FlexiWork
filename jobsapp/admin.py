from django.contrib import admin
from .models import Job, Applicant


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'location', 'type', 'created_at', 'status_label', 'applicant_count', 'days_until_expiration')
    list_filter = ('type', 'location', 'created_at', 'filled')
    search_fields = ('title', 'company_name', 'location')
    readonly_fields = ('created_at', 'applicant_count')
    
    def status_label(self, obj):
        return obj.status_label()

    status_label.short_description = 'Status'
    status_label.admin_order_field = 'filled'  # Sort by filled status
    
    def applicant_count(self, obj):
        return obj.applicant_count()

    applicant_count.short_description = 'Number of Applicants'
    
    def days_until_expiration(self, obj):
        days_left = obj.days_until_expiration()
        if days_left > 0:
            return f"{days_left} days"
        return "Expired"
    
    days_until_expiration.short_description = 'Days Left'


class ApplicantAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'created_at', 'time_since_applied')
    list_filter = ('created_at', 'job__title')
    search_fields = ('user__email', 'job__title')
    readonly_fields = ('created_at',)

    def time_since_applied(self, obj):
        return f"{obj.time_since_applied()} days ago"

    time_since_applied.short_description = 'Applied'


# Register the models with their custom admins
admin.site.register(Job, JobAdmin)
admin.site.register(Applicant, ApplicantAdmin)
