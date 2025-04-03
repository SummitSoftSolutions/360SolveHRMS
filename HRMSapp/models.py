from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CountryTbl(models.Model):
    country_name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=100)
    country_currency = models.CharField(max_length=100)
    country_status = models.CharField(max_length=100)
    isdelete = models.IntegerField()

    class Meta:
        db_table = 'CountryTbl'
    
        def __str__(self):
            return self.country_name

class StateTbl(models.Model):
    state_name = models.CharField(max_length=255)
    country = models.ForeignKey(CountryTbl, models.DO_NOTHING)
    state_status = models.CharField(max_length=100)
    state_code = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    isdelete = models.IntegerField()
    gst_code = models.IntegerField(blank=True,null=True)

    class Meta:
        db_table = 'StateTbl'
    
    def __str__(self):
        return self.state_name


class DistrictTbl(models.Model):
    name = models.CharField(db_column='Name', max_length=225)  # Field name made lowercase.
    state = models.ForeignKey('StateTbl', models.DO_NOTHING, db_column='StateId')  # Field name made lowercase.
    district_status=models.CharField(max_length=100,null=True,default="")
    districtcode = models.CharField(db_column='DistrictCode', max_length=225, blank=True, null=True)
    short_name = models.CharField(max_length=100,default="")
    isdelete = models.IntegerField(default=0)

    class Meta:
        db_table = 'DistrictTbl'
        
    def __str__(self):
        return self.name
        
        
class CityTbl(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=255)
    district = models.ForeignKey('DistrictTbl', models.DO_NOTHING, null=True, blank=True)
    distance = models.IntegerField(null=True, blank=True)
    status = models.IntegerField()
    isdelete = models.IntegerField()

    class Meta:
        db_table = 'CityTbl'
    
    def __str__(self):
        return self.city_name
        

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

    Name = models.CharField(max_length=150,default=True)
    Logo=models.FileField(upload_to='media/logs/',default=True)
    Description=models.CharField(max_length=150,null=True)
    IsDeleted=models.IntegerField(default=0)
    Status=models.BooleanField(default=True)
    
    class Meta:
        db_table = "MasterModule"
    
    def __str__(self):
        return self.Name
    
    
class SubModule(models.Model):
    Name = models.CharField(max_length=150,default=True)
    Module=models.ForeignKey(MasterModule,on_delete=models.CASCADE)
    IsDeleted=models.IntegerField(default=0)
    Status=models.BooleanField(default=True)
     
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


class GroupAdmin(models.Model):
    groupname  = models.CharField(max_length=200)
    legalname = models.CharField(max_length=200)
    shortname = models.CharField(max_length=200)
    address = models.TextField()
    country= models.ForeignKey(CountryTbl,on_delete=models.CASCADE,null=True,blank=True)
    state= models.ForeignKey(StateTbl,on_delete=models.CASCADE,null=True,blank=True)
    district= models.ForeignKey(DistrictTbl,on_delete=models.CASCADE,null=True,blank=True)
    city= models.ForeignKey(CityTbl,on_delete=models.CASCADE,null=True,blank=True)
    contact_mob = models.CharField(max_length=20, blank=True, null=True)  # Mobile contact number (optional)
    contact_email = models.EmailField(max_length=255, blank=True, null=True)
    description =  models.TextField()
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "GroupAdmin"
         
         
class CompanyTbl(models.Model):
    company_name = models.CharField(max_length=200)
    company_code = models.CharField(max_length=200)
    country= models.ForeignKey(CountryTbl,on_delete=models.CASCADE,null=True,blank=True)
    state= models.ForeignKey(StateTbl,on_delete=models.CASCADE,null=True,blank=True)
    district= models.ForeignKey(DistrictTbl,on_delete=models.CASCADE,null=True,blank=True)
    city= models.ForeignKey(CityTbl,on_delete=models.CASCADE,null=True,blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    group =  models.ForeignKey(GroupAdmin,on_delete=models.CASCADE)
    localname = models.CharField(max_length=200)
    legalname = models.CharField(max_length=200)
    company_address = models.CharField(max_length=200)
    company_cin = models.CharField(max_length=200)
    company_tin = models.CharField(max_length=200)
    contact_mob = models.CharField(max_length=20, blank=True, null=True)  # Mobile contact number (optional)
    contact_email = models.EmailField(max_length=255, blank=True, null=True)
    company_registration = models.CharField(max_length=20, blank=True, null=True)  # Mobile contact number (optional)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "CompanyTbl"
         
         
class BranchTbl(models.Model):
    branch_name = models.CharField(max_length=200)
    local_name = models.CharField(max_length=200)
    branch_code = models.CharField(max_length=200)
    company =  models.ForeignKey(CompanyTbl,on_delete=models.CASCADE)
    legalname = models.CharField(max_length=200)
    country= models.ForeignKey(CountryTbl,on_delete=models.CASCADE,null=True,blank=True)
    state= models.ForeignKey(StateTbl,on_delete=models.CASCADE,null=True,blank=True)
    district= models.ForeignKey(DistrictTbl,on_delete=models.CASCADE,null=True,blank=True)
    city= models.ForeignKey(CityTbl,on_delete=models.CASCADE,null=True,blank=True)
    branch_address = models.CharField(max_length=200)
    contact_mob = models.CharField(max_length=20, blank=True, null=True)  # Mobile contact number (optional)
    email = models.EmailField(max_length=255, blank=True, null=True)
    company_registeration = models.CharField(max_length=20, blank=True, null=True)  # Mobile contact number (optional)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "BranchTbl"


class Subscription(models.Model):
    group = models.ForeignKey(GroupAdmin,on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyTbl,on_delete=models.CASCADE)
    branch = models.ForeignKey(BranchTbl,on_delete=models.CASCADE)
    Module = models.ForeignKey(MasterModule,on_delete=models.CASCADE,null=True)
    Sub_Module=models.ForeignKey(SubModule,on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True)
    is_deleted=models.BooleanField(default=False)
    expirydate=models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "Subscription"
 
class TaxCategory(models.Model):
    name = models.CharField(max_length=150,null=True)
    is_deleted=models.IntegerField(default=0) 
    
    class Meta:
        db_table="TaxCategory" 
          
class TaxType(models.Model):
    taxName = models.CharField(max_length=150,null=True)
    is_deleted =models.BooleanField(default=0)
    Category=models.ForeignKey(TaxCategory,on_delete=models.CASCADE,null=True)
    class Meta:
        db_table = "TaxType"
    
    def __str__(self):
        return self.taxName
    
        
    
