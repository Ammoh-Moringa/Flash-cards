from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, default='No bio')
    profile= models.ImageField(upload_to = 'images/',default='SOME IMAGE')

    def __str__(self):
        return self.user.username
    
    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls,name):
        return cls.objects.filter(user__username__icontains=name).all()