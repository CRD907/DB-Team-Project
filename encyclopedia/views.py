from django.shortcuts import render, redirect
import markdown
import random
from . import util

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

# def save_page(request):
#     if request.method =="POST":
#         title = request.POST['title']
#         body = request.POST['content']
#         util.save_entry(title, body)
#         return render(request, "encyclopedia/entry.html", {
#         "title": title,
#         "content": body
#     })