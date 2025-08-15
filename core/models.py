from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

def year_week(dt=None):
    """Return ISO year and week number for a datetime (UTC)."""
    dt = dt or timezone.now()
    iso = dt.isocalendar()  
    return iso.year, iso.week

class Organization(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self):
        return self.name

class User(AbstractUser):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="users",
        null=True, blank=True
    )
    display_name = models.CharField(max_length=120, blank=True, default="")

    def __str__(self):
        return self.display_name or self.username

class Kudo(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kudos_given")
    to_user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kudos_received")
    message   = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    year = models.IntegerField()
    week = models.IntegerField()

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.year or not self.week:
            y, w = year_week(self.created_at)
            self.year, self.week = y, w
        super().save(*args, **kwargs)
