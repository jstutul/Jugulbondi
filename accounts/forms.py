from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import Profile,Comment,SuccessStory
User=get_user_model()
import re
class UsercreationForm(forms.ModelForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2=forms.CharField(label='Password Confirmation',widget=forms.PasswordInput)
    class Meta:
        model = User
        fields  = ('email', 'first_name', 'last_name')
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        if len(password1) < 8:
            raise forms.ValidationError("password must be 8 character")
        elif password1 != password2:
            raise forms.ValidationError("password are not matching")
        return password2
    def save(self,commit=True):
        user=super().save(commit=False)
        user.set_password(self.cleaned_data.get('password2'))

        if commit:
            user.save()
        return user
class UserchangeForm(forms.ModelForm):
    password =ReadOnlyPasswordHashField()
    class Meta:
        model=User
        fields =('email','password','first_name','last_name','is_staff','is_superuser')
    def clean_password(self):
        return self.initial['password']


class CompleteProfile(forms.ModelForm):
    class Meta:
        model =Profile
        fields =('about','age','photo','height','weight','gender','mother_tongue','marital_status')

class CommentForm(forms.ModelForm):
    content = forms.CharField(label="",widget=forms.Textarea(attrs={
        'class':'form-control',
        'id':'comm',
        'rows':3,
        'cols':40,
        'padding':'10px',
        'placeholder':"Enter  your Text here",
    }))
    class Meta:
        model = Comment
        fields = ['content']

class SuccessForm(forms.ModelForm):
    describe = forms.CharField(label="",widget=forms.Textarea(attrs={
        'class':'form-control',
        'id':'comm',
        'rows':10,
        'cols':40,
        'padding':'10px',
        'placeholder':"Enter  your Text here",
    }))
    class Meta:
        model = SuccessStory
        fields =['describe','photo']
class PatnerSearchForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['age','height','weight','city','education','annual_income','gender','body_type','complexion','drinking_habit',
                  'smoking_habit','religion','family_status','physical_status']


def isValid(s):
    Pattern = re.compile("[a-zA-Z]+")
    return Pattern.match(s)
def INNT(n):
    Pattern = re.compile("[0-9]")
    return Pattern.match(n)
class ProfileUpdated(forms.ModelForm):
    about=forms.TextInput()
    age=forms.IntegerField(label="Age")
    height=forms.IntegerField(label="Height")
    weight=forms.IntegerField(label="Weight")
    mother_tongue=forms.CharField(label="Mother Tongue",widget=forms.TextInput())
    phone=forms.CharField(label="Phone",widget=forms.TextInput())
    parents_phone=forms.CharField(label="Phone",widget=forms.TextInput())
    whatsapp=forms.CharField(label="Phone",widget=forms.TextInput())
    country=forms.CharField(label="Country",widget=forms.TextInput())
    citizenship=forms.CharField(label="Citizenship",widget=forms.TextInput())
    state=forms.CharField(label="State",widget=forms.TextInput())
    city=forms.CharField(label="City",widget=forms.TextInput())
    education_details=forms.CharField(label="Education Details",widget=forms.TextInput())
    employed=forms.CharField(label="Employee in",widget=forms.TextInput())
    occupation=forms.CharField(label="Occupation",widget=forms.TextInput())
    p_occupation=forms.CharField(label="Patner Occupation",widget=forms.TextInput())
    family_Value=forms.CharField(label="Family Value",widget=forms.TextInput())
    family_type=forms.CharField(label="Family Type",widget=forms.TextInput())
    family_location=forms.CharField(label="Family Location",widget=forms.TextInput())
    about_family = forms.TextInput()
    p_age=forms.IntegerField(label="Panter Maxium Age")
    p_height=forms.IntegerField(label="Panter Maxium Height")
    p_weight=forms.FloatField(label="Panter Maxium Weight")
    class Meta:
        model=Profile
        fields =('about','photo','age','height','weight','gender','marital_status','mother_tongue',
                 'body_type','complexion','physical_status','eating_habit','drinking_habit','smoking_habit',
                 'religion','phone','parents_phone','whatsapp','country','citizenship','state','city',
                 'education','education_details','employed','occupation','annual_income','family_Value',
                 'family_type','family_status','family_location','about_family','p_age','p_height','p_weight',
                 'p_mother_tongue','p_physical_status','p_eating_habit','p_drinking_habit','p_smoking_habit',
                 'p_religion','p_body_type','p_complexion','p_family_status','p_education','p_occupation',
                 'p_annual_income','p_country','p_citizenship','p_state','p_city'
                 )
    def clean_about(self):
        about=self.cleaned_data.get("about")
        if len(about)<=50:
            raise ValidationError("** input length must be 50 character")
        elif isValid(about):
            return about
        else:
            raise ValidationError("** error input")
    def clean_age(self):
        age=self.cleaned_data.get("age")
        if age <18:
            raise ValidationError("** age must be greater then 18")
        else:
            return age
    def clean_height(self):
        height=self.cleaned_data.get("height")
        if height<50:
            raise ValidationError("** user height must be 50 inch")
        else:
            return height
    def clean_weight(self):
        weight=self.cleaned_data.get("weight")
        if weight>50:
            return weight
        else:
            raise ValidationError("** user weight must be 40 inch and positive")
    def clean_phone(self):
        phone=self.cleaned_data.get("phone")
        if INNT(phone):
            return phone
        else:
            raise ValidationError("** phone no must be 11 digit and number")
    def clean_parents_phone(self):
        parents_phone=self.cleaned_data.get("parents_phone")
        if INNT(parents_phone):
            return parents_phone
        else:
            raise ValidationError("** phone no must be 11 digit and number")

    def clean_whatsapp(self):
        whatsapp=self.cleaned_data.get("whatsapp")

        if INNT(whatsapp):
            return whatsapp
        else:
            raise ValidationError("**  must be  number")

    def clean_country(self):
        country=self.cleaned_data.get("country")

        if isValid(country):
            return country
        else:
            raise ValidationError("** wrong input")
    def clean_citizenship(self):
        citizenship=self.cleaned_data.get("citizenship")
        if isValid(citizenship):
            return citizenship
        else:
            raise ValidationError("** wrong input")

    def clean_state(self):
        state=self.cleaned_data.get("state")
        if isValid(state):
            return state
        else:
            raise ValidationError("** wrong input")

    def clean_city(self):
        city=self.cleaned_data.get("city")
        if isValid(city):
            return city
        else:
            raise ValidationError("** wrong input")
    def clean_education_details(self):
        education_details=self.cleaned_data.get("education_details")
        if isValid(education_details):
            return education_details
        else:
            raise ValidationError("** wrong input")
    def clean_employed(self):
        employed=self.cleaned_data.get("employed")
        if isValid(employed):
            return employed
        else:
            raise ValidationError("** wrong input")
    def clean_occupation(self):
        occupation=self.cleaned_data.get("occupation")
        if isValid(occupation):
            return occupation
        else:
            raise ValidationError("** wrong input")
    def clean_family_Value(self):
        family_Value=self.cleaned_data.get("family_Value")
        if isValid(family_Value):
            return family_Value
        else:
            raise ValidationError("** wrong input")
    def clean_family_type(self):
        family_type=self.cleaned_data.get("family_type")
        if isValid(family_type):
            return family_type
        else:
            raise ValidationError("** wrong input")
    def clean_family_location(self):
        family_location=self.cleaned_data.get("family_location")
        if isValid(family_location):
            return family_location
        else:
            raise ValidationError("** wrong input")
    def clean_about_family(self):
        about_family=self.cleaned_data.get("about_family")
        if isValid(about_family):
            return about_family
        else:
            raise ValidationError("** wrong input")
    def clean_p_occupation(self):
        p_occupation=self.cleaned_data.get("p_occupation")
        if isValid(p_occupation):
            return p_occupation
        else:
            raise ValidationError("** wrong input")


