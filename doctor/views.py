import os
import datetime
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from threading import Thread
import subprocess
import warnings
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
warnings.filterwarnings("ignore")


def register(request):
    if request.method == 'GET':
        return render(request, "registeration.html")
    elif request.method == 'POST':
        doctorName = request.POST['Name']
        doctorEmail = request.POST['Email']
        doctorPassword = request.POST['Password']
        confirm=request.POST['conpass']
        name_validator = RegexValidator(regex=r'^[a-zA-Z0-9@/./+/-/_]+$', message='Letters, digits and @/./+/-/_ only.', code='invalid_name')
        try:
            name_validator(doctorName)
        except ValidationError as e:
            error_message = str(e.message)
            messages.success(request, error_message)
            return HttpResponseRedirect('/register/')
        existing_user_name = User.objects.filter(username=doctorName).first()
        if existing_user_name is not None:
            messages.success(request, "This name already exists.")
            return HttpResponseRedirect('/register/')
        existing_user_email = User.objects.filter(email=doctorEmail).first()
        if existing_user_email is not None:
            messages.success(request, "This email already exists.")
            return HttpResponseRedirect('/register/')
        if doctorPassword != confirm:
            messages.success(request, 'The password is not compatible')
            return HttpResponseRedirect('/register/')
        else:
            doctoruser = User.objects.create_user(doctorName, doctorEmail, doctorPassword)
            doctoruser.save()
            foldername = doctorName.replace(" ", "")
            path = "F:/GraduationProject/oct/media/users" + "/" + foldername
            if not os.path.exists(path):
                os.makedirs(path)
            return HttpResponseRedirect('/')


def loginpage(request):
    if request.method == 'GET':
        return render(request, "login.html")
    elif request.method == 'POST':
        doctorName = request.POST['Name']
        doctorPassword = request.POST['Password']
        user = authenticate(request, username=doctorName, password=doctorPassword)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home/')
        else:
            messages.success(request, "There Was An Error Logging In ,Try Again...")
            return HttpResponseRedirect('/')





def logoutpage(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='login')
def account_page(request):
    op = Operation.objects.filter(users=request.user)
    user = User.objects.get(email=request.user.email)
    return render(request, "myaccount.html", {"Operations": op, "User": user})



@login_required(login_url='login')
def edit_page(request):
    user = User.objects.get(email=request.user.email)
    if request.method == 'GET':
        return render(request, "editprofile.html", {"User": user})
    elif request.method == 'POST':
        NewEmail = request.POST['newemail']
        existing_user = User.objects.filter(email=NewEmail).exclude(id=user.id).first()
        if existing_user is not None:
            messages.success(request, 'The user with this email already exists. Please enter another email')
            return HttpResponseRedirect('/account/editprofile')
        else:
            user.email = NewEmail
            user.save()
            return HttpResponseRedirect('/account/')


@login_required(login_url='login')
def change_page(request):
    user = User.objects.get(password=request.user.password)
    if request.method == 'GET':
        return render(request, "changepassd.html",{"User": user})
    elif request.method == 'POST':
        new_password = request.POST['newpass']
        confirm_password = request.POST['conpass']
        if new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            return HttpResponseRedirect('/')
        else:
            messages.success(request, 'The password is not compatible')
            return HttpResponseRedirect('/account/changepassword')



@login_required(login_url='login')
def details_page(request, pk):
    op = Operation.objects.get(id=pk)
    if (op.ProcessName == "OCT"):
        return render(request, "details.html", {"Operations": op})
    else:
        return render(request, "details2.html", {"Operations": op})


@login_required(login_url='login')
def OCT_options_page(request):
    return render(request, "services/one/options1.html")


@login_required(login_url='login')
def OCT_steps_page(request):
    return render(request, "services/one/steps.html")


@login_required(login_url='login')
def Message_OCT_page(request):
    return render(request, "services/one/message.html")


def send_email(user_email, image_path, context):
    html_content = render_to_string("email.html", context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives('Welcome to Noor Website', text_content, settings.EMAIL_HOST_USER,
                                 [user_email])
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(image_path)
    msg.send()

@login_required(login_url='login')
def OCT_subservicesnew_page(request):
    return render(request, "services/one/subservicesnew.html")


@login_required(login_url='login')
def OCT_subservices_page(request):
    if request.method == 'GET':
        return render(request, "services/one/subservices.html")
    elif request.method == 'POST':
        current_user = request.user
        name = str(current_user).replace(" ", "")
        root_path = f'F:/GraduationProject/oct/media/users/{name}/tasks/' + datetime.datetime.now().strftime(
            '%Y/%m/%d_%H-%M-%S')
        list = ['in', 'out']
        pathin = os.path.join(root_path, str(list[0]))
        os.makedirs(pathin, exist_ok=True)
        pathout = os.path.join(root_path, str(list[1]))
        os.makedirs(pathout, exist_ok=True)
        image = FileSystemStorage()
        request.FILES['image'].name = "image.jpeg"
        file = image.save(pathin + "/" + request.FILES['image'].name, request.FILES['image'])
        subprocess.call(
            f"docker run  -v  {pathin}:/WorkingFiles/in  -v {pathout}:/WorkingFiles/out -v "
            f"F:\GraduationProject\oct\ML\model:/WorkingFiles/model binoct")
        readfile = open(f"{root_path}/out/out.txt", "r")
        output = readfile.readline()
        readfile.close()
        con='/media/'+file
        if output == "This is not OCT images":
            messages.success(request, format_html("This is not OCT image<br> Please upload another photo"))
            return render(request, "services/one/subservicesnew.html",{'context':str(con)})

        else:
            readfile2 = open(f"{root_path}/out/out2.txt", "r")
            lines = readfile2.readlines()
            new_lst = [''.join(line.splitlines()) for line in lines]
            readfile2.close()
            cnv = new_lst[0]
            dme = new_lst[1]
            drusen = new_lst[2]
            normal = new_lst[3]
            ser = Operation.objects.create(Input=request.FILES['image'], Output=output, CNV=cnv, DME=dme, Drusen=drusen,
                                           NormalOCT=normal, ProcessName="OCT")
            ser.save()
            ser.users.add(current_user.id)
            email_context = {"output": output, "CNV": cnv,
                             "DME": dme, "Drusen": drusen,
                             "Normal": normal}

            def async_send():
                send_email(current_user.email,
                           pathin + r"\\" + request.FILES['image'].name,
                           email_context)

            t1 = Thread(target=async_send, args=())
            t1.start()
            messages.success(request,
                             format_html("Thank you for using Noor website.<br> You will receive an email with the result of the diagnosis immediately after the operation is completed"))
            return render(request, "services/one/subservicesnew.html",{'context':str(con)})


@login_required(login_url='login')
def Macula_options_page(request):
    return render(request, "services/two/options2.html")


@login_required(login_url='login')
def Macula_steps_page(request):
    return render(request, "services/two/steps2.html")


@login_required(login_url='login')
def Message_Macula_page(request):
    return render(request, "services/two/message2.html")


def macula_send_email(user_email, image_path, context):
    html_content = render_to_string("email2.html", context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives('Welcome to Noor Website', text_content, settings.EMAIL_HOST_USER,
                                 [user_email])
    msg.attach_alternative(html_content, "text/html")
    msg.attach_file(image_path)
    msg.send()


@login_required(login_url='login')
def Macula_subservices_page(request):
    if request.method == 'GET':
        return render(request, "services/two/subservices2.html")
    elif request.method == 'POST':
        current_user = request.user
        name = str(current_user).replace(" ", "")
        root_path = f'F:/GraduationProject/oct/media/users/{name}/tasks/' + datetime.datetime.now().strftime(
            '%Y/%m/%d_%H-%M-%S')
        list = ['in', 'out']
        pathin = os.path.join(root_path, str(list[0]))
        os.makedirs(pathin, exist_ok=True)
        pathout = os.path.join(root_path, str(list[1]))
        os.makedirs(pathout, exist_ok=True)
        image = FileSystemStorage()
        request.FILES['image'].name = "image.jpeg"
        file = image.save(pathin + "/" + request.FILES['image'].name, request.FILES['image'])

        subprocess.call(f"docker run  -v  {pathin}:/WorkingFiles/in  -v {pathout}:/WorkingFiles/out -v "
                        f"F:\GraduationProject\oct\ML\model2:/WorkingFiles/model binmacula")
        readfile = open(f"{root_path}/out/out.txt", "r")
        output = readfile.readline()
        readfile.close()
        con='/media/'+file
        if output == "This is not Macula image":
            messages.success(request, format_html("This is not Macula image<br> Please upload another photo"))
            return render(request, "services/two/subservicesnew2.html",{'context':str(con)})
        else:
            readfile2 = open(f"{root_path}/out/out2.txt", "r")
            lines = readfile2.readlines()
            new_lst = [''.join(line.splitlines()) for line in lines]
            readfile2.close()
            macular_degeneration = new_lst[0]
            cataract = new_lst[1]
            diabetes = new_lst[2]
            glaucoma = new_lst[3]
            hypertension = new_lst[4]
            pathological_myopia = new_lst[5]
            normal_macular = new_lst[6]
            other = new_lst[7]
            ser = Operation.objects.create(Input=request.FILES['image'], Output=output,
                                           MacularDegeneration=macular_degeneration, Cataract=cataract,
                                           Diabetes=diabetes, Glaucoma=glaucoma, Hypertension=hypertension,
                                           PathologicalMyopia=pathological_myopia, NormalMacular=normal_macular,
                                           Other=other, ProcessName="Macula")
            ser.save()
            ser.users.add(current_user.id)
            email_context = {"output": output, "MacularDegeneration": macular_degeneration, "Cataract": cataract,
                             "Diabetes": diabetes, "Glaucoma": glaucoma, "Hypertension": hypertension,
                             "PathologicalMyopia": pathological_myopia, "NormalMacular": normal_macular, "Other": other}

            def async_send():
                macula_send_email(current_user.email,
                                  pathin + r"\\" + request.FILES['image'].name,
                                  email_context)

            t1 = Thread(target=async_send, args=())
            t1.start()
            messages.success(request,
                             format_html("Thank you for using Noor website.<br> You will receive an email with the result of the diagnosis immediately after the operation is completed"))
            return render(request, "services/two/subservicesnew2.html",{'context':str(con)})

