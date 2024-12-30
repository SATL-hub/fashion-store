from django.shortcuts import render,redirect
from .models import *
# Create your views here.
import random
from django.http import JsonResponse
#from django.db.models import Prefetch
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
import re

def home(request):
    offer = Offers.objects.all()
    categories = Category.objects.all()
   
    products = Product.objects.all()
    max_price = products.aggregate(max_price=models.Max('price'))['max_price'] or 0
    featured_items = random.sample(list(products),3)
    
    categories_data = [
        {
            'category':category.name,
            'unique_products':list(set(product.name for product in category.products.all()))
        }for category in categories
    ]
    return render(request,'index.html',{"offers":offer,'categories':categories_data,"max":max_price,'featured_items':featured_items,'products':products[:3]})

def filter_products(request,category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category).select_related('category')

    # Serialize the product data
    products_data = [
        {
            'name': prod.name,
            'price': prod.price,
            'category': prod.category.name,  # Use the category's name
            'image': prod.image.url if prod.image else None,  # Handle cases with no image
        } for prod in products
    ]

    return JsonResponse({'products': products_data})
def product_details(request,name='null',a='null'):
   
    products=Product.objects.filter(name=name)

    products_data=[
        {
            'id':prod.id,
            'category':prod.category.name,
            'name':prod.name,
            'price':prod.price,
            'image':prod.image.url
        }for prod in products
    ]
    return JsonResponse({'products':products_data})

def filter_products_by_price(request):
    min_price = request.GET.get('min_price', 0)  
    max_price = request.GET.get('max_price', float('inf'))  

    try:
       
        min_price = float(min_price)
        max_price = float(max_price)
    except ValueError:
        return JsonResponse({'error': 'Invalid price range'}, status=400)

  
    products = Product.objects.filter(price__gte=min_price, price__lte=max_price)

    
    products_data = [
        {
            'id':product.id,
            'name': product.name,
            'price': product.price,
            'category': product.category.name,
            'image': product.image.url if product.image else None,
        }
        for product in products
    ]
    return JsonResponse({'products': products_data})

def userlogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if Userprofile.objects.filter(email=email).exists():
            user = Userprofile.objects.get(email=email)
            if password == user.password:
                request.session['user_id']=user.id
                request.session['name'] = user.name
                return redirect('home')
            else:
                messages.error(request,'password mismatch',extra_tags="loginerror_tags")
                return redirect('userlogin')
        else:
            messages.error(request,"user doesn't exists",extra_tags="loginerror_tags")
            return redirect('userlogin')
    return render(request,'login.html',{})

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if Userprofile.objects.filter( email=email).exists():
            return render(request,'login.html',{"message":"User already exists"})
        else:
            if password == repassword:    
                user=Userprofile.objects.create(name=name,email=email,password=password)
                user.save()
            else:
                return render(request,'login.html',{"message":"password mismatch"})
            return redirect(reverse('userlogin'))
    return redirect(reverse('userlogin'))    

def userlogout(request):
    request.session.flush()
    return redirect('home')


def profile(request,id):
    if request.method=="POST":
        name= request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        pic = request.FILES.get('img')
        if pic == None:
            pic = Profilepic.objects.get(user=Userprofile.objects.get(id=id)).propic
        file = request.FILES.get('file')
        if file == None:
            file = Profilepic.objects.get(user=Userprofile.objects.get(id=id)).resume
        print("file",file)
        print("pic",pic)
        print("email",email)
        print("phone",phone)
        print("name",name)
        user = Userprofile.objects.get(id=id)
        user.name=name
        user.email=email
        user.save()
        print("user",user)
        #if Profile.objects.filter(user=user).exists():
        profiles = Profile.objects.filter(user=user).first()
        profilepic = Profilepic.objects.filter(user=user).first()
        if profiles:
            profiles.user=user
            profiles.name=name
            profiles.email=email
            profiles.phone=phone
            profiles.save()
        if profilepic:
            profilepic.user=user
            profilepic.propic=pic
            profilepic.resume=file
            profilepic.save()
        else:
            profi=Profile.objects.create(user=user,name=name,email=email,phone=phone)
            profi.save()
            profilepic = Profilepic.objects.create(user=user,propic=pic,resume=file)
            profilepic.save()
        return redirect('home')
    else:
        user=Userprofile.objects.get(id=id)
        print("user",user)
        if Profile.objects.filter(user=user).exists():
            profiles= Profile.objects.get(user=user)
            profilepic=Profilepic.objects.get(user=user)
        
            return render(request,'profile.html',{'user':user,"profile":profiles,'profilepic':profilepic})
        else:
            request.session['user_id']=user.id
            return render(request,'profile.html',{'user':user})

def cart(request):
    if request.method=="POST":
        if request.session.get('name') is None:
            return redirect('userlogin')
        name = request.session.get('name')
        user = Userprofile.objects.get(name=name)
        id = request.POST.get('product_id')
        count=request.POST.get('quantity')
        size = request.POST.get('size')
        color=request.POST.get('color')
        product = Product.objects.get(id=id)
        total_price = total(product.price,count)
        print("hiii")
        cart = Usercart.objects.create(user=user,product=product,no_of_item=count,size=size,color=color,individual_price=product.price,total_price=total_price)
        cart.save()
        carts = Usercart.objects.filter(user=user)
        print("userrrrrrrrr",user.id)
        return render(request,'cart.html',{'carts':carts,'user':user})
    else:
        if request.session.get('name') is None:
            return redirect('userlogin')
        name = request.session.get('name')
        user = Userprofile.objects.get(name=name)
        print("userrrrrrrrr",user.id)
        carts = Usercart.objects.filter(user=user)
        return render(request,'cart.html',{'carts':carts,'user':user})
def total(price,count):
    return int(price)*int(count)
def contact(request):
    return render(request,'contact-us.html',{})

def details(request,id):
    product = Product.objects.get(id=id)
    productvariation=ProductVariation.objects.filter(product=product)
    productimages = Product_images.objects.get(product=product)
    reviews = Reviews.objects.filter(product=product)
    return render(request,'product-details.html',{"product":product,"productvariation":productvariation,"productimages":productimages,'reviews':reviews,'rating_range':[5,4,3,2,1]})


def minuscart(request, de):
    cart = Usercart.objects.get(id=de)
    if cart.no_of_item > 1:
        cart.no_of_item = cart.no_of_item - 1
        cart.total_price=cart.individual_price*cart.no_of_item
        cart.save()
    else:
        cart.delete()
    return redirect('cart')


# Increasing cart items

def pluscart(request, de):    
    cart = Usercart.objects.get(id=de)
    cart.no_of_item = cart.no_of_item + 1
    cart.total_price=cart.individual_price*cart.no_of_item
    cart.save()
    return redirect('cart')

def deletecart(request, de):
    cart = Usercart.objects.get(id=de)
    cart.delete()
    return redirect('cart')

def check_out(request,id):
    if request.method =='POST':
        firstname=request.POST.get('firstname')
        middlename=request.POST.get('middlename')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        address=request.POST.get('address')
        pin=request.POST.get('pin')
        country=request.POST.get('country')
        state=request.POST.get('state')
        mobile=request.POST.get('mobile')
        message=request.POST.get('message')
        user= Userprofile.objects.get(id=id)
        cart = Usercart.objects.filter(user=user)
        amount = request.POST.get('whole_value')
        
        if request.POST.get('pay_mode'):
            print("paymode",request.POST.get('pay_mode'))
            if request.POST.get('pay_mode')=='Pay_On_delivery':
                orders = Orderitems.objects.create(user=user,first_name=firstname,middile_name=middlename,last_name=lastname,email=email,address=address,pin=pin,country=country,
                                               state=state,mobile=mobile,message=message,payment_mode='Pay_On_Delivery',status='Pending')
                orders.save()
                for i in cart:
                    hist = History.objects.create(user=user,item=i.product.name,image=i.product.image,no_of_item=i.no_of_item,size=i.size,color= i.color,
                                              individual_price = i.individual_price,total_price=i.total_price,payment_mode='Pay_On_Delivery',status='Pending')
                    hist.save()
                Usercart.objects.filter(user=user).delete()
                return redirect('home')
            elif request.POST.get('pay_mode')=='Online_Payment':
                orders = Orderitems.objects.create(user=user,first_name=firstname,middile_name=middlename,last_name=lastname,email=email,address=address,pin=pin,country=country,
                                               state=state,mobile=mobile,message=message,payment_mode='Online_Payment',status='Pending')
                orders.save()
                for i in cart:
                    hist = History.objects.create(user=user,item=i.product.name,image=i.product.image,no_of_item=i.no_of_item,size=i.size,color= i.color,
                                              individual_price = i.individual_price,total_price=i.total_price,payment_mode='Online_Payment',status='Pending')
                    hist.save()   
                Usercart.objects.filter(user=user).delete()
 
                return redirect('home')    
        else:
            print("none mode")
            return render(request,'checkout.html',{'carts':cart,'user':user})
    else:
        print("id",id)
        user= Userprofile.objects.get(id=id)
        cart = Usercart.objects.filter(user=user)
        return render(request,'checkout.html',{'carts':cart,'user':user})

def wishlist(request,id):
    product = Product.objects.get(id=id)
    print("user",request.session['name'])
    print("product",product)
    wishes = Wish_list.objects.create(product=product,user=Userprofile.objects.get(name=request.session['name']) )
    wishes.save()
    print("saved")
    return redirect('home')

def wishlists(request,id):
    user = Userprofile.objects.get(id=id)
    print("user",user)
    wishes = Wish_list.objects.filter(user=user)
  
    return render(request,'wishlist.html',{"wishes":wishes})

def shop(request):
    categories = Category.objects.all()
   
    products = Product.objects.all()
    max_price = products.aggregate(max_price=models.Max('price'))['max_price'] or 0
    
    categories_data = [
        {
            'category':category.name,
            'unique_products':list(set(product.name for product in category.products.all()))
        }for category in categories
    ]
    return render(request,'shop.html',{'categories':categories_data,"max":max_price,'products':products})

def product_review(request,id):
    product = Product.objects.get(id=id)
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    print("message",message)
    rating = request.POST.get('rating')
    if Userprofile.objects.filter(email=email).exists():    
        user = Userprofile.objects.get(email=email)
    else:
        return redirect('userlogin')
    review = Reviews.objects.create(user=user,product=product,message=message,rating=rating)
    review.save()
    return redirect('product_detail', id=id)

def changepassword(request):
    if request.method=="POST":
        print("method is POST")
        opass = request.POST.get('opass')
        npass = request.POST.get('npass')
        rpass = request.POST.get('rpass')
        if npass ==rpass:
            y = re.search("(?=.{8,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^&*?])", npass)
            if y==None:
                return redirect('changepassword')
            else:
                id = request.session.get('user_id')
                user = Userprofile.objects.get(id=id)
                user.password=npass
                user.save()
                return redirect('userlogin')
        else:
            return redirect('changepassword')
    else:
        id = request.session.get('user_id')
        print("id",id)
        user= Userprofile.objects.get(id=id)
        return render(request,"changepassword.html",{"user":user})
    
def history(request):
    id = request.session.get('user_id')
    user= Userprofile.objects.get(id=id)
    hists = History.objects.filter(user=user)
    return render(request,'history.html',{'hists':hists})