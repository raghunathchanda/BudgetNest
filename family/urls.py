from django.urls import path

from family import views

urlpatterns = [
    path('addfamily/',views.add_family,name='addfamily'),
    path('addingmember/',views.adding_member,name='addingmember'),
    path('seefamily', views.seefamily, name='seefamily'),  # display family member details
    path('updatefamily/<int:id>', views.update_family_mem, name='updatefamily'),
    path('deletefamily/<int:id>', views.delete_family_mem, name='deletefamily'),
]