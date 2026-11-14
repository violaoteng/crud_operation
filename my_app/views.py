from django.shortcuts import render,redirect
from .models import User
from .forms import UserForm
# Create your views here.

def user_list(request):
    records = list(User.objects.all().order_by('name'))
    birth_year_groups = {}
    for record in records:
        decade = (record.date_of_birth.year // 10) * 10
        birth_year_groups[decade] = birth_year_groups.get(decade, 0) + 1

    largest_group = max(birth_year_groups.values(), default=0)
    birth_year_chart = [
        {
            'label': '{}s'.format(decade),
            'count': count,
            'width': round(count / largest_group * 100) if largest_group else 0,
        }
        for decade, count in sorted(birth_year_groups.items())
    ]
    context = {
        'records': records,
        'total_users': len(records),
        'birth_year_group_count': len(birth_year_groups),
        'mobile_count': sum(bool(record.mobile_number) for record in records),
        'birth_year_chart': birth_year_chart,
    }
    return render(request, 'Listingpage.html', context=context)

def AddUser(request):
    mydict={}
    form=UserForm(request.POST or None , request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('/')

    mydict['form']=form
    return render(request,'Add.html',mydict)

def EditUser(request,id=None):
    one_rec=User.objects.get(pk=id)
    form=UserForm(request.POST or None,request.FILES or None, instance=one_rec)
    if form.is_valid():
        form.save()
        return redirect('/')
    mydict= {'form':form}
    return render(request,'Edit.html',context=mydict)

def DeleteUser(request,eid=None):
    one_rec = User.objects.get(pk=eid)
    if  request.method=="POST":
         one_rec.delete()
         return redirect('/')
    return render(request,'Delete.html')

def ViewUser(request,eid=None):
    mydict={}
    one_rec = User.objects.get(pk=eid)
    mydict['user']=one_rec
    return render(request,'''View.html''',mydict)