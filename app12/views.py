from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegisterForm,LoginForm,UpdateForm,ChangePasswordForm,ImageForm
from .models import Image
from django.contrib.auth import logout as logouts


def hello(request):
    return HttpResponse("django")
    
def index(request):
    name="fimis."
    return render(request,'index.html',{'data':name})

def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['Name']
            age=form.cleaned_data['Age']
            place=form.cleaned_data['Place']
            email=form.cleaned_data['Email']
            password=form.cleaned_data['Password']
            confirmpassword=form.cleaned_data['ConfirmPassword']

            user=Image.objects.filter(Email=email).exists()
            if user:
                messages.warning(request,'email already exists')
                return redirect('/register')
            elif password!=confirmpassword:
                messages.warning(request,'password mismatch')
                return redirect('/register')
            else:
                tab=Image(Name=name,Age=age,Place=place,Email=email,Password=password)
                tab.save()
                messages.success(request,'datasaved')
                return redirect('/')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})


#for login 

def login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['Email']
            password=form.cleaned_data['Password']
            try:
                user=Image.objects.get(Email=email)
                if not user:
                    messages.warning(request,'email does not exists')
                    return redirect('/login')
                elif password!=user.Password:
                    messages.warning(request,'password incorrect')
                    return redirect('/login')
                else:
                    messages.success(request,'login success')
                    return redirect('/home/%s' % user.id)
            except:
                    messages.warning(request,'email or password incorrect')
                    return redirect('/login')
         
    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})
def home(request,id):
    user=Image.objects.get(id=id)
    return render(request,'home.html',{'user':user})

def showusers(request):
    users=Image.objects.all()
    return render(request,'showusers.html',{'users':users})

def update(request,id):
    user=Image.objects.get(id=id)
    if request.method=='POST':
        form=UpdateForm(request.POST or None,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,'update success')
            return redirect('/home')
    else:
        form=UpdateForm(instance=user)
    return render(request,'update.html',{'form':form,'user':user})
def delete(request,id):
    user=Image.objects.get(id=id)
    user.delete()
    messages.success(request,'delete success')
    return redirect('/home')


def changepassword(request,id):
    user=Image.objects.get(id=id)
    if request.method=='POST':
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            old=form.cleaned_data['OldPassword']
            new=form.cleaned_data['NewPassword']
            confirm=form.cleaned_data['ConfirmPassword']

            if old!=user.Password:
                messages.warning(request,'password incorrect')
                return redirect('/changepassword/%s' % user.id)
            elif old==new:
                messages.warning(request,'passwords are same')
                return redirect('/changepassword/%s' % user.id)
            elif new!=confirm:
                messages.warning(request,'password mismatch')
                return redirect('/changepassword/%s' % user.id)
            else:
                user.Password=new
                user.save()
                messages.success(request,'password changed')
                return redirect('/home/%s' % user.id) 
        
    else:
        form=ChangePasswordForm()
            
    return render(request,'changepassword.html',{'form':form,'user':user})

def logout(request):
    logouts(request)
    messages.success(request,'logged out successfully')
    return redirect('/')

#imageform
def image(request):
    if request.method=='POST':
        form=ImageForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            name=form.cleaned_data['Name']
            age=form.cleaned_data['Age']
            place=form.cleaned_data['Place']
            photo=form.cleaned_data['Photo']
            email=form.cleaned_data['Email']
            password=form.cleaned_data['Password']
            confirmpassword=form.cleaned_data['ConfirmPassword']

            user=Image.objects.filter(Email=email).exists()
            if user:
                messages.warning(request,'email already exists')
                return redirect('/image')
            elif password!=confirmpassword:
                messages.warning(request,'password mismatch')
                return redirect('/image')
            else:
                tab=Image(Name=name,Age=age,Place=place,Photo=photo,Email=email,Password=password)
                tab.save()
                messages.success(request,'datasaved')
                return redirect('/')
    else:
        form=ImageForm()
    return render(request,'image.html',{'form':form})


def showimages(request):
    users=Image.objects.all()
    return render(request,'showimages.html',{'users':users})

def picture(request,id):
    users=Image.objects.get(id=id)

    return render(request,'picture.html',{'users':users})

