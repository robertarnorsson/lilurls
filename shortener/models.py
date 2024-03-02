from django.db import models
from datetime import datetime

class UrlCounter(models.Model):
    count = models.IntegerField(default=0)

    def increment(self):
        self.count += 1
        self.save()
    
    def get_counter(self):
        return self.count

    def __str__(self):
        return str(self.count)

class UrlModel(models.Model):
    original_url = models.URLField(max_length=200)
    short_url_extension = models.CharField(max_length=15, unique=True)
    visit_count = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()

    def is_expired(self):
        return datetime.now().timestamp() >= self.expiration_date.timestamp()

    def increment(self):
        self.visit_count += 1
        self.save()
    
    def get_counter(self):
        return self.visit_count
    
    def get_original(self):
        return self.original_url
    
    def get_days_left(self):
        now_naive = datetime.now().replace(tzinfo=None)
        time_difference = self.expiration_date.replace(tzinfo=None) - now_naive
        return time_difference.days

    def __str__(self):
        return self.short_url_extension

class Report(models.Model):
    VIOLATION_CHOICES = [
        ('spam', 'Spam'),
        ('malware', 'Malware'),
        ('phishing', 'Phishing'),
        ('inappropriate_content', 'Inappropriate Content'),
        ('illegal_activities', 'Illegal Activities'),
        ('rights_infringement', 'Rights Infringement'),
        ('double_redirection', 'Double Redirection'),
        ('other', 'Other'),
    ]

    url = models.URLField()
    violation_type = models.CharField(max_length=50, choices=VIOLATION_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f"Report for {self.url}"