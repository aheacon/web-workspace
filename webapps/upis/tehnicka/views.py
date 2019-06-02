from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect

from tehnicka.models import Ucenik, Smjer, Predmet, Diploma, PredmetIspis, Priznanja
from django.contrib.auth import authenticate, login, logout
import json

from .util import *
from .statistika import *

#### ---------------- INDEX VIEW  ---------------- ####
# INDEX: This view should show all students with corresponding classes and grades
def index_base(request):
    context={
    'smjerovi': Smjer.objects.all()
    }
    return render(request, 'tehnicka/index_base.html',context)

def index(request, smjer_id):
    message=''
    if request.session.get('message'):
        message='Korisnik obrisan!'
        del request.session['message']
    return racunajStatistiku(request, smjer_id, message)

#### ---------------- ADD VIEW  ---------------- ####
# ADD STUDENT: This view should add new student (optional with data from form

def dodajucenika(request):
        if request.method == "POST":
            try:
                return saveStudent(request)
            except KeyError:
                # Prints the error and the line that causes the error
                #import sys
                #print ("%s - %s at line: %s" % (sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
                return HttpResponse("Key error dodajucenika")
        else: # GET request
            #return helpefFunction(request) # has to go return and it doesn't matter where this function is defined
            return getStudent(request)

# def helpefFunction(request):
#     return HttpResponse("helper to check")

#### ---------------- EDIT/DETAILS VIEW  ---------------- ####
def details(request, ucenik_id):
    if request.method == "POST":
        try:
            return updateStudent(request, ucenik_id)
        except KeyError:
            return HttpResponse("Key error - post uredi")

    else:
        return get_for_update(request, ucenik_id)
#### ---------------- DELETE VIEW  ---------------- ####
def delete(request, ucenik_id):

    if request.user.is_authenticated:
        return deleteStudent(request, ucenik_id)

def brisipriznanje(request, priznanje_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            return deleteAcknowledgments(request, priznanje_id)

def test_view(request):
    t=None
    test=Test(t=t)
    test.save()
    t=1
    test=Test(t=t)
    test.save()
