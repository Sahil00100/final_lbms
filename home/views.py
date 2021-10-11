from django.shortcuts import render,redirect,reverse,HttpResponseRedirect,HttpResponse
from .models import Book,Order,RatingAndReview,ReturnOrder,Otp,ClassName,Membership,CreateCombetition,Combetition,Order2,Penalty,Cart,Membership
from.forms import SignupForm,BookForm
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib import messages
import datetime
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
import time
import os
from twilio.rest import Client 
import twilio
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.
# Home page view

def index_view(request):
    #latest 4 books
    
    
    latest=Book.objects.order_by('-id')
    
    """
    -----------------------------------------------------
    This will delete books after 24 hour if not collected
    -----------------------------------------------------
    """
    q=Order.objects.all()
    comb=CreateCombetition.objects.all().order_by('-id')

    for i in q:
        x=i.date+datetime.timedelta(days=1)
        print(i.date)
        print(x)
        if i.date>x and i.order_submit==False:
            i.delete()
        else:
            print("hahhahaha")
    """
    ------------------------------------------------------
    """
    
    return render(request,'index.html',
    {
        'latest':latest,
        'comb':comb,
        'media_url':settings.MEDIA_URL,
        }
        )


def send_otp(name_of_user):
    """
    <----SMS---->
    """
    number=ClassName.objects.get(name_of_user=name_of_user)
    num_list=Otp.objects.get(name_of_user=name_of_user)
    number=number.mobile_number
    num_list=num_list.otp_number
    n=str(number)
    otp=str(num_list)
    account_sid = 'AC0a22647ef8de5bbafdb0d6e592d41354' 
    auth_token = 'be55fd28b25aeeffeaade967a4c00c17' 
    client = Client(account_sid, auth_token) 
 
    message = client.messages.create(  
            body='YOUR ONE TIME PASSWORD IS '+otp,
            from_='+13393095686',       
            to='+91'+n 
        )
    print("kooooiii",message.sid)
#resend otp function
def resend_otp(request,name_of_user):
    
    
    if request.method=='POST':
        otp=request.POST['otp']
        otp=int(otp)
        print(otp)
        obj=Otp.objects.get(name_of_user=name_of_user)
        otp_of_obj=int(obj.otp_number)
        print(otp_of_obj)
        
        if otp_of_obj==otp:
            print('success')
            x=User.objects.get(username=name_of_user)
            x.is_active=True
            x.save()
            return redirect('login')
        else:         
            print("otp is not correct!")  
    else:
        num_list=random.randrange(1001,9999)
        obj=Otp.objects.get(name_of_user=name_of_user)
        obj.otp_number=num_list
        obj.save()
        send_otp(name_of_user)
    return render(request,'otp.html',{'name_of_user':name_of_user})
    
#otp
def otp_view(request,name_of_user):
    
    if request.method=='POST':
        otp=request.POST['otp']
        otp=int(otp)
        print(otp)
        obj=Otp.objects.get(name_of_user=name_of_user)
        otp_of_obj=int(obj.otp_number)
        print(otp_of_obj)
        
        if otp_of_obj==otp:
            print('success')
            x=User.objects.get(username=name_of_user)
            x.is_active=True
            x.save()
            return redirect('login')
        else:         
            print("otp is not correct!")  
            
    return render(request,'otp.html',{'name_of_user':name_of_user})

# signup
def signup_view(request):
    
    if request.method=='POST':      
        form=SignupForm(request.POST)
        name=request.POST['email']
        pswd=request.POST['password1']
        if User.objects.filter(email=name,is_active=False).exists() and ClassName.objects.filter(name_of_user=name):
                num_list=random.randrange(1001,9999)
                obj=Otp.objects.get(name_of_user=name)
                obj.otp_number=num_list
                print(1)
                obj.save()
                user=User.objects.get(email=name,is_active=False)
                user.set_password(pswd)
                user.save()
                print('saved')
                send_otp(name)
                return redirect('otp',name)
        elif form.is_valid():
            num_list=random.randrange(1001,9999)
            name=request.POST['email']
            if User.objects.filter(username=name,is_active=False):
                send_otp(name)
                return redirect('otp',name)
            else:
                
                if Otp.objects.filter(name_of_user=name).exists():
                    print(2)
                    obj=Otp.objects.get(name_of_user=name)
                    obj.otp_number=num_list
                    obj.save()
                    x=form.create_user()
                    x.is_active=False
                    x.save()
                    
                    form.create_classname()
                    send_otp(name)
                    return redirect('otp',name)
                

                else:
                    print(3)
                    obj=Otp(name_of_user=name,otp_number=num_list)
                    obj.save()
                    x=form.create_user()
                    User.is_active=False
                    form.create_classname()
                    x.is_active=False
                    x.save()
                    print("valid")
                    send_otp(name)
                    return redirect('otp',name)
        else:
            print('not valid')
            
    else:
        form=SignupForm
    return render(request,'signup.html',{'form':form})

# Login

def login_view(request):
    if request.method=='POST':
        name=request.POST['name']
        password=request.POST['password']
        user=authenticate(
            request,
            username=name,
            password=password
            )

        if user is not None:
            login(request,user)
            print(user)
            
            return redirect('membership')
        else:
            messages.add_message(
                request,
                messages.INFO,
                'Invalid Username or password'
                )
    else:
        return render(request,'login.html',{})
    return render(request,'login.html',{})

#log out
def logout_view(request):
    logout(request)
    print('logout success!')
    return redirect('login')

#product view

def product_view(request,name_of_book):
    
    print(name_of_book)
    book=Book.objects.get(name_of_book=name_of_book)

    


    book=Book.objects.filter(id=book.id)
    book2=Book.objects.get(name_of_book=name_of_book)
    review=RatingAndReview.objects.filter(name_of_book=book2)
    #rate
    all_rates=RatingAndReview.objects.filter(name_of_book=book2)
    length=len(all_rates)
    sume=0

    for x in all_rates:
        y=x.rate
        sume=sume+y

    if length==0:
        length=1
        rate=sume/length
    else:
        rate=sume/length
    print(rate)

    # availablity-of-products
    obj=Book.objects.get(name_of_book=name_of_book)
    total_p=obj.number_of_copies
    print(total_p)
    if total_p==0:
        print("empty")
        total_p1='Not available'
    else:
        print("hi")
        total_p1='available'
    if request.user.is_authenticated:
        if Order.objects.filter(name=request.user,book=book2,order_submit=False).exists():
            return render(request,'book2.html',{'book':book,'rate':rate,'review':review,"t":total_p1})
        else:
            return render(request,'book.html',{'book':book,'rate':rate,'review':review,"t":total_p1 })
    else:
        return render(request,'book.html',{'book':book,'rate':rate,'review':review,"t":total_p1 })
    
#order
@login_required(login_url='login')
def order_view(request,name_of_book):
 
    name=request.user
    book=Book.objects.get(name_of_book=name_of_book)
    order_submit=False
    today=datetime.datetime.today()
    expire=today + datetime.timedelta(days=10)
    print(expire)
    # availablity-of-products
    obj=Book.objects.get(name_of_book=name_of_book)
    total_p=obj.number_of_copies
    if total_p==0:
        messages.add_message(
                request,
                messages.INFO,
                'order is not available'
                )
        return redirect('product',name_of_book=name_of_book)
    else:
        order=Order.objects.get_or_create(
            name=name,
            book=book,
            order_submit=order_submit,
            date=today,
            return_date=expire
            )
        order2=Order2.objects.get_or_create(
            name=name,
            book=book,
            order_submit=order_submit,
            date=today,
            return_date=expire
        )
        #substracting books
        book.number_of_copies=book.number_of_copies-1
        book.save()
        print(book.number_of_copies)
        return redirect('index')
    
    
#cancel order
@login_required(login_url='login')
def order_delete(request,name_of_book):
    name=request.user
    book=Book.objects.get(name_of_book=name_of_book)
    x=int(book.number_of_copies)
    x=x+1
    book.number_of_copies=x
    book.save()
    order=Order.objects.filter(name=name,book=book)
    order.delete()
    order2=Order2.objects.filter(name=name,book=book).last()
    order_id=order2.id
    order2=Order2.objects.get(id=order_id)
    order2.cancel=True
    order2.save()
    
    return redirect('index')


#Rating and Review
@login_required(login_url='login')
def rate_and_review(request,name_of_book,):
    print('love')
    if request.method=='POST':
        
        rate=request.POST.get('r')
        
        review=request.POST.get('review')
        name=request.user
        book=Book.objects.get(name_of_book=name_of_book)
        print("success")
        print(rate)
        print(review)
        
        if RatingAndReview.objects.filter(name_of_book=book,name_of_user=name).exists():
                print('testing///')
                update=RatingAndReview.objects.get(
                    name_of_book=book,
                    name_of_user=name
                    )
                if rate=='0':
                    print('hei')
                    messages.add_message(
                    request,
                    messages.INFO,
                    'please do rate and review both'
                    )
                    
                    return redirect('product',name_of_book=name_of_book)
                else:
                    print('hello')
                    update.rate=rate
                    update.review=review
                    update.save()
                    return redirect('product',name_of_book=name_of_book)             
        else:
            
            q=RatingAndReview(
                name_of_book=book,
                name_of_user=name,
                rate=rate,
                review=review
            )
            q.save()
            return redirect('product',name_of_book=name_of_book)
        
            
       

    else:
        return redirect('product',name_of_book=name_of_book)
    

"""
-----------------
LIST OF PRODUCTS
-----------------

"""
def list_books(request):
    #search products-:
    if request.method=='POST':
        query=request.POST.get('search')
        print(query)
        books=Book.objects.filter(Q(name_of_book__contains=query))
    else:
        books=Book.objects.all()
    book1=Book.objects.all()
    book2=[]
    for x in book1:
        if x.category not in book2:
            book2.append(x)
        else:
            print('fek')


    return render(request,'product.html',
    {
        'books':books,
        'media_url':settings.MEDIA_URL,
        'book2':book2
        }
        )
#filter search
def filter_search(request,category):
    if request.method=="GET":

        book1=Book.objects.filter(category=category)
    else:
        book1=Book.objects.all()
    
    context={
        'book':book1
    }

    return render(request,'filter.html',context)

"""
    SORT PRODUCTS
"""
#latest-products
def latest(request):
    book=Book.objects.filter().order_by('-id')
    return render(request,'filter.html',{'book':book})


#membership page

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def membership_result(request):
    template='success.html'
    return render(request,template,{'x':'success'}) 
    
def membership(request):
    user=request.user
    if Membership.objects.filter(name_of_user=user).exists():
        return redirect('index')
    else:
        currency = 'INR'
        amount = 3000  # Rs. 30
 
    # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '/paymenthandler/'
 
    # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
 
        return render(request,'membership.html',context)


@csrf_exempt
def paymenthandler(request):
    print('hii')
    # only accept POST request.
    if request.method == "POST":
        
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print('success0',payment_id,razorpay_order_id,signature)
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 3000 # Rs. 30
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    print('success')
                    # render success page on successful caputre of payment
                    user=request.user
                    print(user)
                    x=Membership(
                        name_of_user=user
                        
                    )
                    x.save()

                    return redirect('result')
                except :
 
                    # if there is an error while capturing payment.
                    return redirect('index')
            else:
 
                # if signature verification fails.
                return redirect('index')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()


#profile view
def profile_view(request):

    user=request.user
    u=User.objects.get(email=user)
    u2=ClassName.objects.get(name_of_user=user)
    print(u.email)
    if Membership.objects.filter(name_of_user=request.user).exists():
        print('hi')
        return render(request,'profile.html',{'u':u,'u2':u2,'s1':'show','s2':'none'})
    else:
        print('hello')
        return render(request,'profile.html',{'u':u,'u2':u2,'s2':'show','s1':'none'})

#combetition view
@login_required(login_url='login')
def combetition(request,name_of_combetition):
    comb=CreateCombetition.objects.get(name_of_combetition=name_of_combetition)
    c=CreateCombetition.objects.get(name_of_combetition=name_of_combetition)

    if Combetition.objects.filter(name_of_user=request.user,name_of_combetition=c).exists():
        return redirect('index')

    if request.method=="POST":
        
        work=request.POST.get('work')
        user=User.objects.get(username=request.user)
        c=CreateCombetition.objects.get(name_of_combetition=name_of_combetition)

        x=Combetition(
            name_of_user=user,
            name_of_combetition=c,
            answer=work
        )
        x.save()
        print('good')
        return redirect('index')
    return render(request,'comb.html',{'comb':comb})
#publish-view

def publish_view(request):
    form=BookForm()
    if request.method=="POST":
        form=BookForm(request.POST,request.FILES)
        if form.is_valid():
            print('hi')
            form.save()
            return redirect('index')
        
    return render(request,'publish.html',{'book':form})
#orders_view
def orders(request):
    normal_books=Order2.objects.filter(cancel=False,return_order=False).order_by('-id')
    cancel_books=Order2.objects.filter(cancel=True).order_by('-id')
    return_order=Order2.objects.filter(return_order=True).order_by('-id')
    
    for i in normal_books:
        x=i.date+datetime.timedelta(days=10)
        print(i.date)
        print(x)
        if i.date>x:
            p_books=Order2.objects.filter(name=i.name,cancel=False)
            
            return render(request,'orders.html',{'p':p_books,'n':normal_books,'c':cancel_books,'r':return_order,'media_url':settings.MEDIA_URL})
    return render(request,'orders.html',{'n':normal_books,'c':cancel_books,'r':return_order,'media_url':settings.MEDIA_URL})

#penalty-view
def penalty_view(request):
    user=request.user
    if Penalty.objects.filter(name_of_user=user,penalty=0).exists():
        return redirect('index')
    else:
        x=Penalty.objects.get(name_of_user=user)
        p=x.penalty*100
        currency = 'INR'
        amount = p 
 
    # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        callback_url = '/penaltyhandler/'
 
    # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url
        context['p']=x.penalty
    return render(request,'penalty.html',context)

@csrf_exempt
def penalty_handler(request):
    print('hii')
    # only accept POST request.
    if request.method == "POST":
        
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            print('success0',payment_id,razorpay_order_id,signature)
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                x=Penalty.objects.get(name_of_user=request.user)
                p=x.penalty*100  
                amount = p
                
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    print('success')
                    # render success page on successful caputre of payment
                    user=request.user
                    print(user)
                    z=Penalty.objects.get(name_of_user=request.user)
                    
                    z.penalty=0
                    z.save()
                    

                    return redirect('result')
                except :
 
                    # if there is an error while capturing payment.
                    return redirect('index')
            else:
 
                # if signature verification fails.
                return redirect('index')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

#cart-view
@login_required(login_url='login')
def cart(request,name_of_book):
    book=Book.objects.get(name_of_book=name_of_book)
    user=User.objects.get(username=request.user)
    if Cart.objects.filter(name_of_book=book,name_of_user=user).exists():
        return redirect('product',name_of_book)
    else:
        x=Cart.objects.get_or_create(
            name_of_book=book,
            name_of_user=user
        )
        return redirect('product',name_of_book)
@login_required(login_url='login')
def cart_view(request):
    cart=Cart.objects.all().order_by('-id')
    return render(request,'cart.html',{'cart':cart,'media_url':settings.MEDIA_URL})
@login_required(login_url='login')
def cart_delete(request,name_of_book):
    book=Book.objects.get(name_of_book=name_of_book)
    user=User.objects.get(username=request.user)
    x=Cart.objects.filter(name_of_book=book,name_of_user=user)
    x.delete()
    return redirect('cart')

    
        