from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_control
# Create your views here.

@never_cache
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html') 

def contact(request):
    return render(request,'contact.html') 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def handlelogin(request):
    if request.method=="POST":
        uname=request.POST.get("username")
        pass1=request.POST.get("pass1")
        myuser=authenticate(username=uname,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')
        else:
            messages.success(request,"Invalid username or password")
            return redirect('/login')
    return render(request,'login.html') 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def handlesignup(request):
    if request.method=="POST":
        uname=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")
        confirmpassword=request.POST.get("pass2")
        if ' ' in uname:
            messages.warning(request, "Username cannot contain spaces")
            return redirect('/signup')

        if password != confirmpassword:
            messages.warning(request,"Password is incorrect")
            return redirect('/signup')
        try:
            if User.objects.get(username=uname):
                messages.info(request,"Username already exists")
                return redirect('/signup')
        except:
            pass
        try:
            if User.objects.get(email=email):
                messages.info(request,"Email already exists")
                return redirect('/signup')
        except:
            pass
        myuser=User.objects.create_user(uname,email,password)
        myuser.save()
        messages.success(request,"SignUp sucessfull.Please login!!")
        return redirect('/login')
    return render(request,'signup.html') 

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def handlelogout(request):
    logout(request)
    messages.info(request,"Logout success")
    return redirect('/') 


@never_cache
def handleadminlogin(request):
    if request.user.is_superuser:
        return redirect('/adminview')
    if request.method == "POST":
        uname = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        myuser = authenticate(username=uname, password=pass1)
        if myuser is not None and myuser.is_superuser:
            login(request, myuser)
            request.session['admin_logged_in'] = True
            return redirect('/adminview')
        else:
            messages.success(request, "Invalid username or password")
            return redirect('/adminlogin')
    
    return render(request, 'adminlogin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def handleadminlogout(request):
    if request.session.get('admin_logged_in'):
        del request.session['admin_logged_in'] 
    logout(request)
    messages.info(request,"Logout success")
    return redirect('/adminlogin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def insertdata(request):
    if not request.session.get('admin_logged_in'):
        return redirect('/adminlogin')
    if request.method=="POST":
        uname=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")
        confirmpassword=request.POST.get("pass2")
        if ' ' in uname:
            messages.warning(request, "Username cannot contain spaces")
            return redirect('/adminview')
        if password != confirmpassword:
            messages.warning(request,"Password is incorrect")
            return redirect('/adminview')
        try:
            if User.objects.get(username=uname):
                messages.info(request,"Username already exists")
                return redirect('/adminview')
        except:
            pass
        try:
            if User.objects.get(email=email):
                messages.info(request,"Email already exists")
                return redirect('/adminview')
        except:
            pass

        myuser=User.objects.create_user(uname,email,password)
        myuser.save()
        messages.success(request,"User added successfully")
        return redirect('/adminview')
    return render(request,"adminview.html",)

@never_cache
def handleadminview(request):
    if not request.session.get('admin_logged_in'):
        return redirect('/adminlogin')
    search_query = request.GET.get('search')
    
    if search_query:
        data = User.objects.filter(username__icontains=search_query).order_by('id')
    else:
        data = User.objects.all().order_by('id')
    context = {'data': data }
    return render(request,'adminview.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updatedata(request,id):
    if not request.session.get('admin_logged_in'):
        return redirect('/adminlogin')
    if request.method=="POST":
        uname=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("pass1")

        edit=User.objects.get(id=id)
        edit.username=uname
        edit.email=email
        
        edit.save()
        messages.warning(request,"User updated successfully")
        return redirect('/adminview')

    d=User.objects.get(id=id)
    context = {'d': d }
    return render(request,'adminedit.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deletedata(request,id):
    if request.method == "POST":
        d = User.objects.get(id=id)
        d.delete()
        messages.warning(request, "User deleted successfully")
        return redirect("/adminview")

def deleteconfirm(request,id):
    try:
        d = User.objects.get(id=id)
        context = {'d': d}
        return render(request, 'deleteconfirm.html', context)
    except User.DoesNotExist:
        messages.error(request, "User does not exist")
        return redirect("/adminview")
    return render(request,'deleteconfirm.html')

