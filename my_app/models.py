from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name
    
class User(AbstractUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(default='avatar.png', null=True, upload_to='user_images')
    description = models.TextField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'#User - {self.username}'

class Post(models.Model):
    description = models.TextField(default='', blank=True)
    image = models.ImageField(default='tree_plantation_1.jpg', upload_to='post_images')
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    created_at = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')

    def __str__(self):
        return '#Post - ' + self.description[:20] 

class Aboutus(models.Model):
    organization_name = models.CharField(max_length=200)
    email = models.EmailField()
    description = models.TextField(max_length=400)
    image = models.ImageField(default='save_plant_logo.png', upload_to='organization_images')

    class Meta:
        verbose_name_plural = 'About us'

    def __str__(self):
        return f'#Organization - {self.organization_name}'
    

class Contactus(models.Model):
    
    email = models.EmailField()
    phone = models.CharField(max_length=14, null=True)
    bkash_number = models.CharField(max_length=14, null=True)
    facebook = models.CharField(max_length=200, null=True)
    whatsapp = models.CharField(max_length=14, null=True)
    twitter = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'Contact us'

    def __str__(self):
        return f'#Contact - {self.email}'
    
class UserNotification(models.Model):
    sender = models.ForeignKey(User, related_name='notification_sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='notification_receiver', on_delete=models.CASCADE)
    notification = models.TextField()
    project = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.sender} - {self.receiver}'

class Donation(models.Model):
    receiver = models.ForeignKey(User, related_name='receiver', null=True, on_delete=models.SET_NULL)
    donator = models.ForeignKey(User, related_name='donator', null=True, on_delete=models.SET_NULL)
    donator_bkash_number = models.CharField(max_length=14, null=True)
    money_transaction_id = models.CharField(max_length=200, null=True)
    donation_amount = models.BigIntegerField()
    project = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.donator} - {self.receiver}'