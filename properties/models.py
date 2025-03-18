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
