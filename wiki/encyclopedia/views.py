import os
import random
from markdown2 import Markdown
from django.shortcuts import render
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.files.storage import default_storage


class SearchForm(forms.Form):
    search = forms.CharField(label="Search", required=False,
    widget= forms.TextInput
    (attrs={'placeholder':'Search Encyclopedia'}))

class NewPage(forms.Form):
    NewPage_Name = forms.CharField(label="New_Page_Name")
    NewPage_Text = forms.CharField(label="Text_Input", required=True,
    widget= forms.Textarea
    (attrs={'placeholder':'Enter your markdown text here'}))

class EditPage(forms.Form):
    title = forms.CharField(label="New_Page_Name")
    data = forms.CharField(label="Text_Edititng", required=True,
    widget= forms.Textarea)

form = SearchForm()


markdowner = Markdown()

def index(request):
     return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":form
     })


def get_title(request, title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/get.html", {
            "entry": markdowner.convert(entry),
            "title": title,
            "form": form
        })

def get_search(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            searchquery = form.cleaned_data["search"].lower()
            all_entries = util.list_entries()

            files=[filename for filename in all_entries if searchquery in filename.lower()]

            if len(files) == 0:
                return render(request, "encyclopedia/search_results.html", {
                    'error' : "No results found",
                    "form":form
                })
            elif len(files) == 1:
                title = files[0]
                return get_title(request, title)
            else:
                title = [filename for filename in files if searchquery == filename.lower()]
                if len(title)>0:
                    return get_title(request, title[0])
                else:
                    return render(request, "encyclopedia/search_results.html", {
                        'results': files,
                        "form": form
                    })
        else:
            return index(request)
    return index(request)

def MakeNewPage(request):
    if request.method == "POST":
        form1= NewPage(request.POST)
        if form1.is_valid():
            new_page1 = form1.cleaned_data["NewPage_Name"]
            new_page2 = form1.cleaned_data["NewPage_Text"]
            util.save_entry(new_page1, new_page2)
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form1": form1
            })

        else:
            return render(request, "encyclopedia/NewPage.html", {
                "form1": form
            })

    return render(request, "encyclopedia/NewPage.html", {
              "form1": NewPage()
    })

def RandomPage(request):
    entries = util.list_entries()
    bozi = random.choice(entries)
    entri = util.get_entry(bozi)
    return render(request, "encyclopedia/get.html", {
            "entry": markdowner.convert(entri),
            "form": SearchForm(),
            "title": bozi
        })

def EditEntry(request, title):
    if request.method == "POST":
        entry = util.get_entry(title)
        edit_form = EditPage(initial={'title': title, 'data': entry})
        return render(request, "encyclopedia/EditPage.html", {
            "form": SearchForm(),
            "entry": entry,
            "editPageForm": edit_form,
            "title": title
        })
 
def submitEdit(request, title):
    if request.method == "POST":
        form3 = EditPage(request.POST)
        if form3.is_valid():
            content = form3.cleaned_data["data"]
            title2 = form3.cleaned_data["title"]
            if title2 != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            util.save_entry(title2, content)
            entry = util.get_entry(title2)
        return render(request, "encyclopedia/get.html", {
                "title": title2,
                "entry": markdowner.convert(entry),
                "form": form
        })


