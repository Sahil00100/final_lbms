from django.db import models
from django.contrib.auth.models import User

import datetime

#signal imports
from django.dispatch import receiver
from django.db.models.signals import (
    pre_save,
    post_save,
)
# Create your models here.
class Book(models.Model):
    CATEGORY=sorted(
        [
        ('fantasy','fantasy'),
        ('adventure','adventure'),
        ('romance','romance'),
        ('contemporary','contemporary'),
        ('dystopian','dystopian'),
        ('mystery','mystery'),
        ('horror','horror'),
        ('thriller','thriller'),
        ('paranormal','paranormal'),
        ('historical_fiction','historical fiction'),
        ('science_fiction','science fiction'),
        ('memoir','memoir'),
        ('cooking','cooking'),
        ('art','art'),
        ('development','development'),
        ('motivational','motivational'),
        ('health','health'),
        ('history','history'),
        ('travel','travel'),
        ('humor','humor'),
    ]
    )
    
    
    name_of_book=models.CharField(max_length=200,unique=True)
    photo1=models.ImageField(upload_to='images')
    photo2=models.ImageField(upload_to='images')
    photo3=models.ImageField(upload_to='images')
    auther=models.CharField(max_length=200)
    category=models.CharField(max_length=200,choices=CATEGORY)
    description=models.TextField(max_length=1000)
    number_of_copies=models.IntegerField()
    page1=models.ImageField(upload_to='images')
    page2=models.ImageField(upload_to='images')
    page3=models.ImageField(upload_to='images')
    

    def __str__(self):
        return self.name_of_book

class ClassName(models.Model):
    name_of_user=models.CharField(max_length=100)
    class_of_user=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=10)

    def __str__(self):
        return self.name_of_user
        
class Order(models.Model):
    name=models.ForeignKey(User,models.CASCADE)
    book=models.ForeignKey(Book,models.CASCADE)
    order_submit=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now=False)
    return_date=models.DateTimeField(auto_now=False)
    x='------->'
    def __str__(self):
        return str(self.name)+self.x+str(self.date)+self.x+str(self.order_submit)

class Order2(models.Model):
    name=models.ForeignKey(User,models.CASCADE)
    book=models.ForeignKey(Book,models.CASCADE)
    order_submit=models.BooleanField(default=False)
    cancel=models.BooleanField(default=False)
    return_order=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now=False)
    return_date=models.DateTimeField(auto_now=False)
    x='------->'
    def __str__(self):
        return str(self.name)+self.x+str(self.date)+self.x+str(self.order_submit)

class ReturnOrder(models.Model):
    name=models.ForeignKey(User,models.CASCADE)
    book=models.ForeignKey(Book,models.CASCADE)
    order_return=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now=False)
    x='------->'
    def __str__(self):
       
        return str(self.name)+self.x+str(self.date)+self.x+str(self.order_return)

class RatingAndReview(models.Model):
    name_of_user=models.ForeignKey(User,models.CASCADE)
    name_of_book=models.ForeignKey(Book,models.CASCADE)
    review=models.TextField(max_length=500)
    rate=models.IntegerField()

    def __str__(self):
        return str(self.name_of_user)

class Cart(models.Model):
    name_of_user=models.ForeignKey(User,models.CASCADE)
    name_of_book=models.ForeignKey(Book,models.CASCADE)
    def __str__(self):
        return str(self.name_of_user)

C=(
        ('story','story'),
        ('poem','poem'),
    )
    
class CreateCombetition(models.Model):
    banner=models.ImageField(upload_to='images')
    type_of_combetition=models.CharField(choices=C,max_length=100)
    name_of_combetition=models.CharField(max_length=100)
    subject=models.CharField(max_length=100)
    language=models.CharField(max_length=100)
    min_words=models.IntegerField()
    max_words=models.IntegerField()
    first_prize=models.CharField(max_length=100)
    second_prize=models.CharField(max_length=100)
    third_prize=models.CharField(max_length=100)
    expire_date=models.DateTimeField(auto_now=False)
    def __str__(self):
        return str(self.name_of_combetition)
class Combetition(models.Model):
    name_of_user=models.ForeignKey(User,on_delete=models.CASCADE)
    name_of_combetition=models.ForeignKey(CreateCombetition,on_delete=models.CASCADE)
    answer=models.TextField()
    def __str__(self):
        return str(self.name_of_combetition)+str(self.name_of_user)
class Publish(models.Model):
    name_of_user=models.ForeignKey(User,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)

class Otp(models.Model):
    name_of_user=models.CharField(max_length=100)
    otp_number=models.CharField(max_length=4)
    #https://www.twilio.com/docs/sms/send-messages
class Membership(models.Model):
    name_of_user=models.CharField(max_length=100)
    
class Penalty(models.Model):
    name_of_user=models.CharField(max_length=100)
    penalty=models.IntegerField()

"""
------------
signals-area
------------
"""

# signals for order and create obj in return
@receiver(post_save, sender=Order)
def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    """
    after saved in the database
    """
    name=instance.name
    book=instance.book
    if instance.order_submit==True:
        if ReturnOrder.objects.filter(name=name,book=book).exists():
            print('product already saved')
        else:
                if created:
                    print("New object created")
                    r=ReturnOrder(
                        name=name,
                        book=book,
                        order_return=False,
                        date=datetime.datetime.today()

                    )
                    r.save()
                    
        
                else:
                    print(instance.name, "was  saved")
                    r=ReturnOrder(
                        name=name,
                        book=book,
                        order_return=False,
                        date=datetime.datetime.today()

                    )
                    r.save()
               
    else:
        print('order_submit==False')

# signal for return
@receiver(post_save,sender=ReturnOrder)
def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    name=instance.name
    book=instance.book

    if instance.order_return==True:
        x=Book.objects.get(name_of_book=book)
        x.number_of_copies=x.number_of_copies+1
        x.save()
        instance.delete()
        #order2=Order2.objects.get(name=name,book=book)
        order2=Order2.objects.filter(name=name,book=book).last()
        order_id=order2.id
        order2=Order2.objects.get(id=order_id)
        order2.return_order=True
        order2.save()
    else:
        print("return failed")