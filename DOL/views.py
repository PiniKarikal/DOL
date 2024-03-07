import random
from DOL_contracts.models import User
from django.shortcuts import render
import smtplib

otp_global = None
user_data_global = {}

def register(request):
    error_dict = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        confpassword = request.POST['confpassword']
        f_name = request.POST['fname']
        l_name = request.POST['lname']
        phone_number = request.POST['phonenumber']

        email_error = None
        phone_number_error = None
        password_error = None

        if User.objects.filter(email = email).exists():
            email_error = "Email already exists"
            error_dict['email_error'] = email_error

        if User.objects.filter(phone_number = phone_number ).exists():
            phone_number_error = "Phone number already registered"
            error_dict['phone_number_error'] = phone_number_error

        if password != confpassword :
            password_error = "Password must be same"
            error_dict['password_error'] = password_error

        if email_error == None and phone_number_error == None and password_error == None :
            otp = generate_random_number()
            emailVerification(email,otp)
            user_data_global['email'] = email
            user_data_global['f_name'] = f_name
            user_data_global['l_name'] = l_name
            user_data_global['password'] = password
            user_data_global['phone_number'] = phone_number
            user_data_global['mail_otp'] = otp
            print(user_data_global['mail_otp'])
            
            
            return render(request, 'otp_verification.html')
        else:
            return render(request, 'register.html', error_dict)
            
    return render(request, 'register.html')




def emailVerification(emailid, otp):
    HOST = "smtp.gmail.com"
    PORT = 587

    FROM_EMAIL = 'praveenhegde0987@gmail.com'
    TO_EMAIL = emailid
    PASSWORD = "ttfa pezz movu jjwg"

    MESSAGE = f"""Subject: Mail from DOL
    Hi User, 

    Your OTP is: {otp}

    This is the electronic generated mail frpm DOL.

    Thanks,"""
    smtp = smtplib.SMTP(HOST, PORT)
    status_code, response = smtp.ehlo()
    print(f"[*] Echoing the server: {status_code} {response}")

    status_code, response = smtp.starttls()
    print(f"[*] Starting TLS connection: {status_code} {response}")

    status_code, response, = smtp.login(FROM_EMAIL, PASSWORD)
    print(f"[*] Logging in: {status_code} {response}")

    smtp.sendmail(FROM_EMAIL, TO_EMAIL, MESSAGE)

    smtp.quit()


def generate_random_number():
    return random.randint(10**5, 10**6 - 1)


def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST['otpnumber']
        
        if int(otp) == user_data_global['mail_otp']:
            user_creation(user_data_global)
            user_data_global['mail_otp'] = None
            return render(request, 'index.html')
        
        else:
            return render(request, 'otp_verification.html', {'error_msg' : 'OPT eneterd is false'})
    return render(request, 'index.html')



def user_creation(user_data):
    user = User.objects.create_user(email = user_data['email'], password = user_data['password'], first_name = user_data['f_name'], last_name = user_data['l_name'], phone_number = user_data['phone_number'])
    user.save()



def index(request):
    return render(request, 'index.html')



