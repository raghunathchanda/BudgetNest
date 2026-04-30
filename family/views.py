from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from family.models import FamilyMembers


# Create your views here.
def add_family(request):
    return render(request, 'add_family.html')

from django.contrib import messages
from django.shortcuts import render, redirect

def adding_member(request):
    income = request.POST.get('income')

    if income == '':
        context = {
            'null': True
        }
        return render(request, 'add_member.html', context)

    income = float(income)

    family_mem = FamilyMembers()
    family_mem.firstname = request.POST.get('firstname')
    family_mem.age = request.POST.get('age')
    family_mem.income = income
    family_mem.familyLead = request.user
    family_mem.save()

    messages.success(request, 'Family Member Added ✅')

    # 🔥 IMPORTANT CHANGE
    return redirect('addfamily')   # not render

def seefamily(request):
    family_member = FamilyMembers.objects.all()
    return render(request,'seefamily.html',{'data':family_member})

def update_family_mem(request,id):
    family_mem = FamilyMembers.objects.get(id=id)
    if request.method == 'POST':
        family_mem.firstname = request.POST['firstname']
        family_mem.age = request.POST['age']
        family_mem.income = float(request.POST['income'])
        family_mem.save()
        get_all_data = FamilyMembers.objects.all()
        return render(request,'seefamily.html',{'data':get_all_data})

    return render(request,'update_family.html',{'data':family_mem})



@login_required
def delete_family_mem(request, id):
    family_mem = get_object_or_404(FamilyMembers, id=id, familyLead=request.user)
    family_mem.delete()
    messages.success(request, 'Member deleted successfully!')
    return redirect('seefamily')