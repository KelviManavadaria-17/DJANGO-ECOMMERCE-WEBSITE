from django.http import request
from django.shortcuts import redirect, render
from django.views import View
from .models import Cart, Customer, OrderPlaced, Product
from .form import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages

class ProductView(View):
    def get(self,request):
        topwears = Product.objects.filter(category = 'TW')
        bottomwears = Product.objects.filter(category = 'BW')
        mobiles = Product.objects.filter(category = 'M')
        cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
        total_cart_quantity = sum(cart_quantity)
        context = {'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'total_cart_quantity':total_cart_quantity}
        return render(request,'store/home.html',context)



class ProductDetailView(View):
    def get(self,request,pk):
        item = Product.objects.get(pk =pk)
        cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
        total_cart_quantity = sum(cart_quantity)
        context = {'item' : item ,'total_cart_quantity':total_cart_quantity}
        return render(request, 'store/productdetail.html',context)

def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    products = Product.objects.get(id = product_id)
    cart_products = Cart.objects.filter(product = products).exists()
    
    if cart_products:
        item = Cart.objects.get (product = products)
        item.quantity += 1
        item.save()
    else: 
        Cart(user = user , product=products).save()
   
    
    return redirect('/cart/')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_products = Cart.objects.filter(user = user)
        context = {'cart_product':cart_products}
        amount = 0.0
        Shipping = 70.0
        total_amount = 0.0
        cart_products = [p for p in Cart.objects.all() if p.user == user]
        cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == user]
        total_cart_quantity = sum(cart_quantity)
        for p in cart_products:
            if p.quantity == 0:
                p.delete()

        if cart_products:
            for p in cart_products:
                tempam = p.quantity * p.product.discounted_price
                amount += tempam
                total_amount = amount + Shipping
             
            context = {'cart_product':cart_products ,'total_cart_quantity':total_cart_quantity ,'total_amount' : total_amount ,'Shipping':Shipping,'amount':amount}
            return render(request, 'store/addtocart.html',context)
        else :
            return render(request,'store/empty_cart.html')


def buy_now(request):
    cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
    total_cart_quantity = sum(cart_quantity)
    context = {'total_cart_quantity':total_cart_quantity}
    return render(request, 'store/buynow.html',context)



def address(request):
    add = Customer.objects.filter(user = request.user)
    cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
    total_cart_quantity = sum(cart_quantity)
    context = {'add':add,'total_cart_quantity':total_cart_quantity}
    return render(request, 'store/address.html',context)

def orders(request):
    op = OrderPlaced.objects.filter(user = request.user)
    cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
    total_cart_quantity = sum(cart_quantity)
    context = {'total_cart_quantity':total_cart_quantity , 'op':op}
    return render(request, 'store/orders.html',context)



def mobile(request,data=None):
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == 'BTS' or data == 'SAMSUNG' or data == 'POCO' or data =='Apple' or data =='VIVO':
        mobiles = Product.objects.filter(category = 'M').filter(brand = data)
    elif data == 'below':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gt=10000)
    cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
    total_cart_quantity = sum(cart_quantity)
    
    context = {'mobiles':mobiles,'total_cart_quantity':total_cart_quantity}
    return render(request, 'store/mobile.html',context)

def topwear(request,data=None):
    if data == None:
        top = Product.objects.filter(category = 'TW')
    elif data == 'HandM' or data == 'Lee' or data == 'Legends' or data =='Westsite' or data =='Pantlooms':
        top = Product.objects.filter(category = 'TW').filter(brand = data)
    elif data == 'below':
        top = Product.objects.filter(category = 'TW').filter(discounted_price__lt=800)
    elif data == 'above':
        top = Product.objects.filter(category = 'TW').filter(discounted_price__gt=800)
    cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
    total_cart_quantity = sum(cart_quantity)

    context = {'top':top ,'total_cart_quantity':total_cart_quantity}
    return render(request, 'store/topwear.html',context)

def bottomwear(request,data=None):
    if data == None:
        top = Product.objects.filter(category = 'BW')
    elif data == 'HandM' or data == 'Lee' or data == 'Legends' or data =='Westsite' or data =='Pantlooms':
        top = Product.objects.filter(category = 'BW').filter(brand = data)
    elif data == 'below':
        top = Product.objects.filter(category = 'BW').filter(discounted_price__lt=800)
    elif data == 'above':
        top = Product.objects.filter(category = 'BW').filter(discounted_price__gt=800)
    cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
    total_cart_quantity = sum(cart_quantity)

    context = {'bottom':top,'total_cart_quantity':total_cart_quantity}
    return render(request, 'store/bottomwear.html',context)

def login(request):
 return render(request, 'store/login.html')

class CustomerRegistrationView(View):
    def get(self,request):
        print("get")
        form = CustomerRegistrationForm()
        context = {'form':form}
        return render(request,'store/customerregistration.html',context)
    def post(self,request):
        print("post")
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congratulations!! Register Successfully")
            form.save()
            print("post")
        context = {'form':form}
        return render(request,'store/customerregistration.html',context)
        


def checkout(request):
    users = Customer.objects.filter(user= request.user)
    cart_items = Cart.objects.filter(user=request.user)
    amount = 0.0
    Shipping = 70.0
    total_amount = 0.0
    cart_products = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_products:
            for p in cart_products:
                tempam = p.quantity * p.product.discounted_price
                amount += tempam
                total_amount = amount + Shipping
    cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
    total_cart_quantity = sum(cart_quantity)
    context = {'total_cart_quantity':total_cart_quantity,'users':users,'cart_items':cart_items,'total_amount' : total_amount ,'Shipping':Shipping,'amount':amount}
    return render(request, 'store/checkout.html',context)


class Profile(View):
    def get(self, request):
        form = CustomerProfileForm()
        cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
        total_cart_quantity = sum(cart_quantity)
        context = {'form':form ,'total_cart_quantity':total_cart_quantity}
        return render(request,'store/profile.html',context)

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            rev = Customer(user = usr ,name=name , locality=locality,city=city,state=state,zipcode=zipcode)
            rev.save()
            messages.success(request,"Congratulations!! Profile Saved Successfully")
        cart_quantity = [p.quantity for p in Cart.objects.all() if p.user == request.user]
        total_cart_quantity = sum(cart_quantity)  
        context = {'form':form , 'active':'btn-primary','total_cart_quantity':total_cart_quantity}
        return render(request,'store/profile.html',context)

def RemoveItem(request):
    cart_id = request.GET.get('cart_id')
    pro = Cart.objects.get(id = cart_id).delete()
    print(pro)
    return redirect('/cart/')

def add_one(request,pk):
            
        cart_product = Cart.objects.get(id = pk)
        cart_product.quantity += 1
        cart_product.save()
        return redirect('/cart/')

def remove_one(request,pk=None):
    if pk == None:
        return redirect('/cart/')
    else:
        cart_product = Cart.objects.get(id = pk)
        cart_product.quantity -= 1
        cart_product.save()
        return redirect('/cart/')

def paymentdone(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id = custid)
    cart = Cart.objects.filter(user = user)
    for c in cart:
        OrderPlaced(user = user,customer = customer,product = c.product,quantity = c.quantity).save()
        c.delete()
    print(user)
    print(custid)
    print(customer)
    print(cart)

    return redirect('/orders/')

 