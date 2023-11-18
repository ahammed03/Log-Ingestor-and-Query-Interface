from django.db import models


class Log(models.Model):
    level = models.CharField(max_length=50)
    message = models.TextField()
    resourceId = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    traceId = models.CharField(max_length=100)
    spanId = models.CharField(max_length=100)
    commit = models.CharField(max_length=100)
    parentResourceId = models.CharField(max_length=100, null=True, blank=True)  # Nullable field

    # Add any other fields as required

    def __str__(self):
        return f'{self.level} - {self.message} - {self.timestamp}'




