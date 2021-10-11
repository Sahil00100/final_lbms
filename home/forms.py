from django import forms

from django.contrib.auth.models import User
from home.models import ClassName,RatingAndReview,Order,ReturnOrder,Otp,Book
from django.core.validators import RegexValidator

class SignupForm(forms.Form):
    #validators
    alphanumeric = RegexValidator(r'^[a-zA-Z]*$', 'Only alphabetic characters are allowed.')
    numbers=RegexValidator(r'^[0-9]*$','only numbers allowed')
    #form elements
    name=forms.CharField(max_length=100,required=True,validators=[alphanumeric])  
    email=forms.EmailField(required=True)
    password1=forms.CharField(widget=forms.PasswordInput,required=True)
    password2=forms.CharField(widget=forms.PasswordInput,required=True)
    mobile_number=forms.CharField(max_length=10,validators=[numbers],required=True)
    class_name=forms.CharField(max_length=100,required=True,validators=[alphanumeric])
    

  

    #clean email
    def clean_email(self):
        email=self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            
            raise forms.ValidationError('Using this email already an account created,use another email')
                
        else:
            return email
    
    #clean username
    def clean_name(self):
        username=self.cleaned_data.get('name')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Used name ,take another one')
        else:
            return username
    
    #clean passwords
    def clean_password2(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        
        if password1 and password2 and password1!=password2:
           raise forms.ValidationError('Password incorrect! try again')
        else:
            return password2

    #clean mobile number
    def clean_mobile_number(self):
        mobile=self.cleaned_data.get('mobile_number')
        if ClassName.objects.filter(mobile_number=mobile).exists():
            raise forms.ValidationError('Mobile Number already used!')
        else:
            return mobile
        #clean class
    def clean_class_name(self):
        class_of_user=self.cleaned_data.get('class_name')
        return class_of_user

    #create user
    def create_user(self):
        user=User.objects.create_user(
            username=self.clean_email(),
            first_name=self.clean_name(),
            email=self.clean_email(),
            password=self.clean_password2()
            )
        user.save()
        return user
    
    #create classname
    def create_classname(self):
        
        class_name=ClassName(
            name_of_user=self.cleaned_data.get('email'),
            class_of_user=self.clean_class_name(),
            mobile_number=self.clean_mobile_number()
            )
        class_name.save()
#book form
class BookForm(forms.ModelForm):

    class Meta:
        model=Book
        fields=['name_of_book','photo1','photo2','photo3','auther','category','description','number_of_copies','page1','page2','page3']
