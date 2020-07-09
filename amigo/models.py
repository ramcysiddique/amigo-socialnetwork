from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UseraccountManager(BaseUserManager):
    def createuser(self, email, password=None, first_name=None, last_name=None, gender=None, age=None,country=None,
                   is_active=True, is_admin=False, is_staff=False):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.is_active=is_active
        user.is_admin=is_admin
        user.is_staff=is_staff
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.age = age
        user.country = country
        user.save(using=self._db)
        return user





    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.createuser(email,
                             password=password
                             )
        user.is_admin = True
        user.is_staff= True
        user.first_name = 'admin'
        user.last_name = ' '
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
                             password=password
                             )
        user.is_staff = True
        user.save(using=self._db)
        return user


class Useraccount(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(verbose_name='firstname', max_length=30,null=True)
    last_name = models.CharField(verbose_name='lastname', max_length=30,null=True)
    gender = models.CharField(verbose_name='gender', max_length=20,null=True)
    age = models.CharField(verbose_name='age',null=True,max_length=10)
    country = models.CharField(verbose_name='country', max_length=30,null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    #USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []

    objects = UseraccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        pass

    def get_short_name(self):
        pass



    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    email_id   = models.EmailField(max_length=60)
    time = models.CharField(max_length=20)
    post_text = models.CharField(max_length=100)
    post_img = models.CharField(max_length=50)

class Likes(models.Model):
    post_id = models.CharField(max_length=5)
    like_username = models.CharField(max_length=20)
    like_email = models.EmailField(max_length=60)


