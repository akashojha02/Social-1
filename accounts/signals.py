from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from accounts.models import Profile



def create_user_profile(sender, instance, created, **kwargs):    
    
    if created:
        print('create_user_profile called')
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


post_save.connect(create_user_profile, sender=User)