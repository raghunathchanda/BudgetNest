from django.urls import path

from family import views

urlpatterns = [
    path('addfamily/',views.add_family,name='addfamily'),
    path('addingmember/',views.adding_member,name='addingmember'),
    path('seefamily/', views.seefamily, name='seefamily'),  # display family member details
    path('updatefamily/<int:id>', views.update_family_mem, name='updatefamily'),
    path('deletefamily/<int:id>', views.delete_family_mem, name='deletefamily'),
    path('addexpense/', views.add_expenses, name='addexpense'),
    path('viewexpense/', views.view_expenses, name='viewexpense'),
    path('updateexpense/<int:id>', views.update_expense, name='updateexpense'),
    path('deleteexpense/<int:id>', views.delete_expense, name='deleteexpense'),
    path('monthlyreport/', views.monthly_report, name='monthlyreport'),
    path('yearlyreport/', views.yearly_report, name='yearlyreport'),
    path('totalexpense/', views.total_expense, name='totalexpense'),


]