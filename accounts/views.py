from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.urls import reverse_lazy

from django.http import HttpResponseRedirect

from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash

from assets.forms import *


#for vendor countries 
from django.db.models import Count

from django.core.paginator import Paginator

from django.contrib import messages

from assets.forms import *

from assets.models import *

from django.contrib.auth import get_user_model

from django.db.models import Q

from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserChangeForm

from .forms import UserUpdateForm, ClientMessageForm, AssetForm, BroadcastMessageForm

from django.utils import timezone

#from assets.decorators import allowed_users
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
#from assets.decorators import unauthenticated_user, allowed_users, admin_only, super_user
from django.contrib.auth.decorators import login_required







app_name = 'accounts'


@login_required(login_url='login')
def Home(request):
    total_asset = Assets.objects.count()
    total_emp = Employee.objects.count()
    dept   = Assign.objects.count()
    total_vendor = Vendor.objects.count()
    
     #for assets display 

    New_Assets = Assets.objects.filter(Asset_State = 'New')
    Good_Assets = Assets.objects.filter(Asset_State = 'Good')
    Used_Assets = Assets.objects.filter(Asset_State = 'Used')
    Defective_Assets = Assets.objects.filter(Asset_State = 'Defective')

    #Asset Vendors by country 
    # Render some queries here 
    # Get a queryset of all vendors with their associated countries
    vendors = Vendor.objects.values('Country').annotate(total=Count('id'))


    ##Render User Activity ####
    employee = Employee.objects.all() #

    assets_by_employee = Assets.objects.all().order_by('Employee').values('Employee').annotate(asset_count=Count('id'))

    assets_by_employees = Assets.objects.all().prefetch_related('Employee').annotate(asset_count=Count('id')).order_by('Employee__Full_Name')

    employees = Employee.objects.all()
    employee_assets = []
    for employee in employees:
        total_assets = Assets.objects.filter(Employee=employee).count()
        employee_assets.append((employee, total_assets))

    paginator = Paginator(employee_assets, 5)
    page_number = request.GET.get('page')
    employee_assets = paginator.get_page(page_number)   
   
    myquery = {
        "total_asset" : total_asset,
        "total_emp" : total_emp,
        "dept"   : dept,
        "total_vendor": total_vendor,
        'vendors': vendors,

        #for assets display 

        "New_Assets" : New_Assets,
        "Good_Assets" : Good_Assets,
        "Used_Assets" : Used_Assets,
        "Defective_Assets" : Defective_Assets,

        #Asset Vendors by country 

        #EMployee to be rendered 
        "employee" : employee,

        'employee_assets': employee_assets,

        "assets_by_employee":assets_by_employee,

        "assets_by_employees":assets_by_employees,
        
    }
    return render(request, 'admin/index.html', myquery )

def RegAssetType(request):
    
    AssetTypeform = AssetTypesForm()
    if request.method == 'POST':

       AssetTypeform = AssetTypesForm(request.POST)
       if AssetTypeform.is_valid(): 
        AssetTypeform.save()
        messages.success(request, 'Asset type has been successfully added.')
        return redirect('accounts:view_asset_type')

    context = {'AssetTypeform': AssetTypeform }
    return render(request, 'admin/asset/regAssetType.html', context)

def viewAssetType(request):
    query = request.GET.get('e')
   
    if query:
        AssetType = Asset_Type.objects.filter(
            Q(type__icontains=query)
        )
    else:
        AssetType = Asset_Type.objects.all()

    context = { "AssetType" : AssetType, "query": query}
    return render(request, 'admin/asset/viewAssetType.html', context)

def edit_asset_type(request, assettype_id):
    AssetType = get_object_or_404(Asset_Type, id=assettype_id)
    if request.method == 'POST':
        # Process the form data and save the group
        AssetType.type = request.POST['type']
        AssetType.save()
        return HttpResponseRedirect(reverse('accounts:view_asset_type'))

    context = {
        'AssetType': AssetType
    }
    return render(request, 'admin/user/edit_asset_type.html', context)

def delete_asset_type(request, assettype_id):
    AssetType = get_object_or_404(Asset_Type, id=assettype_id)
    if request.method == 'POST':
        # Delete the group
        AssetType.delete()
        messages.danger(request, 'Asset type has been successfully deleted.')
        return HttpResponseRedirect(reverse('accounts:view_asset_type'))

    context = {
        'AssetType': AssetType
    }
    return render(request, 'admin/delete_assetType.html', context)

def RegAssignGroup(request):
    
    AssignGroup = AssignGroupsForm()
    if request.method == 'POST':

       AssignGroup = AssignGroupsForm(request.POST)
       if AssignGroup.is_valid(): 
        AssignGroup.save()
        messages.success(request, 'Assign group has been successfully added.')
        return redirect('accounts:view_assign')

    context = {'AssignGroup': AssignGroup }
    return render(request, 'admin/asset/regAssign.html', context)

def viewAssignType(request):
    query = request.GET.get('e')
   
    if query:
        AssignG = Assign.objects.filter(
            Q(Name__icontains=query)
        )
    else:
        AssignG = Assign.objects.all()

    context = { "AssignG" : AssignG, "query": query}
    return render(request, 'admin/asset/viewAssign.html', context)

def edit_assign(request, assign_id):
    AssignG = get_object_or_404(Assign, id=assign_id)
    if request.method == 'POST':
        # Process the form data and save the group
        AssignG.Name = request.POST['Name']
        AssignG.save()
        return HttpResponseRedirect(reverse('accounts:view_assign'))

    context = {
        'AssignG': AssignG
    }
    return render(request, 'admin/user/edit_assign.html', context)

def delete_assign(request, assign_id):
    AssignG = get_object_or_404(Assign, id=assign_id)
    if request.method == 'POST':
        # Delete the group
        AssignG.delete()
        return HttpResponseRedirect(reverse('accounts:view_assign'))

    context = {
        'AssignG': AssignG
    }
    return render(request, 'admin/delete_assign.html', context)


def viewEmployee(request):
    query = request.GET.get('e')
   
    if query:
        EmployeeData = Employee.objects.filter(
            Q(Full_Name__icontains=query) |
            Q(Address__icontains=query) | 
            Q(Title__icontains=query) 
        )
    else:
        EmployeeData = Employee.objects.all()

    context = { "EmployeeData" : EmployeeData, "query": query}
    return render(request, 'admin/asset/viewEmployee.html', context)

def edit_employee(request, employee_id):
    EmployeeData = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        # Process the form data and save the group
        EmployeeData.Full_Name = request.POST['Full_Name']
        try:
            user = Employee.objects.get(name=request.POST['user'])
            EmployeeData.user = user
        except ObjectDoesNotExist:
            
            pass
        EmployeeData.Title = request.POST['Title']
        try:
            department = Assign.objects.get(name=request.POST['department'])
            EmployeeData.department = department
        except ObjectDoesNotExist:
            
            pass
        EmployeeData.Phone = request.POST['Phone']
        EmployeeData.Address = request.POST['Address']
        EmployeeData.Date_of_Birth = request.POST['Date_of_Birth']
        EmployeeData.Marital_Status = request.POST['Marital_Status']
        
        if request.FILES.get('profile_pic'):
            EmployeeData.profile_pic = request.FILES['profile_pic']
        EmployeeData.save()
        messages.success(request, 'Employee data has been successfully updated.')
        return HttpResponseRedirect(reverse('accounts:view_employee'))

    context = {
        'EmployeeData': EmployeeData,
        'profile_pic': EmployeeData.profile_pic,
        'date_of_birth': EmployeeData.Date_of_Birth,
    }
    return render(request, 'admin/user/edit_employee.html', context)

def delete_employee(request, employee_id):
    EmployeeData = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        # Delete the group
        EmployeeData.delete()
        messages.danger(request, 'Employeehas been deleted.')
        return HttpResponseRedirect(reverse('accounts:view_employee'))

    context = {
        'EmployeeData': EmployeeData
    }
    return render(request, 'admin/delete_employee.html', context)

def viewAssetData(request):
   
    query = request.GET.get('q')
   
    if query:
        asset = Assets.objects.filter(
            Q(id__icontains=query) | 
            Q(Name__icontains=query) |
            Q(Model__icontains=query) |
            Q(Date_Assigned__icontains=query) 
        )
    else:
        asset = Assets.objects.all()

    paginator = Paginator(asset, 10)
    page = request.GET.get('page')
    asset = paginator.get_page(page)

    context = {
        "asset" : asset,
        "query": query
    }
   
    return render(request, 'admin/asset/viewAssets.html', context)

def edit_assetsss(request, asset_id):
    asset = get_object_or_404(Assets, id=asset_id)
    EmployeeData = Employee.objects.all() # get all employees
    AssetType = Asset_Type.objects.all() # get all employees
    
    if request.method == 'POST':
        # Process the form data and save the group

        asset.Name = request.POST['Name']
        type = request.POST.get('type')
        if type:
            try:
                asset.type = Asset_Type.objects.get(type=type)
            except ObjectDoesNotExist:
                
                pass
        asset.Quantity = request.POST['Quantity']
        asset.Model = request.POST['Model']
        asset.Serian_Num = request.POST['Serian_Num']
        state = request.POST.get('Asset_State')
        if state:
            try:
                state = Assets.objects.get(name=state)
                asset.Asset_State = state
            except ObjectDoesNotExist:
                
                pass
        asset.LifeSpan = request.POST['LifeSpan']
        if 'Date_Acquired' in request.POST:
            asset.Date_Acquired = request.POST['Date_Acquired']
        if 'Warantee_Start_Date' in request.POST:
            asset.Warantee_Start_Date = request.POST['Warantee_Start_Date']
        if 'Warantee_End_Date' in request.POST:
            asset.Warantee_End_Date = request.POST['Warantee_End_Date']
        try:
            employee = Employee.objects.get(Full_Name=request.POST['employee'])
            asset.employee = employee
        except ObjectDoesNotExist:
            
            pass
        if 'Date_Assigned' in request.POST:
            asset.Date_Assigned = request.POST.get('Date_Assigned')

        asset.Location = request.POST['Location']
        if 'Vendor' in request.POST:
            vendor_name = request.POST['Vendor']
        try:
            vendor = Vendor.objects.get(Company_Name=vendor_name)
            asset.Vendor = vendor
        except Vendor.DoesNotExist:
            # handle the case where the vendor doesn't exist
            pass
        asset.Description = request.POST['Description']
        
        asset.save()
        messages.success(request, 'An asset has been successfully updated.')
        return HttpResponseRedirect(reverse('accounts:view_assets'))

    context = {
        'asset': asset,
        'Date_Acquired':asset.Date_Acquired,
        'Warantee_Start_Date':asset.Warantee_Start_Date,
        'Warantee_End_Date':asset.Warantee_End_Date,
        'Date_Assigned':asset.Date_Assigned,
        'EmployeeData': EmployeeData,
        'AssetType':AssetType,
    }
    return render(request, 'admin/user/edit_asset.html', context)

def edit_asset(request, pk):

    asset = get_object_or_404(Assets, pk=pk)

    form = AssetForm(instance=asset)
    
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save()
            messages.success(request, f'Asset {asset.Name} was updated successfully')
            return redirect('accounts:view_assets')
        
    return render(request, 'admin/user/asset_form.html', {'form': form, 'title':'Update Asset', 'method':'PUT'})

def delete_asset(request, asset_id):
    asset = get_object_or_404(Assets, id=asset_id)
    if request.method == 'POST':
        # Delete the group
        asset.delete()
        messages.success(request, 'An asset has been deleted, successfully .')
        return HttpResponseRedirect(reverse('accounts:view_assets'))

    context = {
        'asset': asset
    }
    return render(request, 'admin/delete_asset.html', context)

def viewVendorsData(request):
    query = request.GET.get('q')
   
    if query:
        vendor = Vendor.objects.filter(
            Q(Company_Name__icontains=query) | 
            Q(Email__icontains=query) |
            Q(Country__icontains=query)
        )
    else:
        vendor = Vendor.objects.all()
    
    paginator = Paginator(vendor, 10)
    page = request.GET.get('page')
    vendor = paginator.get_page(page)
    

    context = {
        "vendor" : vendor,
        "query": query
    }
   
    return render(request, 'admin/asset/viewVendors.html', context)

def RegEmployee(request):
    
    Employeeform = EmployeeForm()
    if request.method == 'POST':

       Employeeform = EmployeeForm(request.POST)
       if Employeeform.is_valid(): 
        Employeeform.save()
        messages.success(request, 'Employee has been successfully added.')
        return redirect('accounts:view_employee')

    context = {'Employeeform': Employeeform }
    return render(request, 'admin/asset/regEmployee.html', context)

def list_users(request):
    query = request.GET.get('q')
   
    if query:
        users = User.objects.filter(
            Q(email__icontains=query) | 
            Q(username__icontains=query) |
            Q(is_active__icontains=query)
        )
    else:
        users = User.objects.all()
    context = {'users': users, "query": query}
    return render(request, 'admin/user/viewUser.html', context)

def add_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            request.POST['username'],
            request.POST['email'],
            request.POST['password'],
        )
        # get the group object based on the group name in the form
        group_name = request.POST['group']
        group = Group.objects.get(name=group_name)
        # assign user to the group
        group.user_set.add(user)
        return redirect('accounts:view_users')
    # get all available groups
    groups = Group.objects.all()
    return render(request, 'admin/user/addUser.html', {'groups': groups})

def create_group(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        new_group = Group(name=group_name)
        new_group.save()
        return redirect('accounts:view_group') # redirect to the list of groups
    else:
        return render(request, 'admin/user/create_group.html')

def viewGroups(request):
    
    groups = Group.objects.all()
    context = { 'groups': groups}
    return render(request, 'admin/user/viewGroup.html', context)

def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        # Process the form data and save the group
        group.name = request.POST['name']
        group.save()
        return HttpResponseRedirect(reverse('accounts:view_group'))

    context = {
        'group': group
    }
    return render(request, 'admin/user/edit_group.html', context)

def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        # Delete the group
        group.delete()
        return HttpResponseRedirect(reverse('accounts:view_group'))

    context = {
        'group': group
    }
    return render(request, 'admin/delete_group.html', context)

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = UserUpdateForm(instance=user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:view_users')
    return render(request, 'admin/user/edit_user.html', {'form': form})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('accounts:view_users')
    return render(request, 'admin/user/deleteUser.html', {'user': user})

def UserProfile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('accounts: UserProfile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'admin/user/userProfile.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

def admin_message_list(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-sent_at')

    
    return render(request, 'admin/message/message_list.html', {'messages_received': messages_received})

def user_message_detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    if not message.read_at:
        message.read_at = timezone.now()
        message.save()
    return render(request, 'admin/message/message_detail.html', {'message': message})

def message_reply(request, message_id):
    original_message = get_object_or_404(Message, pk=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = original_message.sender
            message.subject = f'Re: {original_message.subject}'
            message.body = form.cleaned_data['body']
            message.save()
            messages.success(request, 'Your reply was sent successfully.')
            return redirect('accounts:message_list')
    else:
        form = MessageForm(initial={'receiver': original_message.sender, 'subject': f'Re: {original_message.subject}'})
    return render(request, 'admin/message/message_reply.html', {'form': form, 'message': original_message})

def compose_message(request, receiver_id=None):
    if receiver_id:
        receiver = get_object_or_404(User, pk=receiver_id)
        subject = f'Re: {request.GET.get("subject")}' if request.GET.get("subject") else ''
    else:
        receiver = None
        subject = ''
    if request.method == 'POST':
        form = ClientMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            #message.receiver = form.cleaned_data['receiver']
            message.subject = form.cleaned_data['subject']
            message.body = form.cleaned_data['body']
            message.save()
            # If a receiver is selected, send an individual message
            message.receiver.set([form.cleaned_data['receiver']])
 
            messages.success(request, 'Your message was sent successfully.')
            return redirect('accounts:sent_message', user_id=request.user.id)
    else:
        form = ClientMessageForm(initial={'receiver': receiver, 'subject': subject})
    return render(request, 'admin/message/compose_message.html', {'form': form})

def sent_message_list(request, user_id):
    messages_sent = Message.objects.filter(sender=user_id).order_by('-sent_at')
    messages.success(request, 'Message has been sent to the recepient')
    return render(request, 'admin/message/sent_message.html', {'messages_sent': messages_sent})

def broadcast_message(request):
    if request.method == 'POST':
        form = BroadcastMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, 'Broadcast message sent successfully.')
            return redirect('accounts:sent_broadcast_message', user_id=request.user.id)
    else:
        form = BroadcastMessageForm()
    return render(request, 'admin/message/broadcast_message.html', {'form': form})

def sent_broadcast_message(request, user_id):
    broadcast_message_sent = BroadcastMessage.objects.filter(sender=user_id).order_by('-timestamp')
    messages.success(request, 'Broadcast Message has been delivered')
    return render(request, 'admin/message/broadcast_message_list.html', {'broadcast_message_sent': broadcast_message_sent})

def broadcast_message_detail(request, message_id):
    broadcast_message = get_object_or_404(BroadcastMessage, pk=message_id)

    return render(request, 'admin/message/broadcast_message_detail.html', {'broadcast_message': broadcast_message})

#Show the date and time of a record 
def showdate(request):
    datetime.datetime.now()
    return render(request, 'home.html')


#employee report 
def employeeReport(request):
    employee_list = Employee.objects.all()
    return render(request, 'admin/report/employeereport.html', {'employee_list': employee_list})

#vendor report 
def vendorReport(request):
    vendor_list = Vendor.objects.all()
    return render(request, 'admin/report/vendorreport.html', {'vendor_list': vendor_list})

#asset report 
def assetReport(request):
    asset_list = Assets.objects.all()
    return render(request, 'admin/report/assetreport.html', {'asset_list': asset_list})


def unread_message_count(request):
    count = Message.objects.filter(receiver=request.user, read_at__isnull=True).count()
    return JsonResponse({'count': count})