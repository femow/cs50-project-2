from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import randrange
from markdown2 import Markdown

from . import util

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def pages(request, name):
    listEntries = util.list_entries()
    curPage = name
    entry = None
    _list = list(filter(lambda n: n.lower() == name.lower(), listEntries))
    if(len(_list) > 0):
        curPage = _list[0]
        entry = markdowner.convert(util.get_entry(curPage))
    else:
        entry = None

    return render(request, "encyclopedia/pages.html", {
        "page": curPage,
        "entry": entry
    })

def randomPage(request):
    listEntries = util.list_entries()

    _page = listEntries[randrange(len(listEntries) - 1)]

    return HttpResponseRedirect(reverse("wiki:pages", args=(_page,)))

def createNewPage(request):
    if(request.method == "POST"):
        listEntries = util.list_entries()
        _post = request.POST
        _title = _post['title']
        _content = _post['content']

        if len(_title) > 0 and len(_content) > 0:
            _list = list(filter(lambda n: n.lower() == _title.lower(), listEntries))
            if(len(_list) > 0):
                return render(request, "encyclopedia/createPage.html", {
                    "error": True
                })
            else:
                util.save_entry(_title, _content)
                return HttpResponseRedirect(reverse("wiki:pages", args=(_title,)))
    
    return render(request, "encyclopedia/createPage.html", {
        "error": False
    })

def redirectPage(request):
    if request.method == "POST":
        curPage = request.POST["q"]
        listEntries = util.list_entries()
        _list = list(filter(lambda n: n.lower() == curPage.lower(), listEntries))
        if(len(_list) > 0):
            curPage = _list[0]
            return HttpResponseRedirect(reverse("wiki:pages", args=(curPage,)))
        else:
            return HttpResponseRedirect(reverse("wiki:search", args=(curPage,)))
    return None

def edit(request, name):
        
    listEntries = util.list_entries()
    _list = list(filter(lambda n: n.lower() == name.lower(), listEntries))
    if(len(_list) > 0):
        if request.method == "POST":
            _post = request.POST
            _title = _post['title']
            _content = _post['content']
            util.save_entry(_title, _content)
            return HttpResponseRedirect(reverse("wiki:pages", args=(_title,)))
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": _list[0],
                "content": util.get_entry(_list[0])
            })
    else:
        return HttpResponseRedirect(reverse("wiki:search", args=(name,)))


def search(request, name):
    _list = []
    for _name in util.list_entries():
        if name.lower() in _name.lower():
            _list.append(_name)

    return render(request, "encyclopedia/search.html", {
        "page": name,
        "entries": _list
    })