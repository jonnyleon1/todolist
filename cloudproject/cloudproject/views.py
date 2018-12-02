from django.shortcuts import render
import pyrebase
from django.contrib import auth
config = {

    'apiKey': "AIzaSyDblNYj_uJ6jq64wLDhMTpbksijVx2Wj4g",
    'authDomain': "cloudproject1-d71ec.firebaseapp.com",
    'databaseURL': "https://cloudproject1-d71ec.firebaseio.com",
    'projectId': "cloudproject1-d71ec",
    'storageBucket': "cloudproject1-d71ec.appspot.com",
    'messagingSenderId': "878214762831"
  }

""" Initiated pyrebase using a tutorial https://www.youtube.com/watch?v=8wa4AHGKUJM&list=PLhPDb5zFmGR2VfXiN2y-1V0qdRik7Cc0K  """

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database=firebase.database()

def signIn(request):
    
    return render(request, "signIn.html")

""" Figured out how to do function below using the following tutorial:

Python Django with Google Firebase Tutorial: Firebase Authentication SignIn

www.youtube.com/watch?v=8wa4AHGKUJM&list=PLhPDb5zFmGR2VfXiN2y-1V0qdRik7Cc0K  """

def postsign(request):
    email_address=request.POST.get('email')
    passwor = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email_address,passwor)
    except:
        message="Sorry, but we do not recognize that account"
        return render(request,"signIn.html",{"messg":message})
    print(user['idToken'])
    sessionKey=user['idToken']
    request.session['uid']=str(sessionKey)
    return render(request, "welcome.html",{"e":email_address})

""" Figured out how to do function below using the following tutorial:

Python Django with Google Firebase Tutorial Part3 : SignUp Form 

https://www.youtube.com/watch?v=4hTYlgPbBqg&index=3&list=PLhPDb5zFmGR2VfXiN2y-1V0qdRik7Cc0K
"""

def signUp(request):
    
    return render(request,"signup.html")


""" Figured out how to do function below using the following tutorial:

Python Django with Google Firebase Tutorial Part3 : SignUp Form 

https://www.youtube.com/watch?v=4hTYlgPbBqg&index=3&list=PLhPDb5zFmGR2VfXiN2y-1V0qdRik7Cc0K
"""

def postsignup(request):

    name=request.POST.get('name')
    email_address=request.POST.get('email')
    passwor=request.POST.get('pass')

    try:              
        user=authe.create_user_with_email_and_password(email_address,passwor)
  
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
    
    uid = user['localId']
    data={"name":name,"status":"1"}

    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")



def create(request):

    return render(request,'create.html')

""" Used a tutorial on Youtube to learn how to push data back to Firebase. https://www.youtube.com/watch?v=bq0AszeDZf4&index=4&list=PLhPDb5zFmGR2VfXiN2y-1V0qdRik7Cc0K"""

def post_create(request):

    import time
    millis = int(round(time.time()*1000))
    time_now= millis
    work = request.POST.get('work')
    progress =request.POST.get('progress')
    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    data = {
        "work":work,
        'progress':progress,
    }
    database.child('users').child(a).child('reports').child(millis).set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'welcome.html', {'e':name})

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')



""" The following function was also inspired using the method in the following 2 tutorials 

https://www.youtube.com/watch?v=rmQvrIZAzCE&list=PLhPDb5zFmGR2VfXiN2y-1V0qdRik7Cc0K&index=5

https://www.youtube.com/watchv=bq0AszeDZf4&index=4&list=PLhPDb5zFmGR2VfXiN2y-1V0qdRik7Cc0K

"""

def check(request):
    import datetime
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    timestamps = database.child('users').child(a).child('reports').shallow().get().val()
    lis_time=[]
    for i in timestamps:

        lis_time.append(i)

    lis_time.sort(reverse=True)
    work = []

    for i in lis_time:

        work2=database.child('users').child(a).child('reports').child(i).child('work').get().val()
        work.append(work2)
    print(work)


    comb_lis = zip(lis_time,work)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,'check.html',{'comb_lis':comb_lis,'e':name})



def checkbox (request):
    compl=request.POST.get('handchange')


""" Used the following resource in order to create a function below, 
https://www.youtube.com/watchv=bq0AszeDZf4&index=4&list=PLhPDb5zFmGR2VfXiN2y-1V0qdRik7Cc0K"""

def post_check(request):

    import datetime

    time = request.GET.get('z')

    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']

    work =database.child('users').child(a).child('reports').child(time).child('work').get().val()
    progress =database.child('users').child(a).child('reports').child(time).child('progress').get().val()
    i = float(time)
    name = database.child('users').child(a).child('details').child('name').get().val()

    return render(request,'follow_check.html',{'w':work,'p':progress,'e':name})