from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from .models import Useraccount,Posts,Likes
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.http import HttpResponse
# Create your views here.


@login_required(login_url='/amigo/login')
def home(request):
   posts=Posts.objects.all().order_by('-time')
   userlikes=Likes.objects.filter(like_email=request.session['email'])
   user_like_posts=[]
   for i in userlikes:
      user_like_posts.append(int(i.post_id))
   print(user_like_posts)
   likes_count={}
   for i in posts:
      postid = i.post_id
      postcount= Likes.objects.filter(post_id=postid).count()

      likes_count[postid]=postcount

   print(likes_count)
   return render(request, "amigo/index.html", {'posts':posts, 'user_like_posts':user_like_posts , 'likes_count':likes_count})


def sign_up_page(request):
   if request.method == 'POST':
      email = request.POST['email']
      first_name = request.POST['first_name']
      last_name = request.POST['last_name']
      password = request.POST['password']
      gender = request.POST['gender']
      age = request.POST['age']
      country = request.POST['country']

      if Useraccount.objects.filter(email=email).exists():
         print("Email already exists")
         msg = "* This Email Id already registered!!"
         return render(request, 'amigo/signup.html', {'msg': msg})
      else:
         user = Useraccount.objects.createuser(email=email, password=password , first_name=first_name,last_name=last_name,
                                               gender=gender,age=age,country= country)
         user.save()
         print("user created")
         messages.success(request, 'Succesfully userprofile created!')
         user = authenticate(request, email=email, password=password)
         if user is not None:
             login(request,user)
             request.session['email'] = email
             request.session['username'] = user.first_name+" "+user.last_name
         else:
            print("user not authenticated")

         return redirect("/amigo/home")


   return render(request,'amigo/signup.html')


def login_page(request):

   if request.method == 'POST':
      email = request.POST.get('email')
      password = request.POST.get('password')
      user = authenticate(request,email=email, password=password)
      if user is not None:
         login(request, user)
         request.session['email'] = email
         request.session['username'] = user.first_name+" "+user.last_name

         return redirect('/amigo/home')
      else:
         print("Invalid Credentials")
         message = "*Invalid Credentials"
         res = render(request, 'amigo/signup.html', {'message': message})
   else:
      res = render(request, 'amigo/signup.html')
   return res


def userLogout(request):
   logout(request)
   return redirect('/amigo/login')

def profile(request):
      posts = Posts.objects.filter(email_id=request.session['email'])

      userlikes = Likes.objects.filter(like_email=request.session['email'])
      user_like_posts = []
      for i in userlikes:
         user_like_posts.append(int(i.post_id))
      print(user_like_posts)
      likes_count = {}
      for i in posts:
         postid = i.post_id
         postcount = Likes.objects.filter(post_id=postid).count()

         likes_count[postid] = postcount

      print(likes_count)
      return render(request, 'amigo/profile.html',{'posts':posts, 'user_like_posts':user_like_posts , 'likes_count':likes_count})


def about(request):
   return render(request, 'amigo/about.html')

def photos(request):
      return render(request, 'amigo/photos.html')


def friends(request):
   return render(request, 'amigo/friends.html')

def upload(request):
   if request.method == 'POST':
      post = Posts()

      usename = request.session['username']
      email   = request.session['email']
      now = datetime.now()
      today= now.strftime("%d/%m/%Y %I:%M:%S %p")
      post_text = request.POST['post_text']

      uploaded_file = request.FILES['document']
      print(post_text)
      fs = FileSystemStorage()
      fs.save(uploaded_file.name, uploaded_file)
      print(uploaded_file.name)
      print(uploaded_file.size)

      img_name = uploaded_file.name

      # post.post_id =
      post.username = usename
      post.email_id = email
      post.time = today
      post.post_text = post_text
      post.post_img = img_name

      print(post.post_id)

      post.save()

      return redirect('/amigo/home')



def like_post(request):
   #def like_post(request):
      # if request.is_ajax():
      #     username = request.post.get('like_username')
      #     print(username)
      #     print("working")
      # else:
      #     print("not working")

      if request.method == 'GET':
         post_id = request.GET['post_id']
         post_like_name = request.GET['post_like_name']
         post_like_email = request.GET['post_like_email']

         l = Likes()

         l.post_id = post_id
         l.like_username = post_like_name
         l.like_email = post_like_email

         l.save()

         print(post_id)
         print(post_like_name)

         # likedpost = Post.obejcts.get(pk=post_id) #getting the liked posts
         # m = Like(post=likedpost) # Creating Like Object
         # m.save()  # saving it to store in database
         return HttpResponse(post_id)  # Sending an success response
      else:
         return HttpResponse("Request method is not a GET")
