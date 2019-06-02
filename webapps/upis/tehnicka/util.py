from tehnicka.models import Ucenik, Smjer, Predmet, Diploma, PredmetIspis, Priznanja
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
import sys

###############################################################################
#                   CREATE- dodajStudenta                                     #
###############################################################################
def getStudent(request):
    #ys.setrecursionlimit(10000)
    inf=PredmetIspis.objects.filter(razred_id=6).filter(kod="IN"); #moramo dodati informatiku
    deveti=PredmetIspis.objects.filter(razred_id=9);
    deveti|=inf; # napravi uniju

    context={
    'smjerovi': Smjer.objects.all(),
    'predmeti_header': deveti.order_by('-razred_id'),
    }
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    return render(request, 'tehnicka/dodajucenika.html', context)


def saveStudent(request):
    ime=request.POST["ime"]
    prezime=(request.POST["prezime"])
    osnovna_skola=(request.POST["osnovna_skola"])
    smjer_id=(request.POST["smjer"])
    smjer=Smjer.objects.get(id=smjer_id)

    razred6_per_predmet=request.POST.getlist('razred6')
    razred7_per_predmet=request.POST.getlist('razred7')
    razred8_per_predmet=request.POST.getlist('razred8')
    razred9_per_predmet=request.POST.getlist('razred9')

    priznanja_naziv=request.POST.getlist('priznanje_naziv');
    priznanje_bodovi=request.POST.getlist('priznanje_bodovi');
    # Handle empty IntegerField
    # try:
    #    jmbg=int(request.POST["jmbg"])
    # except ValueError:
    #    jmbg = None

    transaction.set_autocommit(False)
    try:
        # Pod pretpostavkom da smo ispravno sve validirali
        # mozemo unijeti ucenika
        ucenik= Ucenik(ime=ime, prezime=prezime, smjer=smjer,osnovna_skola=osnovna_skola)
        ucenik.save()

        if priznanje_bodovi:
            for i in range(len(priznanje_bodovi)):
                naziv=priznanja_naziv[i]
                bodovi=priznanje_bodovi[i]
                priznanje=Priznanja(naziv=naziv, bodovi=bodovi, ucenik_id=ucenik)
                priznanje.save()


        if Ucenik.objects.count()==0:
            ucenik_id=1

        # Pod pretpostavkom da smo validno unijeli sve ocjene za sve predmete
        # mozemo ispuniti diplomu
        razred6=Diploma(razred_id=6, razred_naziv="Šesti razred",ucenik_id=ucenik) # razred.razred_id = 6 (Diploma)
        razred7=Diploma(razred_id=7, razred_naziv="Sedmi razred",ucenik_id=ucenik) # razred.razred_id = 7 (Diploma)
        razred8=Diploma(razred_id=8, razred_naziv="Osmi razred",ucenik_id=ucenik) # razred.razred_id = 8 (Diploma)
        razred9=Diploma(razred_id=9, razred_naziv="Deveti razred",ucenik_id=ucenik) # razred.razred_id = 9 (Diploma)
        #if not razred9_per_predmet:

        razred6.save()
        razred7.save()
        razred8.save()
        razred9.save()
        # save all predmets in dictionary no need for hardcodin
        #d={'MM': 'Matematika', 'BJ':'Bosanski jezik i književnost',
        #  'IN':'Informatika'}
        d={}
        # Duplira predmet ne moze ovako
        for predmet in PredmetIspis.objects.filter(razred_id=6):
               d[predmet.kod]=predmet.naziv

        #svi_predmeti=Predmet.objects.all() # ovo ne moze, kupi zadnje ocjene
        lista_predmeta_6 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
        d={}
        # Duplira predmet ne moze ovako
        for predmet in PredmetIspis.objects.filter(razred_id=7):
               d[predmet.kod]=predmet.naziv
        lista_predmeta_7 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
        d={}
        # Duplira predmet ne moze ovako
        for predmet in PredmetIspis.objects.filter(razred_id=8):
               d[predmet.kod]=predmet.naziv
        lista_predmeta_8 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list
        d={}
        # Duplira predmet ne moze ovako
        for predmet in PredmetIspis.objects.filter(razred_id=9):
               d[predmet.kod]=predmet.naziv
        lista_predmeta_9 = Predmet.objects.bulk_create([Predmet(kod=key, naziv=d[key]) for key in d]) # already list

        for predmet in lista_predmeta_6:
            predmet.save()

        for predmet in lista_predmeta_7:
            predmet.save()

        for predmet in lista_predmeta_8:
            predmet.save()

        for predmet in lista_predmeta_9:
            predmet.save()
        #lista_predmeta=list(svi_predmeti) # not needed to convert (needed for objects.all() query_set)

        razred6.predmeti.add(*lista_predmeta_6)
        razred7.predmeti.add(*lista_predmeta_7)
        razred8.predmeti.add(*lista_predmeta_8)
        razred9.predmeti.add(*lista_predmeta_9)

        predmeti_razreda6=razred6.predmeti.all()
        predmeti_razreda7=razred7.predmeti.all()
        predmeti_razreda8=razred8.predmeti.all()
        predmeti_razreda9=razred9.predmeti.all()

        # Spasi ocjena za predmete razreda 6
        i=0
        for predmet in predmeti_razreda6:
            if (i==8): # ovo je informatika predmet, stavi zadnji element
                predmet.ocjena=razred6_per_predmet[len(razred6_per_predmet)-1]
                if predmet.ocjena:
                    predmet.save()
            elif(i<8):
                predmet.ocjena=razred6_per_predmet[i]
                if predmet.ocjena:
                    predmet.save()
            elif(i>8):
                predmet.ocjena=razred6_per_predmet[i-1]
                if predmet.ocjena:
                    predmet.save()
            i=i+1
        razred6.save()
        # Spasi ocjena za predmete razreda 7
        i=0
        for predmet in predmeti_razreda7:
            if (i==9): # ovo je informatika predmet, stavi zadnji element
                predmet.ocjena=razred7_per_predmet[len(razred7_per_predmet)-1]
                if predmet.ocjena:
                    predmet.save()
            elif(i<9):
                predmet.ocjena=razred7_per_predmet[i]
                if predmet.ocjena:
                    predmet.save()
            elif(i>9):
                predmet.ocjena=razred7_per_predmet[i-1]
                if predmet.ocjena:
                    predmet.save()
            i=i+1
        razred7.save()
        # Spasi ocjena za predmete razreda 8
        i=0
        for predmet in predmeti_razreda8:
                predmet.ocjena=razred8_per_predmet[i]
                if predmet.ocjena:
                    predmet.save()
                i=i+1
        razred8.save()
        # Spasi ocjena za predmete razreda 9
        i=0
        for predmet in predmeti_razreda9:
                predmet.ocjena=razred9_per_predmet[i]
                if predmet.ocjena:
                    predmet.save()
                i=i+1
        razred9.save()

        # Vrati se na home page
        return HttpResponseRedirect(reverse('tehnicka:index_base'))

    except:
        transaction.rollback()
        raise
    else:
        transaction.commit()
    finally:
        transaction.set_autocommit(True)


###############################################################################
#                   UPDATE- details                                           #
###############################################################################
def get_for_update(request, ucenik_id):
    ucenik=Ucenik.objects.get(id=ucenik_id)
    diplome=Diploma.objects.filter(ucenik_id=ucenik);
    sesti_predmeti=diplome[0].predmeti.all();
    sedmi_predmeti=diplome[1].predmeti.all();
    osmi_predmeti=diplome[2].predmeti.all();
    deveti_predmeti=diplome[3].predmeti.all();
    #fizika_7=diplome[1].predmeti.all()[4].ocjena
    #fizika_8=diplome[2].predmeti.all()[4].ocjena #hemija je 2/3 i 5
    context={
    'ucenik':ucenik,
    'sesti':sesti_predmeti,
    'sedmi':sedmi_predmeti,
    'osmi':osmi_predmeti,
    'deveti':deveti_predmeti,
    'smjerovi':Smjer.objects.all(),
    'priznanja':Priznanja.objects.filter(ucenik_id=ucenik)
    }
    if request.user.is_authenticated:
        return render(request, 'tehnicka/details.html',context)
    else:
        return render(request, "users/login.html", {"message": "Please log in."})

def updateStudent(request, ucenik_id):
    ime=request.POST["ime"]
    prezime=(request.POST["prezime"])
    osnovna_skola=(request.POST["osnovna_skola"])
    smjer_id=(request.POST["smjer"])
    smjer=Smjer.objects.get(id=smjer_id)

    razred6_ocjene=request.POST.getlist('razred6_ocjene')
    razred7_ocjene=request.POST.getlist('razred7_ocjene')
    razred8_ocjene=request.POST.getlist('razred8_ocjene')
    razred9_ocjene=request.POST.getlist('razred9_ocjene')

    priznanja_naziv=request.POST.getlist('priznanje_naziv')
    priznanje_bodovi=request.POST.getlist('priznanje_bodovi')
    vrsta_takmicenja=request.POST.getlist('vrsta_takmicenja')

    #return HttpResponse(razredi_ocjene)
    ucenik=Ucenik.objects.get(id=ucenik_id)
    diplome_qs=Diploma.objects.filter(ucenik_id=ucenik_id) # query_set -> not working
    #diplome_list=list(diplome_qs) #list -> not working
    i=0
    for razred in diplome_qs:
        predmeti_list= razred.predmeti.all() # predmeti is a list -> not working, also query_set
        j=0
        for predmet in predmeti_list: #Predmet query_set
            if i==0:
                razredi_ocjene=razred6_ocjene
            if i==1:
                razredi_ocjene=razred7_ocjene
            if i==2:
                razredi_ocjene=razred8_ocjene
            if i==3:
                razredi_ocjene=razred9_ocjene

            try:
                predmet.ocjena=int(razredi_ocjene[j])
            except ValueError:
                predmet.ocjena=None# # cast empty string
            j=j+1

            predmet.save()
        razred.save()
        i=i+1
    ucenik.ime=ime
    ucenik.prezime=prezime
    ucenik.smjer=smjer
    ucenik.osnovna_skola=osnovna_skola
    ucenik.save()
    i=0

    if priznanja_naziv:
        priznanje_ucenik=Priznanja.objects.filter(ucenik_id=ucenik)
        if not priznanje_ucenik: # Nema priznanja ime dugme add i mozemo dodati nova
            for k in range(len(priznanje_bodovi)):
                naziv=priznanja_naziv[k]
                bodovi=priznanje_bodovi[k]
                # tip=vrsta_takmicenja[k]
                priznanje=Priznanja(naziv=naziv, bodovi=bodovi, ucenik_id=ucenik)
                priznanje.save()

        else: # ima priznanja samo mijenjamo
            i=0
            for priznanje in priznanje_ucenik:
                #for i in range(len(priznanje_bodovi)):
                naziv=priznanja_naziv[i]
                bodovi=priznanje_bodovi[i]
                priznanje.naziv=naziv
                priznanje.bodovi=bodovi
                # priznanje.vrsta_takmicenja=tip
                priznanje.save()
                i=i+1

    return HttpResponseRedirect(reverse('tehnicka:index_base'))


###############################################################################
#                   DELETE- delete                                            #
###############################################################################
def deleteStudent(request, ucenik_id):
    ucenik=Ucenik.objects.filter(id=ucenik_id)
    smjer_id=ucenik[0].smjer.id
    ucenik.delete()
    request.session['message']="Obrisan korisnik"
    return HttpResponseRedirect(reverse('tehnicka:index', args=(smjer_id,)))


###############################################################################
#                   DELETE- brisipriznanje                                    #
###############################################################################
def deleteAcknowledgments(request, priznanje_id):
    try:
        ucenik_id=Priznanja.objects.get(id=priznanje_id).ucenik_id.id
        #return HttpResponseRedirect(reverse('tehnicka:details'), kwargs={'ucenik_id':ucenik_id})args=(p.id)
        priznanje=Priznanja.objects.get(id=priznanje_id).delete()
        request.session['message']="Obrisano priznanje"
        return HttpResponseRedirect(reverse('tehnicka:details', args=(ucenik_id,)))

    except KeyError:
        return HttpResponse("Key error - post uredi priznanje")
