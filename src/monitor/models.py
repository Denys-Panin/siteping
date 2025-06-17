from django.db import models
from django.contrib.auth.models import User


class MonitoredSite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sites')
    name = models.CharField(max_length=100)
    url = models.URLField()
    check_interval = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.url})"


class SiteCheckLog(models.Model):
    site = models.ForeignKey(MonitoredSite, on_delete=models.CASCADE, related_name='logs')
    checked_at = models.DateTimeField(auto_now_add=True)
    status_code = models.IntegerField()
    response_time = models.FloatField(help_text="Response time in seconds")
    is_online = models.BooleanField()

    def __str__(self):
        return f"{self.site.name} @ {self.checked_at} -> {self.status_code}"
