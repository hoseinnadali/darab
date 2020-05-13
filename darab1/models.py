from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,RegexValidator
import jdatetime
from django_jalali.db import models as jmodels
from django.utils.translation import gettext_lazy as _

# Create your models here.




class Pharmacy(models.Model):
    licenceNumber = models.PositiveIntegerField(validators = [MinValueValidator(200000000000),MaxValueValidator(999999999999)], null = False, blank = False, unique = True, verbose_name = 'شماره پروانه')
    fullname = models.CharField(db_index = True, max_length = 100, null = False , blank = False, verbose_name = 'نام داروخانه')
    address = models.OnetoOneField('Address', on_delete = models.CASCADE,null = False, blank = False, unique = True, verbose_name = 'آدرس داروخانه')
    contactDetails = models.OneToOneField('ContactDetails', on_delete = models.CASCADE, null = False, blank = False, unique = True, verbose_name = 'شماره تماس های داروخانه')
    person = models.OneToOneField('Person', on_delete = models.CASCADE, nill = False, blank = False, unique = True, verbose_name = 'مدیریت داروخانه')

class Address(model.Model):
    province = models.OneToOneField('Province', on_delete = models.PROTECT, null = False, blank = False, verbose_name = 'استان')
    city = models.OneToOneField('City', on_delete = models.PROTECT, null = False, blank = False, verbose_name = 'شهر')
    exactAddress = models.CharField(db_index = True, max_length = 500, null = False, blank = False, verbose_name = 'آدرس دقیق')

class Province(models.Model):
    name = models.CharField(db_index = True, max_length = 50, null = False, blank = False, unique = True, verbose_name = 'نام استان')

class City(models.Model):
    name = models.CharField(db_index = True, max_length = 100, null = False, blank = False, unique = False, verbose_name = 'نام شهر')

class ContactDetails(models.Model):
    phoneNumber1 = models.PositiveIntegerField(validators = [MinValueValidator(20000000), MaxValueValidator(99999999)], null = Flase, blank = False, unique = True, verbose_name = 'شماره تماس1')
    phoneNumber2 = models.PositiveIntegerField(validators = [MinValueValidator(20000000), MaxValueValidator(99999999)], null = True, blank = True, unique = True, verbose_name = 'شماره تماس2')
    mobileNumber = models.PositiveIntegerField(validators = [MinValueValidator(9000000000), MaxValueValidator(9999999999)], null = True, blank = True, unique = True, verbose_name = 'شماره همراه')

class Person(models.Model):
    nationalCode = models.CharField(db_index = True, max_length = 10, validators = [RegexValidator(regex = r'^\d{10}$', message = 'Length has to be 10', code = 'nomatch')], null = False, blank = False,unique = True, verbose_name = 'کد ملی')
    firstName = models.CharField(db_index = True, max_length = 50, null = False, blank = False, verbose_name = 'نام')
    lastName = models.CharField(db_index = True, max_length = 70, null = False, blank = Flase, verbose_name = 'نام خانوادگی')

class Drug(models.Model):
    name = models.CharField(db_index = True, max_length = 100, null = False, blank = False, verbose_name = 'نام دارو')
    latinName = models.CharField(db_index = True, max_length = 150, null = False = blank = False, verbose_name = 'نام لاتین')
    type = models.CharField(db_index = True, max_length = 50, null = False, blank = False, verbose_name = 'نوع')
    use = models.CharField(db_index = True, max_length = 100, null = False, blank = False, verbose_name = 'موارد استفاده')
    consumptionInstruction = models.TextField(max_length = 1000, null = True, blank = True, verbose_name = 'دستور العمل مصرف')
    sideEffects = models.TextField(max_length = 1000, null = True, blank = True, verbose_name = 'اثرات جانبی')
    warnings = models.TextField(max_length = 1000, null = True, blank = True, verbose_name = 'هشدارها')
    manufacturer = models.CharField(max_length = 100, null = False, blank = False, verbose_name = 'تولیدکننده')

class DrugRegistration(models.Model):
    objects = jmodels.jManager()
    drug = models.OneToOneField('Drug',on_delete = models.CASCADE, null = False, blank = False, unique = True, verbose_name = 'دارو')
    addDate = jmodels.jDateField(default = jdatetime.date.today, null = False, blank = True, verbose_name = 'تاریخ ثبت')
    pharmacy = models.OneToOneField('Pharmacy', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'داروخانه ثبت کننده')

class DrugPricing(models.Model):
    objects = jmodels.jManager()
    drug = models.ForeignKey('Drug', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'دارو')
    price = models.FloatField(null = False, blank = False, verbose_name = 'قیمت')
    insuranceRate = models.OneToOneField('InsuranceRate', on_delete = models.CASCADE, null = Flase, blank = False, verbose_name = 'نرخ بیمه')
    addDate = jmodels.jDateField(default = jdatetime.datetime.now, null = False, blank = True, verbose_name = 'تاریخ ثبت قیمت')

class Request(models.Model):
    objects = jmodels.jManager()
    applicantFirstName = models.CharField(db_index = True, max_length = 50, null = False, blank = False, verbose_name = 'نام متقاضی')
    applicantLastName = models.CharField(db_index = True, max_length = 100, null = False, blank = False, verbose_name = 'نام خانوادگی متقاضی')
    text = models.TextField(db_index = True, max_length = 2000, null = False, blank = False, verbose_name = 'متن درخواست')
    isAccepted = models.BooleanField(default = False, null = False, blank = True, verbose_name = 'تاییدیه')
    requestDate = jmodels.jDateField(default = jdatetime.date.today, null = False, blank = True, verbose_name = 'تاریخ درخواست')

class OpinionForPharmacy(models.Model):
    objects = jmodels.jManager()
    pharmacy = models.ForeignKey('Pharmacy', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'داروخانه')
    userType = models.ForiegnKey('UserType', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'نوع کاربر')

    title = models.CharField(db_index = True, max_length = 300, null = True, blank = True, verbose_name = 'عنوان')
    text = models.TextField(max_length = 1000, null = False, blank = False, verbose_name = 'متن')
    date = jmodels.jDateField(default = jdatetime.date.today, null = False = blank = True, verbose_name = 'تاریخ ثبت')

class OpinionForDrug(models.Model):
    objects = jmodels.jManager()
    drug = models.ForeignKey('Drug', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'دارو')
    userType = models.ForiegnKey('UserType', on_delete = models.CASCADE, null = False, blank = False, verbose_name = 'نوع کاربر')

    title = models.CharField(db_index = True, max_length = 300, null = True, blank = True, verbose_name = 'عنوان')
    text = models.TextField(max_length = 1000, null = False, blank = False, verbose_name = 'متن')
    date = jmodels.jDateField(default = jdatetime.date.today, null = False = blank = True, verbose_name = 'تاریخ ثبت')

class UserType(models.Model):
    typeChoices = models.TextChoices('typeChoices','Pharmacy Drug')
    type = models.CharField(db_index = True, max_length = 50, choices = typeChoices.choices, null = False, blank = False, verbose_name = 'نوع کاربر')
