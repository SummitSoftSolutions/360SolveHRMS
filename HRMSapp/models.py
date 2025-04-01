from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
   
    
    class Meta:
        db_table = "Role"
    
    def __str__(self):
        return self.name
    
class UserManager(BaseUserManager):
    def create_user(self, email, password=None,role=None,  **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        if not role:
            role = Role.objects.get_or_create(name="User")[0]
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        admin_role, _ = Role.objects.get_or_create(name="SuperAdmin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        return self.create_user(email, password,role=admin_role, **extra_fields)

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    role=models.ForeignKey(Role,on_delete=models.CASCADE,null=True)
    groupAcess = models.BooleanField(default=False)
    createdOn=models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False) 
    is_deleted=models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.email


class MasterModule(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    Name = models.CharField(max_length=150,default=True)
    Logo=models.FileField(upload_to='media/logs/',default=True)
    Description=models.CharField(max_length=150,null=True)
    IsDeleted=models.IntegerField(default=0)
    Status=models.IntegerField(choices=STATUS_CHOICES,default=1)
    
    class Meta:
        db_table = "MasterModule"
    
    def __str__(self):
        return self.Name
    
    
class SubModule(models.Model):
    STATUS_CHOICES = [
        (1, 'Active'),
        (0, 'Inactive'),
    ]
    Name = models.CharField(max_length=150,default=True)
    Module=models.ForeignKey(MasterModule,on_delete=models.CASCADE)
    IsDeleted=models.IntegerField(default=0)
    Status=models.IntegerField(choices=STATUS_CHOICES,default=1)
     
    class Meta:
         db_table = "SubModule"
    
    def __str__(self):
        return self.Name
    
     
class SubmoduleLimit(models.Model):
    submod=models.ForeignKey(SubModule,on_delete=models.CASCADE)
    limit_value = models.IntegerField(default=0)
    isactive =    models.IntegerField(default=1)
    isdeleted =    models.IntegerField(default=0)
    
    class Meta:
         db_table = "SubmoduleLimit"
