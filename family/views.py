from django.http import HttpResponse
from django.shortcuts import render

from family.models import FamilyMembers


# Create your views here.
def add_family(request):
    return render(request, 'add_family.html')

def adding_member(request):
    income = request.POST['income']
    if income == '':
        context = {
            'null': True
        }
        return render(request, 'add_member.html', context)
    else:
        income = float(income)

    family_mem = FamilyMembers()
    family_mem.firstname = request.POST['firstname']
    family_mem.lastname = request.POST['lastname']
    family_mem.income = income
    family_mem.familyLead = request.user
    family_mem.save()
    return render(request, 'add_family.html')

def seefamily(request):
    family_member = FamilyMembers.objects.all()
    return render(request,'seefamily.html',{'data':family_member})