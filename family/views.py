from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import never_cache

from family.models import FamilyMembers, Expenses


@login_required
@never_cache
def add_family(request):
    return render(request, 'add_family.html')


@login_required
@never_cache
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
@login_required
@never_cache
def seefamily(request):
    family_member = FamilyMembers.objects.all()
    return render(request,'seefamily.html',{'data':family_member})

@login_required
@never_cache
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
@never_cache
def delete_family_mem(request, id):
    family_mem = get_object_or_404(FamilyMembers, id=id, familyLead=request.user)
    family_mem.delete()
    messages.success(request, 'Member deleted successfully!')
    return redirect('seefamily')


@login_required
@never_cache
def add_expenses(request):
    redirect_data = FamilyMembers.objects.filter(familyLead=request.user)

    if request.method == 'POST':
        try:
            # Get the family member by firstname, filtered by current user
            family_mem = FamilyMembers.objects.get(
                firstname=request.POST.get('name'),
                familyLead=request.user  # 🔥 Security: Filter by user
            )

            exp = Expenses()
            exp.familyLead = request.user
            exp.name = family_mem
            exp.purpose = request.POST.get('purpose')
            exp.expense = float(request.POST.get('expense'))

            date_from_user = request.POST.get('date')
            exp.date = datetime.strptime(date_from_user, '%Y-%m-%d')
            exp.save()

            messages.success(request, 'Expense added successfully! ✅')  # 🔥 Add message
            return redirect('addexpense')  # 🔥 Redirect instead of render

        except FamilyMembers.DoesNotExist:
            messages.error(request, 'Family member not found!')
            return render(request, 'add_expense.html', {'data': redirect_data})
        except ValueError:
            messages.error(request, 'Invalid date or expense amount!')
            return render(request, 'add_expense.html', {'data': redirect_data})

    return render(request, 'add_expense.html', {'data': redirect_data})


@login_required
@never_cache
def view_expenses(request):
    # Fetch all expenses for the current user only
    expenses = Expenses.objects.filter(familyLead=request.user).order_by('-date')

    # Calculate total expenses
    total_expense = sum(exp.expense for exp in expenses)

    context = {
        'expenses': expenses,
        'total_expense': total_expense
    }
    return render(request, 'view_expense.html', context)

@login_required
@never_cache
def update_expense(request, id):
    expense = get_object_or_404(Expenses, id=id, familyLead=request.user)
    if request.method == 'POST':
        expense.purpose = request.POST['purpose']
        expense.expense = float(request.POST['expense'])
        date_from_user = request.POST.get('date')
        expense.date = datetime.strptime(date_from_user, '%Y-%m-%d')
        expense.save()
        messages.success(request, 'Expense updated successfully!')
        return redirect('viewexpense')
    return render(request, 'update_expense.html', {'data': expense})

@login_required
@never_cache
def delete_expense(request,id):
    expense = get_object_or_404(Expenses, id=id, familyLead=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')

    return redirect('viewexpense')


@login_required
@never_cache
def monthly_report(request):
    from django.utils import timezone
    now = timezone.now()

    # Default to current month/year
    selected_year = now.year
    selected_month = now.month

    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))
        selected_month = int(request.POST.get('month'))

    expenses = Expenses.objects.filter(
        familyLead=request.user,
        date__year=selected_year,
        date__month=selected_month
    ).order_by('-date')

    total_expense = sum(exp.expense for exp in expenses)

    # Form data
    years = range(2020, now.year + 1)
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'report_type': 'Monthly',
        'start_year': selected_year,
        'years': years,
        'start_month': selected_month,
        'months': months,
        'records': expenses,  # For template compatibility
        'norecords': 'No records found' if not expenses else ''
    }
    return render(request, 'monthly_report.html', context)


@login_required
@never_cache
def yearly_report(request):
    from django.utils import timezone
    now = timezone.now()

    # Default to current year
    selected_year = now.year

    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))

    expenses = Expenses.objects.filter(
        familyLead=request.user,
        date__year=selected_year
    ).order_by('-date')

    total_expense = sum(exp.expense for exp in expenses)

    # Form data
    years = range(2020, now.year + 1)

    context = {
        'expenses': expenses,
        'total_expense': total_expense,
        'report_type': 'Yearly',
        'start_year': selected_year,
        'years': years,
        'records': expenses,  # For template compatibility
        'norecords': 'No records found' if not expenses else ''
    }
    return render(request, 'yearly_report.html', context)


@login_required
@never_cache
def total_expense(request):
    from django.utils import timezone
    now = timezone.now()

    # Default to current month/year
    selected_year = now.year
    selected_month = now.month

    if request.method == 'POST':
        selected_year = int(request.POST.get('year'))
        selected_month = int(request.POST.get('month'))

    # Filter expenses for selected month/year
    expenses = Expenses.objects.filter(
        familyLead=request.user,
        date__year=selected_year,
        date__month=selected_month
    ).order_by('-date')

    # Calculate monthly total
    total_expense = sum(exp.expense for exp in expenses)

    # Calculate yearly total for the selected year
    yearly_expenses = Expenses.objects.filter(
        familyLead=request.user,
        date__year=selected_year
    )
    year_total = sum(exp.expense for exp in yearly_expenses)

    # Form data
    years = range(2020, now.year + 1)
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    dict1 = {
        'expenses': expenses,
        'total_expense': total_expense,
        'year_total': year_total,
        'years': years,
        'months': months,
        'start_year': selected_year,
        'start_month': selected_month,
        'records': expenses,  # For template compatibility
        'norecords': 'No records found' if not expenses else ''
    }

    return render(request, 'total_expense.html', dict1)
