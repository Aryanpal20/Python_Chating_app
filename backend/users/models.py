from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
import uuid

# Create your models here.


class User(AbstractUser):

    Male = 1
    Female = 2

    GENDER = (
        (Male, 'Male'),
        (Female, 'Female'),
    )

    email = models.EmailField(('email_address'), unique=True, max_length=200)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER, blank=True, null=True, default=1
    )
    mobile_no = PhoneNumberField(unique=True, null=True, blank=True)

    # Required fields for Django's AbstractUser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    # Custom User manager
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)


class ChatRoom(models.Model):
    roomId = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    type = models.CharField(max_length=10, default='DM')
    member_1 = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='member_1'
    )
    member_2 = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='member_2'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.roomId)


class ChatMessage(models.Model):
    room_ID = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='sender'
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='receiver'
    )
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender.first_name}, " \
               f"To: {self.receiver.first_name}, " \
               f"Message: {self.message}"
