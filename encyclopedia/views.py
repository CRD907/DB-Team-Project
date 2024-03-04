from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AbstractUser
from encyclopedia.models import User
from django.db import IntegrityError
from django.http import  HttpResponseRedirect
import markdown
import random
from . import util
from django.db import connection


def convert_to_html(page_title):
    page = util.get_entry(page_title)
    converter = markdown.Markdown()
    if page == None:
        return None
    else:
        return converter.convert(page)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    body = convert_to_html(title)
    if body == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": body
        })

def search(request):
    if request.method == "POST":
        search_query = request.POST['q']
        body = convert_to_html(search_query)
        if body is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": search_query,
                "content": body
            })
        else :
            entries = util.list_entries()
            recommendation = []
            for entry in entries:
                if search_query.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })    

def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create_new.html")
    
    if request.method == "POST":
        page = request.POST.get('page')
        info = request.POST.get('info')
        
        if util.get_entry(page):
            return render(request, "encyclopedia/error.html", 
                          {"message": "This entry already exists"})

        util.save_entry(page, info)
        return redirect('entry', title=page)
        # converted_info = convert_to_html(page)
        # return render(request, "encyclopedia/entry.html", 
        #               {"title": page, "content": converted_info})

            
def get_random(request):
    entries = util.list_entries()
    rand_entry = random.choice(entries)
    return redirect('entry', title=rand_entry)
    # body = convert_to_html(rand_entry)
    # return render(request, "encyclopedia/entry.html", {
    #     "title": rand_entry,
    #     "content": body
    # })

def edit_page(request, title):
    if request.method == 'POST':
        body = request.POST['content']
        util.save_entry(title, body)
        return redirect('entry', title)
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def login_view(request):
    if request.method == "POST":
        cursor = connection.cursor()
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        #user = authenticate(request, username=username, password=password)
        #sql = 'SELECT * FROM encyclopedia_user'
        cursor.execute('SELECT * FROM encyclopedia_user WHERE username = "' + username + '" AND password = "' + password + '"')
        user = cursor.fetchone()
        print(user)
        #Check if authentication successful
        if user is not None:
            return render(request, "encyclopedia/index.html", {'username': user[3]})
        else:
            return render(request, "encyclopedia/login.html", {"message": "Invalid username and/or password."})
    else:
        return render(request, "encyclopedia/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "encyclopedia/register.html", {
                "message": "Passwords must match."
            })

        #Create new user
        try:
            user = User(username = username, email = email, password = password)
            user.save()
        except IntegrityError:
            return render(request, "encyclopedia/register.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("index"))
        return render(request, "encyclopedia/register.html") 

def welcome(request, username):
    return render(request, "encyclopedia/welcome.html", {
        "username": username
    })  