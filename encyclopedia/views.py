from django.shortcuts import render
from django.contrib import messages
import os
from . import util
from numpy import random
from markdown2 import markdown

def index(request):#Index Page
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def title(request,name): #Entry Page
    list = os.listdir('entries')
    list = [x.upper() for x in list]
    newlist = []
    for index in range(len(list)):
        newlist.append(list[index][:-3])
    if name.upper() not in newlist:
        return render(request, "encyclopedia/error.html")


    ##################this part only executes if the user clicks on edit page button#######################
    if request.POST.get("editedtext")!=None:
        edited_text= request.POST.get("editedtext")
        util.save_entry(name, edited_text)
    ################################################################################################

    return render(request, "encyclopedia/title.html",{"name": markdown(util.get_entry(name)),"title_name":name})



def searchresult(request): #Search
    keyword = request.POST.get("q")
    keyword = keyword.upper()
    list = os.listdir('entries')
    list = [x.upper() for x in list]
    newlist=[]
    for index in range(len(list)):
        newlist.append(list[index][:-3])
    if keyword in newlist: #this checks if the whole keyword matches to any name of the file in newlist
        name = keyword
        return render(request, "encyclopedia/title.html",{"name": markdown(util.get_entry(name)),"title_name":name})
    elif [i for i in newlist if keyword in i]: #this check the the part of the keyword matches to any part of the file name in the list
        result = [i for i in newlist if keyword in i]
        return render(request, "encyclopedia/searchresult.html", {"result": result})#this will send a list of matching names to the html file
    else:#this will only run if the keyword is not present in the list or doesnt match any names in the list and it will show error
        messages.error(request,'ERROR!!! could not find what you where searching for be more specific')
        return render(request, "encyclopedia/searchresult.html")




def create(request): #New Page
    if request.POST.get("title")!=None:
        new_title = request.POST.get("title")
        new_content = request.POST.get("text")
        list = os.listdir('entries')#here we get all the names of the files in entries and save it in list
        list = [x.upper() for x in list] #all elements in the list are converted to upper class
        newlist = []
        for index in range(len(list)):
            newlist.append(list[index][:-3]) # the suffix ".md" from each word in the list is removed
        if new_title.upper() in newlist: #we check if the entered title is present in newlist
            messages.error(request,f'ERROR!!! There is already a page with the Title name {new_title} please enter a unique title')
            return render(request,"encyclopedia/create.html")
        else:
            util.save_entry(new_title,new_content)
            return render(request, "encyclopedia/title.html", {"name": markdown(util.get_entry(new_title)), "title_name": new_title})

    return render(request,"encyclopedia/create.html")

def edit(request,name): #edit page
    #once you click edit you will be redirected here and once you save edit you will be redirected to title (entries page)
    return render(request, "encyclopedia/edit.html",{"name": util.get_entry(name),"title_name":name})

def randompage(request):
    list = os.listdir('entries')
    newlist = []
    for index in range(len(list)):
        newlist.append(list[index][:-3])
    name = random.choice(newlist)
    return render(request, "encyclopedia/title.html", {"name": markdown(util.get_entry(name)), "title_name": name})





