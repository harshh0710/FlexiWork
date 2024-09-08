from django.db import models
from django.utils import timezone
from accounts.models import User

JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Posted by")
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    category = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    company_name = models.CharField(max_length=100)
    company_description = models.CharField(max_length=300)
    website = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']  # Latest jobs appear first

    def __str__(self):
        return self.title

    # Custom method to calculate days until the job expires
    def days_until_expiration(self):
        return (self.last_date - timezone.now()).days
    # Custom method for dashboard display - count of applicants
    def applicant_count(self):
        return self.applicants.count()

    # Method to check if the job is active or expired
    def is_active(self):
        return timezone.now() < self.last_date and not self.filled


    # Status label for dashboard
    def status_label(self):
        if self.filled:
            return "Filled"
        elif self.is_active():
            return "Active"
        return "Expired"


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']  # Latest applicants appear first

    def __str__(self):
        return self.user.get_full_name()

    # Custom method to return how long ago the application was submitted
    def time_since_applied(self):
        return (timezone.now() - self.created_at).days

    # Custom method for dashboard display - user's email
    def applicant_email(self):
        return self.user.email
