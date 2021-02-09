from django.shortcuts import render,HttpResponse,redirect
from .models import books
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . forms import sellbookform, ContactForm
from .models import Order,TrackUpdate
from django.core.mail import send_mail

def loginsignup(request):
    return render(request,'home/loginlink.html')
def home(request):
    allProds = []
    book = books.objects.all()
    categories = books.objects.values('category')
    ca = {item['category'] for item in categories}
    cats = list(ca)
    for cat in cats:
        prod = books.objects.filter(category = cat)
        allProds.append([prod,range(len(prod))])
    params = {'books':book, 'cats':cats, 'allProds':allProds}
    return render(request,'home/home.html',params)

def handleSignup(request):

    if request.method =='POST':
        username = request.POST['username']
        email = request.POST['signupemail']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if len(username) > 25:
            messages.error(request, "User name must be under 25 Characters")
            return redirect('/')
        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect('/')

        myuser = User.objects.create_user(username=username,email=email,password=pass2)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,'Your account has been created Successfully ')
        return redirect('/')
    else:
        return HttpResponse('NOT ALLOWED')

def handleLogin(request):
    loginusername = request.POST['loginusername']
    loginpass = request.POST['loginpass']
    user = authenticate(username=loginusername,password=loginpass)
    if user is not None:
        login(request,user)
        messages.success(request,"Successfully Logged In ")
        return redirect('/')
    else:
        messages.error(request,"Please Enter the username or password correctly!")
        return redirect('/')

@login_required(login_url='/loginsignup')
def handleLogout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect('/')

@login_required(login_url='/loginsignup')
def sellbook(request):
    context ={'form': sellbookform()}
    return render(request, "home/sellbook.html", context)

@login_required(login_url='/loginsignup')
def savebook(request):
    sellername = request.user.username
    book_name =  request.POST.get('book_name')
    category =  request.POST.get('category')
    price =  request.POST.get('price')
    image =  request.FILES['image']
    pickuplocation =  request.POST.get('pickuplocation')
    slug = book_name.replace(" ", "+") + "+by+" + str(sellername)
    newbook = books.objects.create(sellername=sellername, book_name = book_name, category = category, price= price,image= image,pickuplocation = pickuplocation, slug= slug)
    try:
        newbook.save()
        messages.success(request,'Your post has been added successfully, Thank you for your great effort.')
    except:
        messages.error(request,"Sorry! unable to Process..")
    return redirect('/')

@login_required(login_url='/loginsignup')
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone)
        order.save()
        updateorder = TrackUpdate(order_id=order.order_id,update="Your Order Is Placed")
        updateorder.save()
        thank = True
        id = order.order_id
        return render(request, 'home/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'home/checkout.html')

def TrackOrder(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        updates = TrackUpdate.objects.filter(order_id=order_id)
        context = {'updates':updates}
        return render(request,'home/updatepage.html',context)

    return render(request,'home/trackorder.html')

def search(request):
    searchquery = request.GET['search']
    if len(searchquery)>200:
        allposts = Post.objects.none()
    if len(searchquery)<4:
        allposts = Post.objects.none()
        messages.error(request,'Please enter more than 4 characters')
        redirect('/')
    else:
        allpoststitle = books.objects.filter(book_name__icontains=searchquery)
        allpostscontent = books.objects.filter(category__icontains=searchquery)
        allposts = allpoststitle.union(allpostscontent)
        context = {'allposts':allposts,'search':searchquery}
        return render(request,'home/search.html',context)
    return render(request,'home/search.html')

#def contact(request):
#        if request.method == "POST":
#            form_name=request.POST['from_name']
#            form_lastname=request.POST['from_lastname']
#            form_email=request.POST['from_email']
#        form_phone=request.POST['from_phone']
#        form_message=request.POST['from_message']
#
#        #send an Email
#        send_mail(
#        form_name,#subject
#        form_message,#message
#        form_email,#email from
#        ['gkaur2_be19@thapar.edu'],#email to
#        )
#
#        return render(request, 'home/contact.html', {'form_name':form_name})
#    else:
#        return render(request, 'home/contact.html', {})
def contact(request):
    name=''
    email=''
    comment=''


    form= ContactForm(request.POST or None)
    if form.is_valid():
        name= form.cleaned_data.get("name")
        email= form.cleaned_data.get("email")
        comment=form.cleaned_data.get("comment")


        subject= "A Visitor's Comment"


        comment= name + " with the email, " + email + ", sent the following message:\n\n" + comment;
        send_mail(subject, comment, email , ['gkaur2_be19@thapar.edu'])


        context= {'name': name}

        return render(request, 'home/contact.html', context)

    else:
        context= {'form': form}
        return render(request, 'home/contact.html', context)
