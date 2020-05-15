from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
import jdatetime
from django_jalali.db import models as jmodels
from django.contrib.auth.models import AbstractBaseUser,User
from django.contrib.auth.managers import UserManager
from django.core.mixins import PermissionsMixin

# Create your models here.



class MyUser(AbstractBaseUser,PermissionsMixin):
    objects = jmodels.jManager()
    username = models.CharField(db_index = True, max_length = 100, null = False, blank = False, unique = True, verbose_name = 'نام کاربری')
    email = models.EmailField(max_length = 255, null = True, blank = True, unique = True, verbose_name = 'آدرس ایمیل')
    date_joined = jmodels.jDateField(default = jdatetime.date.todey, null = False, blank = True, verbose_name = 'تاریخ ثبت نام')
    last_login = models.jDateTimeField(default = jdatetime.datetime.now, null = False,blank = True, verbose_name = 'آخرین ورود')
    is_active = models.BooleanField(default = True, null = False, blank = True, verbose_name = 'فعال')
    is_superuser = models.BooleanField(default = False, null = False, blank = True, verbose_name = 'ادمین')
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    def __str__(self):
        return self.username

class ActiveUser(models.Model):
    user = models.OneToOneField('MyUser',on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'کاربر فعال')
    firstName = models.CharField(db_index = True, max_length = 100, null = False, blank = False, verbose_name = 'نام')
    lastName = models.CharField(db_index = True, max_length = 200, null = False, blank = False, verbose_name = 'نام خانوادگی')
def __str__(self):
    return self.user.username

class PharmacyUser(models.Model):
    user = models.OneToOneField('MyUser',on_delete = models.CASCADE, null = False, blank = False, unique = True, verbose_name = 'کاربر داروخانه')
    pharmacy = models.OneToOneField('Pharmacy', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'داوخانه')
    def __str__(self):
        return self.user.username

class Pharmacy(models.Model):
    licenceNumber = models.PositiveIntegerField(validators = [MinValueValidator(200000000000),MaxValueValidator(999999999999)], null = False, blank = False, unique = True, verbose_name = 'شماره پروانه')
    fullname = models.CharField(db_index = True, max_length = 100, null = False , blank = False, verbose_name = 'نام داروخانه')
    address = models.OnetoOneField('Address', on_delete = models.CASCADE,null = False, blank = False, unique = True, verbose_name = 'آدرس داروخانه')
    contactDetails = models.OneToOneField('ContactDetails', on_delete = models.CASCADE, null = False, blank = False, unique = True, verbose_name = 'شماره تماس های داروخانه')
    person = models.OneToOneField('Person', on_delete = models.CASCADE, nill = False, blank = False, unique = True, verbose_name = 'مدیریت داروخانه')
    def __str__(self):
        return self.fullname

class Address(model.Model):
    province = models.OneToOneField(on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'استان')
    city = models.CharField(on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'شهر')
    exactAddress = models.CharField(db_index = True, max_length = 500, null = False, blank = False, verbose_name = 'آدرس دقیق')
    def __str(self):
        return '%s-%s-%s'%(self.province.name,self.city.name,self.exactAddress)

class Province(models.Model):
    name = models.CharField(db_index = True, max_length = 100, null = False, blank = False, unique = True, verbose_name = 'استان')
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(db_index = True, max_length = 100, null = Flase, blank = False, verbose_name = 'شهر')
    def __str__(self):
        return self.name

class ContactDetails(models.Model):
    phoneNumber1 = models.PositiveIntegerField(validators = [MinValueValidator(20000000), MaxValueValidator(99999999)], null = Flase, blank = False, unique = True, verbose_name = 'شماره تماس1')
    phoneNumber2 = models.PositiveIntegerField(validators = [MinValueValidator(20000000), MaxValueValidator(99999999)], null = True, blank = True, unique = True, verbose_name = 'شماره تماس2')
    mobileNumber = models.PositiveIntegerField(validators = [MinValueValidator(9000000000), MaxValueValidator(9999999999)], null = True, blank = True, unique = True, verbose_name = 'شماره همراه')
    def __str__(self):
        return self.id

class Person(models.Model):
    nationalCode = models.CharField(db_index = True, max_length = 10, validators = [RegexValidator(regex = r'^\d{10}$', message = 'Length has to be 10', code = 'nomatch')], null = False, blank = False,unique = True, verbose_name = 'کد ملی')
    firstName = models.CharField(db_index = True, max_length = 50, null = False, blank = False, verbose_name = 'نام')
    lastName = models.CharField(db_index = True, max_length = 70, null = False, blank = Flase, verbose_name = 'نام خانوادگی')
    def __str__(self):
        return '%s %s'%(self.firstName,self.lastName)

class Drug(models.Model):
    name = models.CharField(db_index = True, max_length = 100, null = False, blank = False, verbose_name = 'نام دارو')
    latinName = models.CharField(db_index = True, max_length = 150, null = False = blank = False, verbose_name = 'نام لاتین')
    type = models.CharField(db_index = True, max_length = 50, null = False, blank = False, verbose_name = 'نوع')
    use = models.CharField(db_index = True, max_length = 100, null = False, blank = False, verbose_name = 'موارد استفاده')
    consumptionInstruction = models.TextField(max_length = 1000, null = True, blank = True, verbose_name = 'دستور العمل مصرف')
    sideEffects = models.TextField(max_length = 1000, null = True, blank = True, verbose_name = 'اثرات جانبی')
    warnings = models.TextField(max_length = 1000, null = True, blank = True, verbose_name = 'هشدارها')
    manufacturer = models.CharField(max_length = 100, null = False, blank = False, verbose_name = 'تولیدکننده')
    def __str__(self):
        return self.name

class DrugRegistration(models.Model):
    objects = jmodels.jManager()
    drug = models.OneToOneField('Drug',on_delete = models.CASCADE, null = False, blank = False, unique = True, verbose_name = 'دارو')
    addDate = jmodels.jDateField(default = jdatetime.date.today, null = False, blank = True, verbose_name = 'تاریخ ثبت')
    pharmacy = models.ForeignKey('Pharmacy', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'داروخانه ثبت کننده')
    def __str__(self):
        return '%s : %s'%(self.drug.name,self.parmacy.fullName)

class DrugPricing(models.Model):
    objects = jmodels.jManager()
    drug = models.ForeignKey('Drug', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'دارو')
    price = models.FloatField(null = False, blank = False, verbose_name = 'قیمت')
    insuranceRate = models.ForeignKey('InsuranceRate', on_delete = models.CASCADE, null = Flase, blank = False, verbose_name = 'نرخ بیمه')
    addDate = jmodels.jDateTimeField(default = jdatetime.datetime.now, null = False, blank = True, verbose_name = 'تاریخ ثبت قیمت')
    def __str__(self):
        return '%s : %s'%(self.drug.name,self.addDate)

class InsuranceRate(models.Model):
    type = models.CharField(db_index = True, max_length = 100, null = False, blank = False, unique = True, verbose_name = 'نوع نرخ بیمه')
    def __str__(self):
        return self.type

class Request(models.Model):
    objects = jmodels.jManager()
    applicantFirstName = models.CharField(db_index = True, max_length = 50, null = False, blank = False, verbose_name = 'نام متقاضی')
    applicantLastName = models.CharField(db_index = True, max_length = 100, null = False, blank = False, verbose_name = 'نام خانوادگی متقاضی')
    text = models.TextField(db_index = True, max_length = 2000, null = False, blank = False, verbose_name = 'متن درخواست')
    isAccepted = models.BooleanField(default = False, null = False, blank = True, verbose_name = 'تاییدیه')
    requestDate = jmodels.jDateField(default = jdatetime.date.today, null = False, blank = True, verbose_name = 'تاریخ درخواست')
    def __str__(self):
        return '%s %s : %s'%(self.applicantFirstName,self.applicantLastName,self.requestDate)

class OpinionForPharmacy(models.Model):
    objects = jmodels.jManager()
    pharmacy = models.ForeignKey('Pharmacy', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'داروخانه')
    author = models.ForiegnKey('MyUser', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'نویسنده')
    title = models.CharField(db_index = True, max_length = 300, null = True, blank = True, verbose_name = 'عنوان')
    text = models.TextField(max_length = 1000, null = False, blank = False, verbose_name = 'متن')
    date = jmodels.jDateField(default = jdatetime.date.today, null = False = blank = True, verbose_name = 'تاریخ ثبت')

class OpinionForDrug(models.Model):
    objects = jmodels.jManager()
    drug = models.ForeignKey('Drug', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'دارو')
    author = models.ForiegnKey('MyUser', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'نویسنده')
    title = models.CharField(db_index = True, max_length = 300, null = True, blank = True, verbose_name = 'عنوان')
    text = models.TextField(max_length = 1000, null = False, blank = False, verbose_name = 'متن')
    date = jmodels.jDateField(default = jdatetime.date.today, null = False = blank = True, verbose_name = 'تاریخ ثبت')
