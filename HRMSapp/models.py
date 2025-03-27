from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class SuperAdminManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class SuperAdmin(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150, default=True)  # Set default
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="superadmin_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="superadmin_permissions",
        blank=True,
    )

    objects = SuperAdminManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
    
    class Meta:
        db_table = "SuperAdmin"

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = "Role"
    
    def __str__(self):
        return self.name
    



class MasterModule(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    Name = models.CharField(max_length=150,default=True)
    Logo=models.FileField(upload_to='media/logs/',default=True)
    Description=models.CharField(max_length=150,null=True)
    IsDeleted=models.IntegerField()
    Status=models.IntegerField(choices=STATUS_CHOICES,default=1)
    
    class Meta:
        db_table = "MasterModule"
    
    def __str__(self):
        return self.Name
    
    
class SubModule(models.Model):
    Name = models.CharField(max_length=150,default=True)
    Module=models.ForeignKey(MasterModule,on_delete=models.CASCADE)
     
    class Meta:
         db_table = "SubModule"
    
    def __str__(self):
        return self.Name
    
     
    