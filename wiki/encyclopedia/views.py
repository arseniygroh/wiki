from random import randint
import markdown2
import re
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage

from . import util
from .forms import SearchForm, AddForm, EditForm

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)

    if (content == None):
        return render(request, "encyclopedia/error.html", {
            "msg": "This page is not found:("
        })
    else:
        return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown2.markdown(content)
    })

def search_entry(request):
    form = SearchForm(request.GET)
     
    if form.is_valid():
        query = form.cleaned_data.get("q")
        content = util.get_entry(query)
        if (content == None):
            result = []
            for entry in util.list_entries():
                match = re.search(query.lower(), entry.lower())
                if (match):
                    result.append(entry)
            if (len(result) == 0):
                return render(request, "encyclopedia/error.html", {
                    "msg": "This page is not found:("
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "matches": result
                })
        else:
            return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": markdown2.markdown(content)
        })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def add_entry(request):
    if request.method == 'POST':
        form = AddForm(request.POST) 
        if form.is_valid():
            title = form.cleaned_data.get("title")
            if (title in util.list_entries()):
                return render(request, "encyclopedia/error.html", {
                    "msg": "This page already exists"
                })
            else:
                content = form.cleaned_data.get("content")
                util.save_entry(title, content)
                return redirect("entry", title=title)

    else:
        form = AddForm() 
    return render(request, 'encyclopedia/add.html')

def edit_entry(request, title):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            contentUpdated = form.cleaned_data.get("content")
            html_content = markdown2.markdown(contentUpdated)
            util.save_entry(title, contentUpdated)
            return redirect("entry", title=title)
    else:
        form = EditForm()
        initialContent = util.get_entry(title)
        return render(request, 'encyclopedia/edit.html', {
            "title": str.capitalize(title),
            "content": '' if initialContent is None else initialContent
        })
            
        
def random(request):
    enties = util.list_entries()
    randomIndex = randint(0, len(enties) - 1)
    title = enties[randomIndex]
    return redirect("entry", title=title)

def delete_entry(request, title):
    if request.method == "POST":
        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            default_storage.delete(filename)
    
    return redirect("index")


