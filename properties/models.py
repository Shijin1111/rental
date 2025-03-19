from django.db import models
from django.conf import settings

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    area = models.IntegerField()
    floor = models.IntegerField()
    location = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    rent = models.IntegerField()
    bedrooms = models.IntegerField()
    kitchen = models.IntegerField()
    hall = models.CharField(max_length=3)  # 'Yes' or 'No'
    balcony = models.CharField(max_length=3)  # 'Yes' or 'No'
    description = models.CharField(max_length=200)
    AC = models.CharField(max_length=3)  # 'Yes' or 'No'
    image = models.ImageField(upload_to='property_images/', blank=True, null=True)
    date_added = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.property_id} - {self.location}, {self.city}"


from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE)
    property = models.ForeignKey("Property", on_delete=models.CASCADE)  # Message linked to a property
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
