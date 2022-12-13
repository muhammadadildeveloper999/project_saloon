

from django.db import models
import uuid


two = (

    ('monthly','monthly'),
    ('yearly','yearly')
)

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    class Meta:
        abstract = True

# #Role table
class Role(BaseModel):
        role=models.CharField(max_length=20, default='user')
        def __str__(self):
            return self.role

# register table uuit, created date & updated
class Account(BaseModel):
    firstname = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=255, default='')
    password = models.CharField(max_length=255, default='')
    contact = models.CharField(max_length=255, default='')
    role_id = models.ForeignKey(Role, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.email

# category table
class category(BaseModel):
    categoryname = models.CharField(max_length=255, default='')
    role_id = models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='superadmin/',default='superadmin/dumm.jpg')

    def __str__(self):
        return self.categoryname

#SubCategory
class subcategory(BaseModel):
    subcategory_name = models.CharField(max_length=255, default='')
    category_id = models.ForeignKey(category, blank = True, null = True, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='superadmin/',default='superadmin/dumm.jpg')

    def __str__(self):
        return self.subcategory_name

#Packages
class package(BaseModel):
    registration_date = models.DateTimeField(blank=True,null=True)
    end_date = models.DateTimeField(blank=True,null=True)
    description = models.CharField(max_length=255, default='')
    charges = models.IntegerField(default='')
    packagesStatus=models.BooleanField(max_length=255, default='False')
    packages=models.CharField(choices=two, max_length=20, default='monthly')
    register_id = models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.registration_date

#Country table
class country(BaseModel):
    name = models.CharField(max_length=255,default='')
    Account_id = models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

#City table
class city(BaseModel):
    name = models.CharField(max_length=255,default='')
    country_id = models.ForeignKey(country,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class service(BaseModel):
    service_name = models.CharField(max_length=255,default='')
    description = models.CharField(max_length=255,default='') 
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to='superadmin/',default='superadmin/dumm.jpg')
    Service_Timing = models.DateTimeField(null=True, blank=True)
    before_time = models.TimeField(null=True, blank=True)
    # Added_by = models.ForeignKey(Role, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.service_name

#Saloon
class saloon(BaseModel):
    saloon_name = models.CharField(max_length=255,default='')
    contact = models.CharField(max_length=255,default='')
    address = models.CharField(max_length=255,default='')
    city_id = models.ForeignKey(city,blank=True,null=True,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='superadmin/',default='superadmin/dumm.jpg')
    service_id = models.ForeignKey(service,blank=True,null=True,on_delete=models.CASCADE)
    # role_id = models.ForeignKey(Role, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.saloon_name

#Employee table
class employee(BaseModel):
    name = models.CharField(max_length=255,default='')
    contact = models.CharField(max_length=255,default='')
    image = models.ImageField(upload_to='superadmin/',default='superadmin/dumm.jpg')
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)
    service_id = models.ForeignKey(service,blank=True,null=True,on_delete=models.CASCADE)
    Added_by = models.ForeignKey(Role, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

class appointment(BaseModel):
    description = models.CharField(max_length=255,default='')
    start_date = models.DateTimeField(blank=True,null=True)
    contact = models.CharField(max_length=255,default='')
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)
    facilty_id = models.ForeignKey(service, blank = True, null = True, on_delete = models.CASCADE)
    register_id = models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.description

    # Login Data for records
class whitelistToken(models.Model):
    token = models.CharField(max_length=255, default='')
    user_agent = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add='True', blank = True, null = True)
    role_id = models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.token
