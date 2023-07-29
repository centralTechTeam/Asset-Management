from django.db import models
from django_countries.fields import CountryField
from accounts.models import User


# Create your models here.


class Assign(models.Model):
    Name = models.CharField(max_length=100,)

    def __str__(self):
        return self.Name
    

#class DepreciationRate(models.Model):
    #Depre_Rate = models.PositiveBigIntegerField(null=True, default='2%')

   # def __repr__(self):
    #    return self.Depre_Rate

#class DepreciationType(models.Model):
 #   Depre_Type = models.CharField(max_length=100, null=True, default='Straight-Line Method')

  #  def __str__(self):
   #     return self.Depre_Type



class Vendor(models.Model):
    VENDOR_CHOICES = (
    ('Manufacturer','Manufacturer'),
    ('wholesaler','Wholesaler'),
    ('retailers','Retailer'),
    ('service and maintenance providers','Service and maintenance providers'),
    ('independent vendors','Independent vendors')
    )
    Company_Name = models.CharField(max_length=50, blank=False,)
    Name = models.CharField(max_length=100)
    Business = models.CharField(max_length=40, choices=VENDOR_CHOICES, default='Manufacturer')
    Address = models.CharField(max_length=250)
    City = models.CharField(max_length=30, null=True, blank=True)
    Phone = models.CharField(max_length=15)
    Email = models.EmailField(max_length=50, null=True, blank=True)
    Website = models.URLField(max_length=250, blank=True, null=True)
    Country = CountryField(blank_label='(select country)')

    def __str__(self):
        return self.Company_Name


class Employee(models.Model):
    Status = [
    ('Single', 'Single'),
    ('Marriage', 'Marriage'),
    ('Disvorce', 'Disvorce'),
    ('Engaged', 'Engaged'),
    ('Window', 'Window'),
]
    Full_Name = models.CharField(max_length=50)
    user = models.OneToOneField("accounts.User", related_name='emp_user', null=True, blank=True, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100, null=True, blank=True,)
    Departments = models.ForeignKey(Assign, null=True, on_delete=models.SET_NULL) 
    Phone = models.CharField(max_length=15)
    Address = models.CharField(max_length=50, null=True, blank=True)
    profile_pic = models.ImageField(default="picture1.png", null=True, blank=True)
    Date_of_Birth = models.DateField(null=True, blank=True)
    Marital_Status = models.CharField(max_length=20, choices=Status, null=True, blank=True )
    #Category = models.ForeignKey(Assign, on_delete=models.CASCADE)

    def __str__(self):
        return self.Full_Name

#class InCharge(models.Model):
 #   Name = models.ForeignKey(Employee, on_delete=models.CASCADE)
  #  Category = models.ForeignKey(Assign, on_delete=models.CASCADE)

   # def __str__(self):
    #    return str(self.Name.Full_Name)



class Assets(models.Model):
    A_CHOICES = (
    ('New','New'),
    ('Good','Good'),
    ('Used','Used'),
    ('Defective','Defective')
    )
    Name = models.CharField(max_length= 50)
    Type = models.ForeignKey("Asset_Type", on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    Model = models.CharField(max_length=200, null=True,)
    Serian_Num = models.CharField(max_length= 100, null=True, blank=True)
    Asset_State = models.CharField(max_length=15, choices=A_CHOICES, default='New')
    Departments = models.ForeignKey(Assign,on_delete=models.CASCADE)
    LifeSpan = models.CharField(max_length=50, null=True, blank=True, default='10Yrs')
    Date_Acquired = models.DateField()
    Warantee_Start_Date = models.DateField(null=True, blank=True)
    Warantee_End_Date = models.DateField(null=True, blank=True)
    Employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    Date_Assigned = models.DateField( null=True)
    Location = models.CharField(max_length=100, null=True, blank=True,)
    Vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    Description = models.TextField()

    def __str__(self):
        return self.Name

class Asset_Type(models.Model):
    type = models.CharField(max_length= 50,)

    def __str__(self):
        return self.type

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ManyToManyField(User, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f'{self.subject} ({self.sender} -> {self.receiver})'
    
class BroadcastMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject