from django.contrib import auth
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
User= auth.get_user_model()


def get_first_name(self):
    return "@{}".format(self.username)

User.add_to_class("__str__", get_first_name)
# class User(auth.models.User,auth.models.PermissionsMixin):
#     def __str__(self):
#         return "@{}".format(self.username)


class Profile(models.Model):
    """ Extending User model to store extra field"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_img = models.ImageField(upload_to= 'accounts/profile_img',
                                        default='accounts/profile_img/no_image.jpg')
    bio = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=50, blank=True)
    dob = models.DateField(null=True, blank=True)

    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    
class Friend_Request(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user',
                 on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user',
                 on_delete=models.CASCADE)