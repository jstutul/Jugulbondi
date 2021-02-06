import csv
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import request
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from accounts.tokens import account_activation_token

class UserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,password=None):
        if not email:
            raise ValueError("user must have an email")
        email=email.lower()
        first_name=first_name.title()
        last_name=last_name.title()
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.is_active=False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name, last_name, password=None):
        user=self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_superuser=True
        user.is_staff=True
        user.is_active=True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True,verbose_name='Email')
    first_name = models.CharField(max_length=20,verbose_name='First Name')
    last_name = models.CharField(max_length=20,verbose_name='Last Name')
    # city = models.CharField(max_length=20,verbose_name='City Name')

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name','last_name',)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_varified = models.BooleanField(default=False)
    verification = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return self.first_name+" "+self.last_name
    def clean(self):
        if self.is_active==False and self.is_varified==True and self.verification==False:
            self.verification=True
            mail_subject = 'Account Verification'
            current_site = 'http://127.0.0.1:8000'
            message = render_to_string('user/acc_active_email.html', {
                'user': self.first_name,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(self.id)),
                'token': account_activation_token.make_token(self),
            })
            to_email = self.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

        elif self.is_varified==False:
            self.verification=False
            self.is_active=False
            self.save()
            print("admin verification kore nai")

    def get_short_name(self):
        return self.email
    def has_perm(self,prem,obj=None):
        return self.is_superuser
    def has_module_perms(self,app_label):
        return self.is_superuser
    def title_name(self):
        return self.first_name
    class Meta:
        verbose_name_plural='users'

Marital_Status = (
    ('Single','Single'),
    ('Married', 'Married'),
    ('Divorced','Divorced'),
)
Body_type = (
    ('Slim','Slim'),
    ('Faty', 'Faty'),
    ('Medium','Medium'),
)
Eating_Habit = (
    ('Vegetarian','Vegetarian'),
    ('Non Vegetarian', 'Non Vegetarian'),
    ('Both','Both'),
)
Drinking_Habit = (
    ('Never','Never'),
    ('Occasionally', 'Occasionally'),
    ('Regularly','Regularly'),
)
Smoking_Habit= (
    ('Never','Never'),
    ('Sometimes', 'Sometimes'),
    ('Regularly','Regularly'),
)
Complexion = (
    ('Fair','Fair'),
    ('Light Fair','Light Fair'),
    ('Black', 'Black'),
    ('Light Brown','Light Brown'),
    ('Brown','Brown'),
)
Physical_Status = (
    ('Normal','Normal'),
    ('Abnormal','Abnormal'),
)
Religion_Status=(
    ('Hindu','Hindu'),
    ('Muslim','Muslim'),
    ('Buddhists','Buddhists '),
    ('Christians','Christians '),

)
Gender_Status=(
    ('Male','Male'),
    ('Female','Female'),
    ('Others','Others'),
)
Education_Status=(
    ('JSC','JSC'),
    ('SSC','SSC'),
    ('HSC','HSC'),
    ('BBA','BBA '),
    ('MBA','MBA '),
    ('BA','BA '),
    ('BSC','BSC '),
    ('MBBS','MBBS '),
    ('CIVIL','CIVIL '),
    ('DAKIL','DAKIL '),
    ('KAMIL','KAMIL '),
    ('LLB','LLB '),


)
Family_Status=(
    ('Reputed','Reputed'),
    ('Low','Low'),
    ('Medium','Medium'),
)


class Profile(models.Model):
    email = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    about = models.TextField(blank=False, max_length=500)
    photo = models.ImageField(upload_to="profile",blank=True,default="default.png")
    age = models.PositiveIntegerField(default=18)
    height = models.PositiveIntegerField(default=0)
    weight = models.FloatField(default=0.0)
    gender = models.CharField(choices=Gender_Status,blank=True,max_length=12)
    mother_tongue = models.CharField(blank=True, max_length=30)
    marital_status = models.CharField(choices=Marital_Status, max_length=20, blank=True)
    body_type = models.CharField(choices=Body_type, blank=True, max_length=12)
    complexion = models.CharField(choices=Complexion, blank=True, max_length=20)
    physical_status = models.CharField(choices=Physical_Status,max_length=20, blank=True)
    eating_habit = models.CharField(choices=Eating_Habit, blank=True, max_length=20)
    drinking_habit = models.CharField(choices=Drinking_Habit, blank=True, max_length=20)
    smoking_habit = models.CharField(choices=Smoking_Habit, blank=True, max_length=20)
    religion = models.CharField(choices=Religion_Status, blank=True, max_length=20)

    phone = models.CharField(max_length=11, blank=True)
    parents_phone = models.CharField(max_length=11, blank=True)
    whatsapp = models.CharField(max_length=11, blank=True)

    country = models.CharField(max_length=30, blank=True)
    citizenship = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    city = models.CharField(blank=True, max_length=100)

    education = models.CharField(max_length=30, blank=True, choices=Education_Status)
    education_details = models.TextField(max_length=200, blank=True)
    employed = models.CharField(max_length=50, blank=True)
    occupation = models.TextField(max_length=100,blank=True)
    annual_income = models.PositiveIntegerField(default=0)

    family_Value = models.CharField(blank=True, max_length=30)
    family_type = models.CharField(blank=True, max_length=30)
    family_status = models.CharField(choices=Family_Status,blank=True, max_length=30)
    father_status = models.CharField(blank=True, max_length=30)
    family_location = models.CharField(blank=True, max_length=30)
    about_family = models.TextField(max_length=200, blank=True)

    # Patner Preference
    p_age = models.PositiveIntegerField(default=18)
    p_height = models.PositiveIntegerField(default=0)
    p_weight = models.FloatField(default=0.0)
    p_mother_tongue = models.CharField(blank=True, max_length=30)
    p_physical_status = models.CharField(choices=Physical_Status,max_length=20, blank=True)
    p_eating_habit = models.CharField(choices=Eating_Habit, blank=True, max_length=20)
    p_drinking_habit = models.CharField(choices=Drinking_Habit, blank=True, max_length=20)
    p_smoking_habit = models.CharField(choices=Smoking_Habit, blank=True, max_length=20)
    p_religion = models.CharField(choices=Religion_Status, blank=True, max_length=20)
    p_body_type = models.CharField(choices=Body_type, blank=True, max_length=12)
    p_complexion = models.CharField(choices=Complexion, blank=True, max_length=20)
    p_family_status = models.CharField(choices=Family_Status, blank=True, max_length=30)

    p_education = models.CharField(max_length=30, blank=True, choices=Education_Status)
    p_occupation = models.TextField(max_length=100,blank=True)
    p_annual_income = models.PositiveIntegerField(default=0)

    p_country = models.CharField(max_length=30, blank=True)
    p_citizenship = models.CharField(max_length=30, blank=True)
    p_state = models.CharField(max_length=30, blank=True)
    p_city = models.CharField(blank=True, max_length=100)



    following = models.ManyToManyField(CustomUser, blank=True, related_name="following")
    viewer = models.ManyToManyField(CustomUser, blank=True, related_name="viewer")
    see_contract = models.ManyToManyField(CustomUser,related_name="see_contract",blank=True)
    send_request = models.ManyToManyField(CustomUser,related_name="send_request",blank=True)
    receive_request = models.ManyToManyField(CustomUser,related_name="receive_request",blank=True)

    friends = models.ManyToManyField(CustomUser,blank=True,related_name="friends")
    friend_request = models.ManyToManyField(CustomUser,blank=True,related_name="friend_request")
    friend_send = models.ManyToManyField(CustomUser,blank=True,related_name="friend_send")

    def __str__(self):
        return '{}-{}'.format(str(self.email),str(self.following.count()))

    def count_viewr(self):
        return self.viewer.count()

    def get_absolute_url(self):
        return reverse('viewprofile', kwargs={'id': self.id})
    def get_view(self):
        return self.viewer.count()
    def get_follow(self):
        return self.following.count()

    def top_3(self):
        u=Profile.objects.all()
        r=[]
        for p in u:
            r.append(p.get_follow())
        return r

    def redaytogo(self):
        if self.age!='' and self.height!='' and self.weight!='' and self.city!='' and self.education!='' and self.annual_income!='' and self.gender!='' and self.body_type!='' and self.complexion!='' and self.drinking_habit!='' and self.smoking_habit!='' and self.religion!='' and self.family_status!='' and self.marital_status!='' and self.physical_status!='':
            return True
        else:
            return False


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(email=instance)
        print(instance.is_active)



@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=CustomUser)
def change_profile(sender, instance, created, **kwargs):
    if instance.is_active ==True:
        print("ok")
    else:
        print("yeah")

@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

class FriendList(models.Model):
    Friend_Status = (
        ('Pending', 'Pending'),
        ('Accept', 'Accept'),
    )
    owner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="owner")
    request_Sent = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="request_Sent")
    contract = models.CharField(choices=Friend_Status,max_length=12)

    def __str__(self):
        return str(self.owner)
class ContractUs(models.Model):
    name = models.CharField(max_length=50,blank=False)
    email = models.EmailField(max_length=50,blank=False)
    message = models.TextField(max_length=500,blank=False)
    reply = models.TextField(max_length=500,blank=True)
    replied = models.BooleanField(default=False,max_length=10)
    receive_on = models.DateTimeField(auto_now_add=False,auto_now=True)

    def clean(self):
        reply =self.reply
        if reply !=None:
            print("go")
        replied=self.replied
        if replied:
            mail_subject = 'Message Reply'
            message = render_to_string('user/messagereply.html', {
                'user': self.name,
                'msg':reply,
            })
            to_email = self.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

    def __str__(self):
        return str(self.email)

class Messeges(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="receiver")
    subject = models.CharField(max_length=50,blank=False,default="subject")
    sender_msg = models.TextField(max_length=300,blank=False)
    receiver_msg = models.TextField(max_length=300,blank=False)
    send_on = models.DateTimeField(auto_now=True,auto_now_add=False)
    reply_on = models.DateTimeField(auto_now_add=False,auto_now=True)


    def __str__(self):
        return str(self.id)

    def demotext(self):
        return self.sender_msg[:50]
    def demoreply(self):
        return self.receiver_msg[:50]

    def sender_count(self):
        return self.sender.objects.count()

from ckeditor.fields import RichTextField
class SuccessStory(models.Model):
    post_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    post_on = models.DateField(auto_now=True,auto_now_add=False)
    describe = RichTextField(blank=False,default="write your succes story here")
    photo = models.ImageField(upload_to="successStory/",blank=False,default="success.jpg")
    likes = models.ManyToManyField(CustomUser,related_name="likes",blank=True)
    approve = models.BooleanField(default=False)

    def __str__(self):
        return str(self.post_by)

    def sample(self):
        return self.describe[:100]
    def get_absolute_url(self):
        return reverse('viewstory', kwargs={'id': self.id})

class Comment(models.Model):
    post = models.ForeignKey(SuccessStory,on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment',on_delete=models.CASCADE,null=True,related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post,str(self.user))