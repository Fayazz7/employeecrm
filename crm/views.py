from django.shortcuts import render,redirect
from django.views.generic import View,ListView
from crm.forms import EmployeeForm,EmployeeModelForm,RegistrationForm,LoginForm
from crm.models import Employees
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
# Create your views here.

# Decorators Start
def signin_required(fn):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"please login")
            return redirect("sign-in")
        else:
            return fn(request,*args, **kwargs)
    return wrapper
        
# Decarators End

class IndexView(View):
    def get(self,request,*args, **kwargs):
        return render(request,"index.html")
    

@method_decorator(signin_required,name="dispatch")
class EmployeeCreateView(View):
    def get(self,request,*args, **kwargs):
        form=EmployeeModelForm()
        return render (request,"emp_add.html",{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=EmployeeModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Employee Created Succesfully")
            # Employees.objects.create(**form.cleaned_data)
            print(form.cleaned_data)
            return render (request,"emp_add.html",{"form":form})
        else:
            messages.error(request,"Faild to add employee")
            return render (request,"emp_add.html",{"form":form})
        
@method_decorator(signin_required,name="dispatch")
class EmployeeListView(View):
    def get(self,request,*args, **kwargs):
        if request.user.is_authenticated:
            form=Employees.objects.all()
            departments=Employees.objects.all().values_list("department",flat=True).distinct()
            print(departments)
            if 'department' in request.GET:
                dept=request.GET.get("department")
                form=form.filter(department__iexact=dept)
            return render(request,"emp_all.html",{"datas":form,"departments":departments})
        else:
            messages.error(request,"Session Failed")
            return redirect ("sign-in")
    def post(self,request,*args, **kwargs):
        name=request.POST.get("box")
        form=Employees.objects.filter(name__icontains=name)
        return render (request,"emp_all.html",{"datas":form})
        # model=Employees
        # template_name="emp_all.html"
        # context_object_name="datas"

    

@method_decorator(signin_required,name="dispatch")
class EmployeeUpdateView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(instance=obj)
        return render (request,"emp_update.html",{"form":form})
    
    def post (self,request,*args, **kwargs):
        id=kwargs.get("pk")
        obj=Employees.objects.get(id=id)
        form=EmployeeModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect ("emp-detail",pk=id)
        else:
            return render (request,"emp_update.html",{"form":form})
            
        
        
@method_decorator(signin_required,name="dispatch")
class EmployeeDetalView(View):
    def get (self,request,*args, **kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render (request,"emp_detail.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")
class EmployeeDeleteView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        messages.success(request,"Succesfully Deleted")
        return redirect ("emp-list")
    
class SignUpView(View):
    def get (self,request,*args, **kwargs):
        form=RegistrationForm()
        return render (request,"registration.html",{"form":form})
    def post(self,request,*args, **kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
            User.objects.create_user(**form.cleaned_data)
            # print("saved")
            messages.success(request,"created")
            return redirect("sign-in")
        else:
            messages.error(request,"failed")
            # print("invalid")
            return render (request,"registration.html",{"form":form})
        
class SignInView(View):
    def get (self,request,*args, **kwargs):
        form=LoginForm()
        return render (request,"login.html",{"form":form})
    def post(self,request,*args, **kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            u_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(u_name,pwd)
            usr_obj=authenticate(request,username=u_name,password=pwd)
            if usr_obj:
                print("valid creditial")
                login(request,usr_obj)
                return redirect("emp-list")
            else:
                print("invalid credintial")
                return redirect ("sign-up")
        else:
            print("invalid")
            return render (request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")      
class SignOutView(View):
    def get(self,request,*args, **kwargs):
        logout(request)
        return redirect ("sign-in")
