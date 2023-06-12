from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
from shortuuidfield import ShortUUIDField

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
    last_name  = models.CharField(max_length=100)
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


# class OnlineUser(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)

# 	def __str__(self):
# 		return self.user.username


class ChatRoom(models.Model):
	roomId = ShortUUIDField()
	type = models.CharField(max_length=10, default='DM')
	member_1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='member_1')
	member_2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='member_2')
	timestamp = models.DateTimeField(auto_now_add=True)
	# name = models.CharField(max_length=20, null=True, blank=True)

	def __str__(self):
		return self.roomId + ' -> ' + str(self.name)

class ChatMessage(models.Model):
	sender = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL, null=True)
	reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	message = models.CharField(max_length=255)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.message
