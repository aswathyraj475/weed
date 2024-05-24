from django.shortcuts import render,redirect
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from keras.applications.imagenet_utils import preprocess_input
from django.contrib import messages
from PIL import Image
from Frontend.models import Review,Registration


def home(request):
    x=Review.objects.all()
    return render(request,'Home.html',{'x':x})

def detect_weed_or_crop(request):
    if request.method == 'POST':
        # Assume file is passed in the request
        img_file = request.FILES['image_file']

        # Load the trained model
        model = load_model('weed_model.h5', compile=False)

        # Read and resize the image file
        img = Image.open(img_file)
        img = img.resize((224, 224))  # Resize to match the model's expected input shape

        # Preprocess the image
        x = np.array(img, dtype=np.float32) / 255
        x = np.expand_dims(x, axis=0)
        img_data = preprocess_input(x)

        # Predict the class
        prediction = np.argmax(model.predict(img_data), axis=1)

        # Return the result as a response
        if prediction == 0:
            result = 'Weed Detected'
        else:
            result = 'Crop Detected'

        messages.success(request,result)

    # Handle GET requests
    return render(request, 'Home.html')

def ReviewSave(req):
    if req.method=="POST":
        nm=req.POST.get('uname')
        des=req.POST.get('txt')
        x=Review(username=nm,Description=des)
        x.save()
        messages.success(req,"Review Submitted Successfully")
        return redirect(home)

def RegistrationForm(req):
    return render(req,"Registration.html")



def Registration_save(request):
    if request.method == "POST":
        nm = request.POST.get('uname')
        em = request.POST.get('email')
        passw = request.POST.get('password')
        con = request.POST.get('cpassword')
        if passw != con:
            messages.error(request, "Password and confirm password do not match.")
            return redirect(RegistrationForm)
        registration = Registration(username=nm, Email=em, Password=passw, Confirm_Password=con)
        registration.save()
        return redirect(Login_Pg)

def Login_Pg(req):
    return render(req,"Login_Pg.html")

def Login_fun(request):
    if request.method=="POST":
        nm=request.POST.get('uname')
        pwd=request.POST.get('password')
        if Registration.objects.filter(username=nm,Password=pwd).exists():
            request.session['username']=nm
            request.session['Password']=pwd
            messages.success(request, "Logged in Successfully")
            return redirect(home)
        else:
            messages.warning(request, "Check Your Credentials")
            return redirect(Login_Pg)
    else:
        messages.warning(request, "Check Your Credentials Or Sign Up ")
        return redirect(Login_Pg)

def Logout_fn(request):
    del request.session['username']
    del request.session['Password']
    messages.success(request, "Logged Out Successfully")
    return redirect(Login_Pg)