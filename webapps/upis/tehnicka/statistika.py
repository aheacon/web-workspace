from tehnicka.models import Ucenik, Smjer, Predmet, Diploma, PredmetIspis, Priznanja
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
import sys

import logging


def racunajStatistiku(request, smjer_id, message):

    logger = logging.getLogger(__name__)

    # Put the logging info within your django view
    logger.info("Simple info")
    posebni_bodovi={}
    prosjek_6={}
    prosjek_7={}
    prosjek_8={}
    prosjek_9={}

    prosjek_ukupno=0
    posebni_predmet_ukupno=0
    posebni_predmet_1_ocjena_razred9=0
    posebni_predmet_2_ocjena_razred9=0
    posebni_predmet_3_ocjena_razred7=0
    UKUPNO=0
    posebni_predmet_1_ocjena_razred8=posebni_predmet_1_ocjena_razred9
    posebni_predmet_2_ocjena_razred8=posebni_predmet_2_ocjena_razred9
    posebni_predmet_3_ocjena_razred6=posebni_predmet_3_ocjena_razred7

    posebni_predmet_1=""
    posebni_predmet_2=posebni_predmet_1
    posebni_predmet_3=posebni_predmet_1

    # Dictionaries
    posebni_predmet_1_ocjena_razred8_dict={}
    posebni_predmet_1_ocjena_razred9_dict={}
    posebni_predmet_2_ocjena_razred8_dict={}
    posebni_predmet_2_ocjena_razred9_dict={}
    posebni_predmet_3_ocjena_razred6_dict={}
    posebni_predmet_3_ocjena_razred7_dict={}
    prosjek_ukupno_dict={}

    prosjek_6_dict={}
    prosjek_7_dict={}
    prosjek_8_dict={}
    prosjek_9_dict={}
    posebni_bodovi_dict={}
    ukupno_dict={}

    # Pokupi bodove sa priznanja
    priznanje_opcinsko_dict={} # @todo
    priznanje_kantonalno_dict={}
    priznanje_federalno_dict={}

    # =============== Racunanje statistike ===============
    for ucenik in Ucenik.objects.filter(smjer=smjer_id):
        s=0 # prosjek po razredu laznjak -> brisi

        for razred in Diploma.objects.filter(ucenik_id=ucenik):
            p=0 # broj predmeta
            p2=0
            s1=0 # prosjek po razredu
            for predmet in razred.predmeti.all():
                if predmet.ocjena == None:
                    print("do nothing")
                    p2=p2+1
                else:
                    p=p+1
                    print(predmet.naziv)
                    print(p)
                    s1=s1+predmet.ocjena
                # Handling posebni_bodovi na predmete automatika/arhitekture/energetike
                if(ucenik.smjer.kod == 'AUT' or ucenik.smjer.kod == 'ARH' or ucenik.smjer.kod == 'EL'):
                    posebni_predmet_1="Matematika"
                    posebni_predmet_2="Fizika"
                    posebni_predmet_3="Informatika"

                    # RACUNAJ POJEDINACNE BODOVE NA POSEBNE PREDMETE
                    if predmet.ocjena !=None:
                        if predmet.kod=='MM' and razred.razred_id==8:
                            posebni_predmet_1_ocjena_razred8=predmet.ocjena
                        elif predmet.kod=='MM' and razred.razred_id==9:
                            posebni_predmet_1_ocjena_razred9=predmet.ocjena
                        elif predmet.kod=='FI' and razred.razred_id==8:
                            posebni_predmet_2_ocjena_razred8=predmet.ocjena
                        elif predmet.kod=='FI' and razred.razred_id==9:
                            posebni_predmet_2_ocjena_razred9=predmet.ocjena
                        elif predmet.kod=='IN' and razred.razred_id==6:
                            posebni_predmet_3_ocjena_razred6=predmet.ocjena
                        elif predmet.kod=='IN' and razred.razred_id==7:
                            posebni_predmet_3_ocjena_razred7=predmet.ocjena

                # Handling posebni_bodovi na predmete masinci/metalurzi
                if(ucenik.smjer.kod == 'MAS' or ucenik.smjer.kod == 'ME'):
                    posebni_predmet_1="Matematika"
                    posebni_predmet_2="Fizika"
                    posebni_predmet_3="Tehnička kultura"

                    # RACUNAJ POJEDINACNE BODOVE NA POSEBNE PREDMETE
                    if predmet.ocjena !=None:
                        if predmet.kod=='MM' and razred.razred_id==8:
                            posebni_predmet_1_ocjena_razred8=predmet.ocjena
                        elif predmet.kod=='MM' and razred.razred_id==9:
                            posebni_predmet_1_ocjena_razred9=predmet.ocjena
                        elif predmet.kod=='FI' and razred.razred_id==8:
                            posebni_predmet_2_ocjena_razred8=predmet.ocjena
                        elif predmet.kod=='FI' and razred.razred_id==9:
                            posebni_predmet_2_ocjena_razred9=predmet.ocjena
                        elif predmet.kod=='TK' and razred.razred_id==6:
                            posebni_predmet_3_ocjena_razred6=predmet.ocjena
                        elif predmet.kod=='TK' and razred.razred_id==7:
                            posebni_predmet_3_ocjena_razred7=predmet.ocjena


                # Handling posebni_bodovi na predmete tehnicar drumskog saobracaja
                if(ucenik.smjer.kod == 'TDS'):
                    posebni_predmet_1="Matematika"
                    posebni_predmet_2="Fizika"
                    posebni_predmet_3="Geografija"

                    # RACUNAJ POJEDINACNE BODOVE NA POSEBNE PREDMETE
                    if predmet.ocjena !=None:
                        if predmet.kod=='MM' and razred.razred_id==8:
                            posebni_predmet_1_ocjena_razred8=predmet.ocjena
                        elif predmet.kod=='MM' and razred.razred_id==9:
                            posebni_predmet_1_ocjena_razred9=predmet.ocjena
                        elif predmet.kod=='FI' and razred.razred_id==8:
                            posebni_predmet_2_ocjena_razred8=predmet.ocjena
                        elif predmet.kod=='FI' and razred.razred_id==9:
                            posebni_predmet_2_ocjena_razred9=predmet.ocjena
                        elif predmet.kod=='GE' and razred.razred_id==6:
                            posebni_predmet_3_ocjena_razred6=predmet.ocjena
                        elif predmet.kod=='GE' and razred.razred_id==7:
                            posebni_predmet_3_ocjena_razred7=predmet.ocjena

                # else: # ocjena is None
                #     return HttpResponse(predmet.naziv)

            # Racunaj prosjek po razredima za svakog ucenika
            if(razred.razred_id==6):
                prosjek_6=round(s1/p,2) # round(x,2) float("{0:.2f}".format(x))

            if(razred.razred_id==7):
                prosjek_7=round(s1/p,2)
            if(razred.razred_id==8):
                prosjek_8=round(s1/p,2)
            if(razred.razred_id==9):
                #return HttpResponse(p2)
                prosjek_9=round(s1/p,2)

        # Pokupi zakljucne ocjene na 2 decimale i ukupnu prosjecnu ocjenu
        prosjek_6_dict[ucenik.id]=prosjek_6
        prosjek_7_dict[ucenik.id]=prosjek_7
        prosjek_8_dict[ucenik.id]=prosjek_8
        prosjek_9_dict[ucenik.id]=prosjek_9
        prosjek_ukupno_dict[ucenik.id]=round((prosjek_6+prosjek_7+prosjek_8+prosjek_9)*3,2)

        # Pokupi ocjene iz posebnih predmeta i ukupnu ocjenu
        posebni_predmet_1_ocjena_razred8_dict[ucenik.id]=posebni_predmet_1_ocjena_razred8
        posebni_predmet_1_ocjena_razred9_dict[ucenik.id]=posebni_predmet_1_ocjena_razred9
        posebni_predmet_2_ocjena_razred8_dict[ucenik.id]=posebni_predmet_2_ocjena_razred8
        posebni_predmet_2_ocjena_razred9_dict[ucenik.id]=posebni_predmet_2_ocjena_razred9
        posebni_predmet_3_ocjena_razred6_dict[ucenik.id]=posebni_predmet_3_ocjena_razred6
        posebni_predmet_3_ocjena_razred7_dict[ucenik.id]=posebni_predmet_3_ocjena_razred7
        #posebni_bodovi_suma
        posebni_bodovi_dict[ucenik.id]= posebni_predmet_1_ocjena_razred8 + posebni_predmet_1_ocjena_razred9+\
        posebni_predmet_2_ocjena_razred8+posebni_predmet_2_ocjena_razred9+\
        posebni_predmet_3_ocjena_razred6+posebni_predmet_3_ocjena_razred7

        priznanja=Priznanja.objects.filter(ucenik_id=ucenik)
        if not priznanja:
            priznanje_opcinsko_dict[ucenik.id]=0
            priznanje_kantonalno_dict[ucenik.id]=0
            priznanje_federalno_dict[ucenik.id]=0
        else:
            s_o=0
            for p in priznanja:
                s_o=s_o+p.bodovi
            priznanje_opcinsko_dict[ucenik.id]=s_o # {{ key }} - {{ value.i }}<
            priznanje_kantonalno_dict[ucenik.id]=0
            priznanje_federalno_dict[ucenik.id]=0

        ukupno_dict[ucenik.id]=round(prosjek_ukupno_dict[ucenik.id]+\
        posebni_bodovi_dict[ucenik.id]+\
        priznanje_opcinsko_dict[ucenik.id]+priznanje_kantonalno_dict[ucenik.id]+\
        priznanje_federalno_dict[ucenik.id], 2)

    #return HttpResponse(json.dumps( bodovi ))

    # =============== Prikazivanje statistike ===============

    context={
    'ucenici':Ucenik.objects.filter(smjer=smjer_id),     # 'smjerovi':Smjer.objects.all(),
    'posebni_predmet_1':posebni_predmet_1,
    'posebni_predmet_2':posebni_predmet_2,
    'posebni_predmet_3':posebni_predmet_3,

    'prosjek_6':prosjek_6_dict,
    'prosjek_7':prosjek_7_dict,
    'prosjek_8':prosjek_8_dict,
    'prosjek_9':prosjek_9_dict,

    'prosjek_ukupno':prosjek_ukupno_dict, # mnozi se sa 3

    'posebni_predmet_1_ocjena_razred8':posebni_predmet_1_ocjena_razred8_dict,
    'posebni_predmet_1_ocjena_razred9':posebni_predmet_1_ocjena_razred9_dict,
    'posebni_predmet_2_ocjena_razred8':posebni_predmet_2_ocjena_razred8_dict,
    'posebni_predmet_2_ocjena_razred9':posebni_predmet_2_ocjena_razred9_dict,
    'posebni_predmet_3_ocjena_razred6':posebni_predmet_3_ocjena_razred6_dict,
    'posebni_predmet_3_ocjena_razred7':posebni_predmet_3_ocjena_razred7_dict,

    'posebni_predmet_ukupno':posebni_bodovi_dict,

    'priznanje_opcinsko':priznanje_opcinsko_dict,
    'priznanje_kantonalno':priznanje_kantonalno_dict,
    'priznanje_federalno':priznanje_federalno_dict,

    'ukupno':ukupno_dict,

    'message':message
    }
    #if request.user.is_authenticated:
    return render(request, 'tehnicka/index.html',context)
