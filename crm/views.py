from django.shortcuts import render,redirect
from django.views.generic import View,ListView
from crm.forms import EmployeeForm,EmployeeModelForm
from crm.models import Employees
# Create your views here.

class IndexView(View):
    def get(self,request,*args, **kwargs):
        return render(request,"index.html")
    


class EmployeeCreateView(View):
    def get(self,request,*args, **kwargs):
        form=EmployeeModelForm()
        return render (request,"emp_add.html",{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=EmployeeModelForm(request.POST)
        if form.is_valid():
            form.save()
            # Employees.objects.create(**form.cleaned_data)
            print(form.cleaned_data)
            return render (request,"emp_add.html",{"form":form})
        else:
            return render (request,"emp_add.html",{"form":form})
        
class EmployeeListView(ListView):
    model=Employees
    template_name="emp_all.html"
    context_object_name="datas"
    # def get(self,request,*args, **kwargs):
    #     form=Employees.objects.all()
    #     return render(request,"emp_all.html",{"datas":form})
    


class EmployeeUpdateView(View):
    def get(self,request,*args, **kwargs):
        
        return render (request,"emp_update.html")
    
class EmployeeDetalView(View):
    def get (self,request,*args, **kwargs):
        id=kwargs.get("pk")
        qs=Employees.objects.get(id=id)
        return render (request,"emp_detail.html",{"data":qs})
    
class EmployeeDeleteView(View):
    def get(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        Employees.objects.get(id=id).delete()
        return redirect ("emp-list")
        
    

        


