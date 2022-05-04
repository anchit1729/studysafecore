#Define venue, hku_member, visit_record relationship

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.

"""
Author: Anchit Mishra

This class acts as a user manager for the custom users we define below.
"""
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



"""
Author: Anchit Mishra

This class provides a baseline template for user authentication.
Currently, it doesn't extend anything beyond the default available
from Django, but it is always useful to include a custom model 
for future use.
"""
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(_('email address'), unique = True)
    is_human = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    if is_human:
        REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'email']
    else:
        REQUIRED_FIELDS = ['username'] 

    objects = CustomUserManager()

    def __str__(self):
        return self.username

"""
Author: Anchit Mishra

This class forms the model of a member of HKU - these may be either
staff or students (StudySafeCore does not treat either as different).
It defines the attributes and their corresponding constraints to 
enable database setup by Django.
"""
class HKUMember(models.Model):
    # The uid must be a unique attribute (primary key)
    uid = models.CharField(max_length = 10, unique = True, primary_key = True)
    name = models.CharField(max_length = 150, default = '')

    def __str__(self):
        return self.uid

"""
Author: Anchit Mishra

This class forms the model of a venue in HKU. It defines the attributes
required for a Venue entity as well as their corresponding constraints
to enable database setup by Django.
"""
class Venue(models.Model):
    # We define the set of values acceptable for the venue type field
    VENUE_TYPES = [('LT', 'Lecture Theatre'), ('CR', 'Classroom'), ('TR', 'Tutorial Room')]
    # The venue_code must be a unique attribute (primary key)
    venue_code = models.CharField(max_length = 20, unique = True, primary_key = True)
    location = models.CharField(max_length = 150)
    type = models.CharField(max_length = 2, choices = VENUE_TYPES)
    capacity = models.DecimalField(decimal_places = 0, max_digits = 5)
    # Since Members and Venues have a many-to-many relationship, we define VisitRecord
    # as an Association Class
    members = models.ManyToManyField(HKUMember, through = 'VisitRecord')

    def __str__(self):
        return self.venue_code

"""
Authors: Anchit Mishra and Jianan Lin

This class acts as an association class between Venues and HKUMembers. It enables the storage
of entry and exit records of HKUMembers into/from Venues for the purpose of contact tracing.
To make semantic sense, the 'through' field to mark this class as an association class has been
defined in the Venue class - a Venue may have several members within it. This class also specifies
the various attributes and their corresponding referential constraints to enable database setup
by Django.
"""
#Define association class: Refer to https://stackoverflow.com/questions/60762397/uml-association-class-and-oop-languages
class VisitRecord(models.Model):

    class Meta:
        unique_together = ('member_uid', 'venue_code', 'access_type', 'record_datetime')
    # We define the set of values acceptable for the access type field
    VISIT_TYPES = [('IN', 'Entry'), ('EX', 'Exit')]
    # member_uid and venue_code fields are foreign keys taken from the HKUMember and Venue models 
    member_uid = models.ForeignKey(HKUMember, on_delete=models.CASCADE, default = 1)
    venue_code = models.ForeignKey(Venue, on_delete=models.CASCADE, default = 1)
    access_type = models.CharField(max_length = 2, choices = VISIT_TYPES)
    record_datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.member_uid} --- {self.venue_code} --- {self.access_type} --- {self.record_datetime}'

"""

All the code below is NOT REQUIRED for now, since the initial MVP does not have to include authentication.
We will see to it at a later point in time, when the core API and web application are ready and deployed.

"""

# class device(models.Model):
#     VISIT_RECORD = models.ManyToManyField(visit_record)
#     pass

# class task_force_member(user):
#     VENUE = models.ManyToManyField(venue)
#     VISIT_RECORD = models.ManyToManyField(visit_record)
#     HKU_MEMBER = models.ManyToManyField(hku_member)
#     DEVICE = models.ManyToManyField(device, through='user', related_name='+', blank=True)
#     #first_name, last_name, email are present in AbstractUser class already. They are not defined here again.

# #Define association class: Refer to https://stackoverflow.com/questions/60762397/uml-association-class-and-oop-languages
# class user(AbstractUser):
#     class Meta:
#         unique_together = [("TASK_FORCE_MEMBER", "DEVICE")]
#     DEVICE = models.ForeignKey(device, on_delete=models.CASCADE, default = 1)
#     TASK_FORCE_MEMBER = models.ForeignKey(task_force_member, on_delete=models.CASCADE, default = 1)
#     username = models.CharField(max_length = 150, primary_key=True)
#     password = models.CharField(max_length = 150)
#     #device = models.ForeignKey(device, on_delete = models.CASCADE)
#     #task_force_member = models.ForeignKey(task_force_member, on_delete = models.CASCADE)
#     #id = models.AutoField(primary_key=True)
#     def __str__(self):
#         return self.username


