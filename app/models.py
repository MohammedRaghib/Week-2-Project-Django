from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('image', null= True, blank=True)
    def __str__(self):
        return f"{self.user.username} Profile"

@receiver(post_save, sender=User) 
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User) 
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Photo(models.Model):
    description = models.TextField()
    photo = CloudinaryField('image', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='tags')
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    def __str__(self):
        return f"A photo of {self.description}"

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()