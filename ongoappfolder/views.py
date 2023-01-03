from django.views import View
import os
import stripe
import pyotp

from django.shortcuts import render
from django.views.generic import View
from django.views import View
from django.contrib import auth, messages
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from .send_sms import sendsms
from django.urls import reverse
from projectfolderongo import settings as django_settings
from django.core.mail import send_mail



    
  
class HotelProducts(View):
    @method_decorator(login_required)
    def get(self, request, name):
        hotel = HotelName.objects.filter(hotelname=name)
        context = {
            'hotel': hotel
        }
        return render(request, 'hotelproducts.html', context)


# Customer Registration
class CustomerRegistration(View):
    def get(self, request):
        return render(request, 'products/registration/registration.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        address = request.POST['address']
        phn_number = request.POST['phn_number']

        user_type = "customer"

        if password == password2:
            if UserLoginDetails.objects.filter(username=username).exists():
                messages.info(request, 'Username is already exist')
                return redirect('registration')
            else:
                login_cred = UserLoginDetails.objects.create(username=username, first_name=first_name,
                                                             last_name=last_name, email=email, address=address, phn_number=phn_number, user_type=user_type)
                login_cred.set_password(password)
                login_cred.save()
                user = UserDetails.objects.create(
                    username=login_cred, first_name=first_name, last_name=last_name, email=email, address=address, phn_number=phn_number, )
                user.save()
                # sendsms(phn_number)
                messages.info(request, 'customer registered')
                return redirect('auth/login')
        else:
            messages.info(request, 'password is not matching')
            return redirect('registration')

# MerchantRegistration


class MerchantRegistration(View):
    def get(self, request):
        return render(request, 'products/registration/merchantregistration.html')

    def post(self, request):
        global Registration
        global u1
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        hotelname = request.POST['hotelname']
        businesstype = request.POST['businesstype']
        username = request.POST['username']
        address = request.POST['address']
        u1 = username
        password = request.POST['password']
        password2 = request.POST['password2']
        user_type = "merchant"

        if password == password2:
            if UserLoginDetails.objects.filter(username=username).exists():
                messages.info(request, 'Username is already exist')
                return redirect('registration')
            else:
                login_cred = UserLoginDetails.objects.create(username=username, first_name=first_name, last_name=last_name,
                                                             email=email, address=address, phn_number=phone, user_type=user_type)
                login_cred.set_password(password)
                login_cred.save()
                print(login_cred)
                merchant = MerchantDetails.objects.create(username=login_cred, first_name=first_name, last_name=last_name,
                                                          email=email, address=address, phn_number=phone, hotel_name=hotelname,
                                                          bussiness_type=businesstype)
                merchant.save()
                subject = 'Ongo-Delivery Welcome Mail'
                message = f'Hi {merchant.username}, Welcome to Ongo-Delivery \n \t Where you can find the food to your liking'
                from_email = django_settings.EMAIL_HOST_USER
                send_mail(subject, message, from_email, [merchant.email])
                messages.info(request, 'Merchant registered')
                return redirect('auth/login')

        else:
            messages.info(request, 'password is not matching')
            return redirect('merchantregistration')


class Customer_index(View):
    
    def get(self, request):
        
        if request.user.is_staff:
            context = {
                'hotel': HotelName.objects.all(),
                'data': UserLoginDetails.objects.get(username=request.user.username)
            }
        else:
            context = {
                'hotel': HotelName.objects.all(),
                'data': UserDetails.objects.get(username__username=request.user.username)
            }

        # print(HotelName.objects.all())
        
            
        
        return render(request, 'home.html', context)


class About(View):
     def get(self, request): 
        
        context = {
                'hotel': HotelName.objects.all(),
                'data': UserDetails.objects.get(username__username=request.user.username)
            }

        return render(request, 'team/about.html' , context)

        

class Contact(View):
    def get(self, request): 
        
        context = {
                'hotel': HotelName.objects.all(),
                'data': UserDetails.objects.all( )
            }
        
        return render(request, 'team/contact.html' , context)

class Services(View):
     def get(self, request): 
        context = {
                'hotel': HotelName.objects.all(),
                'data': UserDetails.objects.get(username__username=request.user.username)
            }

        return render(request, 'team/service.html' ,context)

# class Index(View):
    
#     def get(self, request): 
#         context = {
#             'hotel': HotelName.objects.all(),
#         }
#         # print(HotelName.objects.all())
        
#         return render(request, 'home.html', context)

# Common Login page


class Login(View):
    def get(self, request):
        return render(request, 'products/registration/login.html')

    def post(self, request):
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            try:
                user_obj = UserLoginDetails.objects.get(username=username)
            except:
                messages.info(request, 'User with this username does not exists')
                return redirect("login")
            user = auth.authenticate(username=username, password=password)
            if user is None:
                messages.info(request, 'invalid password...')
                return redirect("login")
            elif user.user_type == "merchant":
                auth.login(request, user)
                return redirect('owner_index')
            else:
                auth.login(request, user)
                return redirect("customer_index")

# The logout class


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        auth.logout(request)
        return redirect('customer_index')


@login_required
def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.user.user_type == 'merchant':
        data = MerchantDetails.objects.get(username__username=request.user.username)
    else:
        data = UserDetails.objects.get(username__username=request.user.username)
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(
            request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()   
    else:
        try:
            customer = Customer.objects.get(
                user__username=request.user.username)
            # customer = Customer.object.
            if customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'products/settings.html', {'membership': membership,
                                                      'cancel_at_period_end': cancel_at_period_end,
                                                      'data':data})


class CustomerProfile(LoginRequiredMixin, ListView):
    def post(self, request):
        if request.user.user_type == 'customer':
            data = UserDetails.objects.get(username__username=request.user.username )
        elif request.user.user_type == 'merchant':
            data = MerchantDetails.objects.get(username__username=request.user.username )
        else:
            data = UserLoginDetails.objects.get(username=request.user.username )
        # if len(request.FILES) != 0:
        #     if len(data.profile_pic) > 0:
        #         os.remove(data.profile_pic.path)
        
        if request.FILES:
            data.profile_pic = request.FILES['profile_pic']


        data.first_name = request.POST['first_name']
        data.last_name = request.POST['last_name']
        data.address = request.POST['address']
        data.email = request.POST['email']
        data.save()

        messages.success(request, " Updated Successfully")

        return redirect('customer_index')

    def get(self, request):
        # data = UserLoginDetails.objects.get(username=request.user.username)
        print(request.user.id)
        if request.user.user_type == 'customer':
            data = UserDetails.objects.get(username__username=request.user.username )
        elif request.user.user_type == 'merchant':
            data = MerchantDetails.objects.get(username__username=request.user.username )
        else:
            data = UserLoginDetails.objects.get(username=request.user.username )
        context = {'data': data}
        return render(request, 'profile.html', context)


# @method_decorator(login_required(login_url='/log/'), name='dispatch')
# class EditProfile(View):
#     def get(self, request, *args, **kwargs):
#         data = User.objects.get(username=request.user)
#         return render(request, "profile.html", {'obj': data})


class Owner_index(LoginRequiredMixin, TemplateView):

    template_name = "products/productshop_owner/owner_index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(Owner_index, self).get_context_data(**kwargs)
        merchant = MerchantDetails.objects.get(
            username__username=self.request.user.username)
        context["hotelname"] = HotelName.objects.filter(owner=merchant)
        context['data'] = merchant
        print(context)

        print(merchant)
        if not merchant.is_approved:
            print(merchant.is_approved)
            context['approval'] = "needed"
        print(context)
        return context


# forloop

class Add_product(LoginRequiredMixin, View):
    form_class = HotelForm

    def get(self, request):
        HotelForm = self.form_class()
        merchant = MerchantDetails.objects.get(username__username=request.user.username)
        return render(request, "products/productshop_owner/add_product.html", {'form': HotelForm, 'merchant': merchant})

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():

                form.save(request)

                return redirect('owner_index')
            else:
                return redirect('add_product')


# This class will delete the product details
class Delete_product(LoginRequiredMixin, View):
    def get(self, request, id):
        hotelname = HotelName.objects.get(id=id)
        hotelname.delete()
        return redirect("owner_index")


# This class will edit/update the product details
class Edit_product(LoginRequiredMixin, View):
    def get(self, request, id):
        hotelname = HotelName.objects.get(id=id)
        form = HotelForm(instance=hotelname)
        return render(request, 'products/productshop_owner/edit_product.html', {'form': form})

    def post(self, request, id):
        if request.method == 'POST':
            hotelname = HotelName.objects.get(id=id)
            form = HotelForm(request.POST, request.FILES, instance=hotelname)
            print(form)
            if form.is_valid():
                form.save(request)
                return redirect("owner_index")


class ProductDetailView(LoginRequiredMixin, View):
    @method_decorator(login_required)
    def get(self, request, id):

        product_details = HotelName.objects.filter(id=id)
        context = {
            'hotel': product_details
        }
        # context['stripe_publishable_key'] = STRIPE_PUBLISHABLE_KEY
        return render(request, 'hotelproducts.html', context)


class MerchantApprovalIndex(LoginRequiredMixin, ListView):

    context_object_name = 'approvals'
    queryset = MerchantDetails.objects.filter(is_approved=False)

    template_name = 'admin/approvals.html'


class MerchantApproval(LoginRequiredMixin, View):

    def get(self, request, id):

        merchant = MerchantDetails.objects.get(id=id)
        try:
            merchant.is_approved = True
            merchant.save()
            return redirect('approvals')
            # approvals = MerchantDetails.objects.filter(is_approved=False)
        except:
            print("something went wrong")

#forgot password

def generate_random_otp():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=120)
    OTP = totp.now()
    return {"totp": secret, "otp": OTP}


class GenerateOTP(View):
    def get(self, request):
        return render(request, 'products/registration/forgot_password_generate_otp.html')

    def post(self, request):
        if request.method == 'POST':

            phone = request.POST['phn_numer']
            print('##############################################')
            print(phone)
            try:
                user = UserLoginDetails.objects.get(phn_number=phone)

            except:
                messages.info(request, 'This is not a registered phone number......')
                return redirect("generate_otp")
            try:
                key = generate_random_otp()
                print('***************************************')
                print(key)
                user.otp = key['otp']
                user.otp_activation_key = key['totp']

                user.save()
                print('***************************************')
                print(user.otp_activation_key)
                return render(request, 'products/registration/forgot_password_otp_verification.html',
                              context={'user_id': user.id})
            except:
                messages.info(request, 'something went wrong')
                return redirect("generate_otp")


class VerifyOTP(View):
    def get(self, request, id):
        return render(request, 'products/registration/forgot_password_otp_verification.html', context={'user_id': id})

    def post(self, request, id):
        if request.method == 'POST':

            otp = request.POST['otp']
            print('##############################################')
            print(otp)
            try:
                user = UserLoginDetails.objects.get(otp=otp)
            except:
                messages.info(request, 'wrong OTP......')
                return render(request, 'products/registration/forgot_password_otp_verification.html',
                              context={'user_id': id})
            try:
                activation_key = user.otp_activation_key
                totp = pyotp.TOTP(activation_key, interval=120)
                verify = totp.verify(otp)
                print('***************************************')
                print(totp)
                if verify:
                    print('***************************************')
                    print(user.otp_activation_key)
                    return render(request, 'products/registration/forgot_password_change.html',
                                  context={'user_id': user.id})
                else:
                    messages.info(request, 'otp expired')
                    return redirect("generate_otp")
            except:
                messages.info(request, 'something went wrong')
                return redirect("generate_otp")


class ForgotPasswordChange(View):
    def get(self, request, id):
        return render(request, 'products/registration/forgot_password_change.html', context={'user_id': id})

    def post(self, request, id):
        if request.method == 'POST':

            new_password = request.POST['new_password']
            repeat_password = request.POST['repeat_password']

            if new_password == repeat_password:
                try:
                    user = UserLoginDetails.objects.get(id=id)
                    print(user)
                    user.set_password(new_password)
                    user.save()
                except:
                    messages.info(request, 'something went wrong')
                    return render(request, 'products/registration/forgot_password_change.html', context={'user_id': id})
                messages.info(request, 'successfully changed password')
                return redirect("login")
            else:
                messages.info(request, 'password does not match')
                return render(request, 'products/registration/forgot_password_change.html', context={'user_id': id})


