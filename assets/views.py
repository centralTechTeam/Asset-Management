from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, Http404

from assets.models import *

#from accounts.models import User
from .forms import AssetForm, VendorForm, UserForm, SuperUserForm, MessageForm
#from django.db.models import F

from django.views.generic.edit import FormView

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from .decorators import authenticate_user

# for date and time 
from datetime import datetime

#for vendor countries 
from django.db.models import Count

#filters
from .filters import AssetFilter, AssetFilter_User
from django.core.paginator import Paginator, EmptyPage

from django.db.models import Q
from django.utils import timezone

from django.http import JsonResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.models import Group





def index(request):
	context = {}
	return render(request, 'app/index.html', context)


@login_required(login_url='login')
def test(request):
    return render(request, 'admin/base.html' )



@login_required(login_url='login')
def RegAsset(request):
    Assetform = AssetForm()
    if request.method == 'POST':
      #print('Done POSTED:', request.POST)
       Assetform = AssetForm(request.POST)
       if Assetform.is_valid(): 
        Assetform.save()
        messages.success(request, 'Asset has been successfully added.')
        return redirect('viewasset')
    
    context = {'Assetform': Assetform }
    return render(request, 'regAsset.html', context)

@login_required(login_url='login')
def RegVendor(request):
    Vendorform = VendorForm()
    if request.method == 'POST':
      #print('Done POSTED:', request.POST)
       Vendorform = VendorForm(request.POST)
       if Vendorform.is_valid(): 
        Vendorform.save()
        messages.success(request, 'Vendor has been successfully added.')
        return redirect('view_vendor')

    
    context = {'Vendorform': Vendorform }
    return render(request, 'regVendor.html', context)

@login_required(login_url='login')
def viewAsset(request):
   
    query = request.GET.get('d')
   
    if query:
        assets = Assets.objects.filter(
            Q(id__icontains=query) | 
            Q(Name__icontains=query) |
            Q(Model__icontains=query) |
            Q(Departments__icontains=query) |
            Q(Asset_State__icontains=query) |
            Q(Location__icontains=query) |
            Q(Date_Assigned__icontains=query) 
        )
    else:
        
        if request.user.groups.filter(name__in=['super_admin', 'admin']).exists():
            assets = Assets.objects.all()
        elif request.user.groups.filter(name__in=['users']):
            assets = Assets.objects.filter(Employee=request.user.emp_user).all()

            #assets = Assets.objects.all().prefetch_related('Employee').annotate(asset_count=Count('id')).order_by('Employee__Full_Name')
  

        paginator = Paginator(assets, 10)
        page = request.GET.get('page')
        assets = paginator.get_page(page)

        context = {
            "assets" : assets,
            "query": query
        }
    
    return render(request, 'viewAsset.html', context)

@login_required(login_url='login')
def viewVendors(request):
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
   
    return render(request, 'viewVendor.html', context)

@login_required(login_url='login')
#@allowed_users(allowed_roles=['users'])
def UserSetting(request):
    employee = request.user.employee
    form = UserForm(instance=employee)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile has successfully updated.')
            
    context = {'form':form}
    return render(request, 'userSetting.html', context)

@login_required
def message_list(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-sent_at')
    messages_sent = Message.objects.filter(sender=request.user).order_by('-sent_at')
    return render(request, 'messages/message_list.html', {'messages_received': messages_received, 'messages_sent': messages_sent})

@login_required
def message_compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            admin_group = Group.objects.get(name='admin')
            message.save()
            message.receiver.add(*admin_group.user_set.all())
            message.subject = form.cleaned_data['subject']
            message.body = form.cleaned_data['body']
            message.save()
            
            messages.success(request, 'Your message was sent successfully.')
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'messages/compose_message.html', {'form': form})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id, receiver=request.user)
    if not message.read_at:
        message.read_at = timezone.now()
        message.save()
    return render(request, 'messages/message_detail.html', {'message': message})

@login_required
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
            return redirect('message_list')
    else:
        form = MessageForm(initial={'receiver': original_message.sender, 'subject': f'Re: {original_message.subject}'})
    return render(request, 'messages/reply_message.html', {'form': form})

@login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-sent_at', 'sender')
    unique_senders = []
    for message in messages_received:
        if message.sender not in unique_senders:
            unique_senders.append(message.sender)

     # get the message ID from the URL parameter
    message_id = request.GET.get('message_id')
    
    # if message ID is not provided, render the inbox page
    if not message_id:
        return render(request, 'messages/inbox.html', {'messages_received': messages_received})

    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        raise Http404

    # check if the user is the receiver of the message
    if message.receiver != request.user:
        raise Http404

    # update the message as read
    message.read_at = timezone.now()
    message.save()
    return render(request, 'messages/inbox.html', {'messages_received': messages_received})

def Broadcast_inbox(request):
    broadcast_messages = BroadcastMessage.objects.all().order_by('-timestamp')
    return render(request, 'messages/broadcast_message.html', {'broadcast_messages':broadcast_messages})

@login_required
def unread_message_count(request):
    count = Message.objects.filter(receiver=request.user, read_at__isnull=True).count()
    return JsonResponse({'count': count})

























@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='login')
@never_cache

def home(request):

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

    asset = request.user.emp_user.assets_set.all()

    assetInCharge = request.user.emp_user.assets_set.all().count()

    Emp_New_Assets = request.user.emp_user.assets_set.filter(Asset_State = 'New').count() 
    Emp_Good_Assets = request.user.emp_user.assets_set.filter(Asset_State = 'Good').count() 
    Emp_Used_Assets = request.user.emp_user.assets_set.filter(Asset_State = 'Used').count() 
    Emp_Defective_Assets = request.user.emp_user.assets_set.filter(Asset_State = 'Defective').count() 


    #assetw = request.user.employee.assets.quantity_set.all() to be done later 
    total_assets = asset.count()

    #total_quantity = assetw.count()

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

        "assets_by_employee":assets_by_employee,

        "assets_by_employees":assets_by_employees,

        "asset":asset, "total_assets":total_assets, "assetInCharge":assetInCharge, 
        "Emp_New_Assets":Emp_New_Assets,"Emp_Good_Assets":Emp_Good_Assets,
        "Emp_Used_Assets":Emp_Used_Assets,"Emp_Defective_Assets":Emp_Defective_Assets
    }

    return render(request, 'usersPage.html', myquery )

@login_required(login_url='login')
def table(request):
   
    vendor = Vendor.objects.all()

    assets = Assets.objects.all()

    myFilter = AssetFilter(request.GET, queryset=assets)
    assets = myFilter.qs

    UserFilterAsset = AssetFilter_User(request.GET, queryset=assets)
    assets = UserFilterAsset.qs
    #tblquery = myFilter.qs # filter later

    tblquery = {
        "vendor" : vendor,
        "assets" : assets,
        'myFilter' : myFilter,
        'UserFilterAsset': UserFilterAsset,

    }
   

    return render(request, 'table.html', tblquery)


@login_required(login_url='login')
def registerassets(request):

    Assetform = AssetForm()
    if request.method == 'POST':
      #print('Done POSTED:', request.POST)
       Assetform = AssetForm(request.POST)
       if Assetform.is_valid(): 
        Assetform.save()
        messages.success(request, 'Asset has been successfully added.')
        return redirect('registerassets')

    Vendorform = VendorForm()
    if request.method == 'POST':
      #print('Done POSTED:', request.POST)
       Vendorform = VendorForm(request.POST)
       if Vendorform.is_valid(): 
        Vendorform.save()
        messages.success(request, 'Vendor has been successfully added.')
        return redirect('registerassets')

    context = {'Assetform': Assetform,'Vendorform': VendorForm }
    return render(request, 'registerassets.html', context)

@login_required(login_url='login')
def userPage(request):
    
    asset = request.user.emp_user.assets_set.all()

    assetInCharge = request.user.emp_user.assets_set.all().count()

    Emp_New_Assets = request.user.emp_user.assets_set.filter(Asset_State = 'New').count() 
    Emp_Good_Assets = request.user.emp_user.assets_set.filter(Asset_State = 'Good').count() 
    Emp_Used_Assets = request.user.emp_user.assets_set.filter(Asset_State = 'Used').count() 
    Emp_Defective_Assets = request.user.emp_user.assets_set.filter(Asset_State = 'Defective').count() 


    #assetw = request.user.employee.assets.quantity_set.all() to be done later 
    total_asset = asset.count()

    #total_quantity = assetw.count()
    
    context = {'asset':asset, 'total_asset':total_asset, 'assetInCharge':assetInCharge, 
    'Emp_New_Assets':Emp_New_Assets,'Emp_Good_Assets':Emp_Good_Assets,
    'Emp_Used_Assets':Emp_Used_Assets,'Emp_Defective_Assets':Emp_Defective_Assets}
    return render(request, 'user.html', context)

@login_required(login_url='login')
def accountSettings(request):
    employee = request.user.employee
    form = UserForm(instance=employee)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES,instance=employee)
        if form.is_valid():
            form.save()
            
    context = {'form':form}
    return render(request, 'account_settings.html', context)

##################### User Details Page ###########################

@login_required(login_url='login')
#@allowed_users(allowed_roles=['users'])
def userDetails(request, employee_id=None):

    #employee = Employee.objects.get(id=employee_id)
    #asset_count = Assets.objects.filter(employee=employee).count()

    if employee_id is not None:
        employee = Employee.objects.get(id=employee_id)
        asset_count = Assets.objects.filter(employee=employee).count()
    else:
        employee = None
        asset_count = 0
   
    context = {'employee': employee, 'asset_count': asset_count}
    return render(request, 'userdetails.html', context)

@login_required(login_url='login')
def accountSuperSettings(request):
    super = request.user
    form = SuperUserForm(instance=super)

    if request.method == 'POST':
        form = SuperUserForm(request.POST, request.FILES,instance=super)
        if form.is_valid():
            form.save()

            
    context = {'form':form}
    return render(request, 'account_settings.html', context)

def loginPageSSS(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Email or Password is Incorrect')

    context = {}
    return render(request, 'registration/sign_in.html')

def loginPage(request):


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser or user.groups.filter(name='admin').exists():
                return redirect('admin:index')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'registration/sign_in.html')

#@unauthenticated_user
def loginPagefff(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.groups.filter(name='super_admin').exists():
                return redirect('admin:index')
            elif user.groups.filter(name='users').exists():
                return redirect('home')
            else:
                return HttpResponse('Page not found')
        return redirect('login')
    return render(request, 'registration/sign_in.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutUser(request):
    logout(request)
    next_page = reverse('login')
    response = redirect(next_page)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
#def updateAsset(request, pk):

#    asset = Assets.objects.get(id=pk)
#    Assetform = AssetForm(instance=asset)
    
#    if request.method == 'POST':
#       Assetform = AssetForm(request.POST, instance=asset)
#       if Assetform.is_valid(): 
#        Assetform.save()
#        return redirect('table')

#    context = {'Assetform':Assetform}
#    return render(request, 'asset_form.html', context)


@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin','users'])
def asset_update(request, pk):

    asset = get_object_or_404(Assets, pk=pk)

    form = AssetForm(instance=asset)
    
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save()
            messages.success(request, f'Asset {asset.Name} was updated successfully')
            return redirect('table')
        
    return render(request, 'asset_form.html', {'form': form, 'title':'Update Asset', 'method':'PUT'})



#@login_required(login_url='login')
#def updateVendor(request, pk):

 #   vendor = Vendor.objects.get(id=pk)
  #  Vendorform = VendorForm(instance=vendor)
    
   # if request.method == 'POST':
    #   Vendorform = VendorForm(request.POST, instance=vendor)
     #  if Vendorform.is_valid(): 
      ##  Vendorform.save()
        #return redirect('registerassets')

#    context = {'Vendorform': Vendorform}
 #   return render(request, 'registerassets.html', context)


@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
def deleteAsset(request, pk):

    asset = Assets.objects.get(id=pk)
    if request.method == "POST":
        asset.delete()
        return redirect('/')

    context = {'item':asset}
    return render(request, 'delete.html', context)

#Show the date and time of a record 
def showdate(request):
    datetime.datetime.now()
    return render(request, 'home.html')


#employee report 
def employeeReport(request):
    employee_list = Employee.objects.all()
    return render(request, 'report/employeereport.html', {'employee_list': employee_list})

#vendor report 
def vendorReport(request):
    vendor_list = Vendor.objects.all()
    return render(request, 'report/vendorRe.html', {'vendor_list': vendor_list})

#asset report 
def assetReport(request):
    asset_list = Assets.objects.all()
    return render(request, 'report/assetRe.html', {'asset_list': asset_list})