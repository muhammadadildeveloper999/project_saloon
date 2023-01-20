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

# #Role table``
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
    image = models.ImageField(upload_to='superadmin/')
    # Added_by = models.ForeignKey(Role, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.service_name

#Saloon
class saloon(BaseModel):
    saloon_name = models.CharField(max_length=255,default='')
    contact = models.CharField(max_length=255,default='')
    address = models.CharField(max_length=255,default='')   
    image = models.ImageField(upload_to='superadmin/',default="")
    city_id = models.ForeignKey(city,blank=True,null=True,on_delete=models.CASCADE)
    service_id = models.ForeignKey(service,blank=True,null=True,on_delete=models.CASCADE)
    # role_id = models.ForeignKey(Role, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.saloon_name
    
class saloon_image(BaseModel):
        image = models.ImageField(upload_to='superadmin/',default="")
        saloon_id = models.ForeignKey(saloon ,blank=True,null=True,on_delete=models.CASCADE)
# category table


class category(BaseModel):
    category_name = models.CharField(max_length=255, default='')
    saloon_id= models.ForeignKey(saloon, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.category_name

class services_list(BaseModel):
    name = models.CharField(max_length=255, default='')
    before_time = models.TimeField(null=True, blank=True)
    service_type = models.CharField(max_length=255,default='')
    price = models.FloatField(default=0)
    saloon_id= models.ForeignKey(saloon, blank = True, null = True, on_delete = models.CASCADE)
    category_id= models.ForeignKey(category, blank = True, null = True, on_delete = models.CASCADE)
    # role_id = models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)
    def __str__(self):
        return self.name

#Employee table 
class float_list(BaseModel):
    section_name = models.CharField(max_length=255,default='')    
    saloon_id= models.ForeignKey(saloon, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.section_name


# # Employee table
class review(BaseModel):
    comment = models.CharField(max_length=255,default='')  
    star = models.IntegerField(default='0')    
    date_created = models.DateField(null=True, blank=True)
    Account_id= models.ForeignKey(Account, blank = True, null = True, on_delete = models.CASCADE)
    services_list_id = models.ForeignKey(services_list, blank = True, null = True, on_delete = models.CASCADE)
    float_id = models.ForeignKey(float_list, blank = True, null = True, on_delete = models.CASCADE)
    saloon_id = models.ForeignKey(saloon, blank = True, null = True, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.comment

#Employee table
class portfolio(BaseModel):
    image = models.ImageField(upload_to='superadmin/',default="")
    saloon_id= models.ForeignKey(saloon, blank = True, null = True, on_delete = models.CASCADE)

    def __img__(self):
        return self.image


#Employee table
class detail(BaseModel):
    name = models.CharField(max_length=255,default='')    
                                                                                                                                                
    def __str__(self):
        return self.name

class about_us(BaseModel):
    heading = models.CharField(max_length=955,default='')                                       
    discription = models.CharField(max_length=955,default='')                                       
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.discription

#Employee table
class employee(BaseModel):
    name = models.CharField(max_length=955,default='')
    image = models.ImageField(upload_to='superadmin/',default="")
    emp_about_description = models.CharField(max_length=255,default='')
    heading = models.CharField(max_length=955,default='')
    services_list_id = models.ForeignKey(services_list,blank=True,null=True,on_delete=models.CASCADE)
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)
    # service_id = models.ForeignKey(service,blank=True,null=True,on_delete=models.CASCADE)
   # Added_by = models.ForeignKey(Role, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.emp_about_description

class employee_name(BaseModel):
    employee_name = models.CharField(max_length=955,default='')
    employee_image = models.ImageField(upload_to='superadmin/',default="")
    saloon_id = models.ForeignKey(saloon, blank = True, null = True, on_delete = models.CASCADE)
    # Added_by = models.ForeignKey(Role, blank = True, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.employee_name  

class employee_timing(BaseModel):
    date = models.DateField(null=True, blank=True)
    starttime = models.TimeField(null=True, blank=True)
    endtime = models.TimeField(null=True, blank=True)
    saloon_id = models.ForeignKey(saloon, blank = True, null = True, on_delete = models.CASCADE)
    employee_name_id = models.ForeignKey(employee_name, blank = True, null = True, on_delete = models.CASCADE)

    def __int__(self):
        return self.timing

class contact_buss_hour(BaseModel):
    heading = models.CharField(max_length=955,default='')                                       
    discription = models.CharField(max_length=955,default='')                                       
    phone_no = models.CharField(max_length=255,default='')    
    monday = models.TimeField(null=True, blank=True)
    tuesday = models.TimeField(null=True, blank=True)
    wednesday = models.TimeField(null=True, blank=True)
    thursday = models.TimeField(null=True, blank=True)
    friday = models.TimeField(null=True, blank=True)
    saturday = models.TimeField(null=True, blank=True)
    sunday = models.TimeField(null=True, blank=True)
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.phone_no

class social_media_share(BaseModel):
    heading = models.CharField(max_length=955,default='')                                       
    icon_name = models.CharField(max_length=255,default='')    
    icon_img = models.ImageField(upload_to='superadmin/')
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.icon_name

class venue_amenitie(BaseModel):
    heading = models.CharField(max_length=955,default='')                                       
    venue = models.CharField(max_length=255,default='')    
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.venue

class travel_fee_policy(BaseModel):
    heading = models.CharField(max_length=955,default='')                                       
    discription = models.CharField(max_length=955,default='')    
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.discription

class pay_cancellation_policy(BaseModel):
    heading = models.CharField(max_length=955,default='')                                       
    discription = models.CharField(max_length=955,default='')    
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.discription

class report(BaseModel):
    heading = models.CharField(max_length=955,default='')                                       
    name = models.CharField(max_length=255,default='')    
    discription = models.CharField(max_length=255,default='')    
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.discription


class health_safety_rule(BaseModel):
    name = models.CharField(max_length= 555,default='')    
    saloon_id = models.ForeignKey(saloon,blank=True,null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

#SubCategory
class subcategory(BaseModel):
    subcategory_name = models.CharField(max_length=255, default='')
    category_id = models.ForeignKey(category, blank = True, null = True, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='superadmin/')

    def __str__(self):
        return self.subcategory_name

#Employee table
class section(BaseModel):
    section_name = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.section_name


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
