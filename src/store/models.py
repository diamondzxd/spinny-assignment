from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class Box(models.Model):
    length = models.IntegerField()
    width = models.IntegerField()
    height = models.IntegerField()
    created_on = models.DateTimeField(
        auto_now_add=True, auto_now=False, blank=True)
    updated_on = models.DateTimeField(auto_now=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='created_by')
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='updated_by')

    def __str__(self):
        return f"{self.length} X {self.width} X {self.height}"

    @property
    def area(self):
        return self.length * self.width

    @property
    def volume(self):
        return self.length * self.width * self.height
