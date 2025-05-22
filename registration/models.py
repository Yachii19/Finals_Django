from django.db import models



class Registration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    confirm_password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    date_registered = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=12, default="")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
