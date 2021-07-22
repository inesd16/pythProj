#!/usr/bin/python

# -*- coding: utf-8 -*-

import json
import urllib3
from flask import Flask, request, render_template, redirect, url_for



import json
import urllib3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__, static_folder='static')  # Instancie une nouvelle application


@app.route('/api/tracking', methods=['GET', 'POST'])


def verifiedClient():
    print("Appel /api/tracking")
    if request.method == 'GET':
        print("Methode GET")
        return render_template("1_verif_numerocolis.html",
                               agrikolis_suivi=url_for('static', filename='agrikolis_suivi.svg'))

    if request.method == 'POST':

        print("Methode POST")
        trackingNumber = str(request.form.get("TrackingNumber"))  # Numero de suivi du consommateur

        # URL a changer lorsque la methode sera mise en prod
        url = "https://middlewarepreprod.misyl.net/api/chatbot/known?trackingNumber=" + trackingNumber
        https = urllib3.PoolManager()

        response = https.request('GET', url)

        fileKnow = json.loads(response.data)

        # with open('/var/www/api_suivi_prod/data/know.json', 'w') as f:
        with open('data/know.json', 'w') as f:
            json.dump(fileKnow, f)
        # know_file = json.loads(open('/var/www/api_suivi_prod/data/know.json', 'rb').read())
        know_file = json.loads(open('data/know.json', 'rb').read())

        IsColisinDatabase = know_file['data']['isColisInDatabase']

        if IsColisinDatabase == True:
            print("is colis in database = true")
            return redirect(url_for('dataClient', TrackingNumber=trackingNumber))

        else:
            print("is colis in database = false")
            return render_template("9_error_numerocolis.html",
                                   agrikolis_suivi=url_for('static', filename="agrikolis_suivi.svg"))


@app.route('/api/tracking/<TrackingNumber>', methods=['GET', 'POST'])
def dataClient(TrackingNumber):
    customerEmail = str(request.form.get('EmailUser'))  # Email utilisateur

    # URL a changer lorsque la methode sera mise en prod
    url = "https://middlewarepreprod.misyl.net/api/chatbot/colis?trackingNumber=" + TrackingNumber + "&email=" + \
          customerEmail
    https = urllib3.PoolManager()

    response = https.request('GET', url)
    fileKolis = json.loads(response.data)

    with open('data/kolis.json', 'w') as fout:
    # with open('/var/www/api_suivi_prod/data/kolis.json', 'w') as fout:
        json.dump(fileKolis, fout)

    if request.method == "GET":
        return render_template("2_verif_email.html",
                               agrikolis_colis_trouve=url_for('static', filename='agrikolis_colis_trouve.svg'))

    if request.method == 'POST':

        # ApiKolis(TrackingNumber, customerEmail)

        kolis_file = json.loads(open('data/kolis.json', 'rb').read())

        # Test si l'email de l'utilisateur est connu
        if kolis_file['status'] == 500:  # Email pas correct
            return render_template("10_error_mail.html",
                                   agrikolis_colis_trouve=url_for('static', filename='agrikolis_colis_trouve.svg'))

        elif kolis_file['status'] == 204:  # Aucune donnee concernant le colis
            return render_template("10_error_mail.html",
                                   agrikolis_colis_trouve=url_for('static', filename='agrikolis_colis_trouve.svg'))

        elif kolis_file['status'] == 200:  # Aucun probleme detecte

            # Recupere toutes les informations necessaires sur le colis du consommateur
            status = int(kolis_file['data']['data']['status'])
            meetingLink = kolis_file['data']['data']['meetingLink']
            meetingDateTime = kolis_file['data']['data']['meetingDatetime']
            productWidth = kolis_file['data']['data']['productWidth']
            productHeight = kolis_file['data']['data']['productHeight']
            productWeight = kolis_file['data']['data']['productWeight']
            relayMaps = kolis_file['data']['data']['relayMaps']
            productLength = kolis_file['data']['data']['productLength']
            productVolume = kolis_file['data']['data']['productVolume']
            relayAddress = kolis_file['data']['data']['relayAddress']
            relayName = kolis_file['data']['data']['relayName']
            productDescription = kolis_file['data']['data']['productDescription']

            # Code pour des variables pas encore presentent dans middleware

            # estimatedDate = kolis_file['data']['data']['estimatedDate']
            # receiptDate = kolis_file['data']['data']['receiptData']
            # deliveryData = kolis_file['data']['data']['deliveryDate']
            # actualHour = kolis_file['data']['data']['now']
            # mondayMorning = kolis_file['data']['calendarOpening']['monday']['plage1']
            # mondayAfternoon = kolis_file['data']['calendarOpening']['monday']['plage2']
            # tuesdayMorning = kolis_file['data']['calendarOpening']['tuesday']['plage1']
            # tuesdayAfternoon = kolis_file['data']['calendarOpening']['tuesday']['plage2']
            # wednesdayMorning = kolis_file['data']['calendarOpening']['wednesday']['plage1']
            # wednesdayAfternoon = kolis_file['data']['calendarOpening']['wednesday']['plage2']
            # thursdayMorning = kolis_file['data']['calendarOpening']['thursday']['plage1']
            # thursdayAfternoon = kolis_file['data']['calendarOpening']['thursday']['plage2']
            # fridayMorning = kolis_file['data']['calendarOpening']['friday']['plage1']
            # firdayAfternoon = kolis_file['data']['calendarOpening']['friday']['plage2']
            # saturdayMorning = kolis_file['data']['calendarOpening']['saturday']['plage1']
            # saturdayAfternoon = kolis_file['data']['calendarOpening']['saturday']['plage2']
            # sundayMorning = kolis_file['data']['calendarOpening']['sunday']['plage1']
            # sundayAfternoon = kolis_file['data']['calendarOpening']['sunday']['plage2']

            horaires = {
                "calendarOpening": {
                    "monday": {
                        "plage1": "10:00 - 12:00",
                        "plage2": "14:00 - 17:00"
                    },
                    "thursday": {
                        "plage1": None,
                        "plage2": "14:00 - 17:00"
                    },
                    "wednesday": {
                        "plage1": "10:00 - 12:00",
                        "plage2": None
                    },
                    "tuesday": {
                        "plage1": None,
                        "plage2": None
                    },
                    "friday": {
                        "plage1": None,
                        "plage2": None
                    },
                    "saturday": {
                        "plage1": None,
                        "plage2": "14:00 - 17:00"
                    },
                    "sunday": {
                        "plage1": None,
                        "plage2": "14:00 - 17:00"
                    }
                }
            }

            json.dumps(horaires)

            historic_status1 = "Votre colis est en cours d'acheminement"
            historic_status2 = "Votre colis est disponible dans votre relais. Prenez un rdv!"
            historic_status3 = "Vous avez un rendez-vous de fixe :-)"
            historic_status4 = "Votre colis vous a ete remis :)"
            historic_status5 = "Votre colis a ete abime sur le relais... Contacter le support"
            historic_status6 = "Votre colis a demande a etre retourne"
            historic_status7 = "Votre colis est actuellement en retour"
            historic_status8 = "Votre colis a rencontre un probleme. Merci de contacter le support"

            # Colis en attente de reception
            if status == 1:
                return render_template("3_acheminementencours.html",
                                       trackingNumber=TrackingNumber,
                                       relayAddress=relayAddress,
                                       relayName=relayName,
                                       relayMaps=relayMaps,
                                       historic=historic_status1,
                                       productHeight=productHeight,
                                       productLength=productLength,
                                       productDescription=productDescription,
                                       productVolume=productVolume,
                                       productWidth=productWidth,
                                       productWeight=productWeight,
                                       status=kolis_file['status'],
                                       goh=url_for('static', filename="goh.svg"),
                                       gom=url_for('static', filename="gom.svg"),
                                       acheminement=url_for('static', filename="acheminement.svg"),
                                       monday_morning="Ferme" if horaires['calendarOpening']['monday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage1'],
                                       monday_afternoon="Ferme" if horaires['calendarOpening']['monday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage2'],
                                       tuesday_morning="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                      'plage1'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage1'],
                                       tuesday_afternoon="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                        'plage2'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage2'],
                                       wednesday_morning="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                        'plage1'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage1'],
                                       wednesday_afternoon="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                          'plage2'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage2'],
                                       thursday_morning="Ferme" if horaires['calendarOpening']['thursday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage1'],
                                       thursday_afternoon="Ferme" if horaires['calendarOpening']['thursday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage2'],
                                       friday_morning="Ferme" if horaires['calendarOpening']['friday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage1'],
                                       friday_afternoon="Ferme" if horaires['calendarOpening']['friday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage2'],
                                       saturday_morning="Ferme" if horaires['calendarOpening']['saturday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage1'],
                                       saturday_afternoon="Ferme" if horaires['calendarOpening']['saturday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage2'],
                                       sunday_morning="Ferme" if horaires['calendarOpening']['sunday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage1'],
                                       sunday_afternoon="Ferme" if horaires['calendarOpening']['sunday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage2'])


            # Colis receptionne mais pas de rendez-vous
            elif status == 2:
                return render_template("4_disponibleenpointrelais.html",
                                       trackingNumber=TrackingNumber,
                                       meetingLink=meetingLink,
                                       relayAddress=relayAddress,
                                       relayName=relayName,
                                       historic=historic_status2,
                                       relayMaps=relayMaps,
                                       meetingDateTime=meetingDateTime,
                                       productHeight=productHeight,
                                       productLength=productLength,
                                       productDescription=productDescription,
                                       productVolume=productVolume,
                                       productWidth=productWidth,
                                       productWeight=productWeight,
                                       status=kolis_file['status'],
                                       goh=url_for('static', filename="goh.svg"),
                                       gom=url_for('static', filename="gom.svg"),
                                       disporelais=url_for('static', filename='disporelais.svg'),
                                       valide=url_for('static', filename='valide.svg'),
                                       monday_morning="Ferme" if horaires['calendarOpening']['monday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage1'],
                                       monday_afternoon="Ferme" if horaires['calendarOpening']['monday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage2'],
                                       tuesday_morning="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                      'plage1'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage1'],
                                       tuesday_afternoon="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                        'plage2'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage2'],
                                       wednesday_morning="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                        'plage1'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage1'],
                                       wednesday_afternoon="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                          'plage2'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage2'],
                                       thursday_morning="Ferme" if horaires['calendarOpening']['thursday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage1'],
                                       thursday_afternoon="Ferme" if horaires['calendarOpening']['thursday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage2'],
                                       friday_morning="Ferme" if horaires['calendarOpening']['friday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage1'],
                                       friday_afternoon="Ferme" if horaires['calendarOpening']['friday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage2'],
                                       saturday_morning="Ferme" if horaires['calendarOpening']['saturday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage1'],
                                       saturday_afternoon="Ferme" if horaires['calendarOpening']['saturday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage2'],
                                       sunday_morning="Ferme" if horaires['calendarOpening']['sunday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage1'],
                                       sunday_afternoon="Ferme" if horaires['calendarOpening']['sunday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage2'])



            # Colis recpetionne et rdv fixe
            elif status == 3:
                return render_template("6_rdvvalide.html",
                                       trackingNumber=TrackingNumber,
                                       meetingLink=meetingLink,
                                       meetingDateTime=meetingDateTime,
                                       relayAddress=relayAddress,
                                       relayName=relayName,
                                       relayMaps=relayMaps,
                                       productHeight=productHeight,
                                       productLength=productLength,
                                       productDescription=productDescription,
                                       productVolume=productVolume,
                                       productWidth=productWidth,
                                       productWeight=productWeight,
                                       historic=historic_status3,
                                       status=kolis_file['status'],
                                       goh=url_for('static', filename="goh.svg"),
                                       gom=url_for('static', filename="gom.svg"),
                                       rdvok=url_for('static', filename='rdvok.svg'),
                                       valide=url_for('static', filename='valide.svg'),
                                       image_meetingfixed=url_for('static', filename='meeting_fixed.png'),
                                       monday_morning="Ferme" if horaires['calendarOpening']['monday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage1'],
                                       monday_afternoon="Ferme" if horaires['calendarOpening']['monday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage2'],
                                       tuesday_morning="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                      'plage1'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage1'],
                                       tuesday_afternoon="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                        'plage2'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage2'],
                                       wednesday_morning="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                        'plage1'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage1'],
                                       wednesday_afternoon="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                          'plage2'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage2'],
                                       thursday_morning="Ferme" if horaires['calendarOpening']['thursday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage1'],
                                       thursday_afternoon="Ferme" if horaires['calendarOpening']['thursday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage2'],
                                       friday_morning="Ferme" if horaires['calendarOpening']['friday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage1'],
                                       friday_afternoon="Ferme" if horaires['calendarOpening']['friday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage2'],
                                       saturday_morning="Ferme" if horaires['calendarOpening']['saturday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage1'],
                                       saturday_afternoon="Ferme" if horaires['calendarOpening']['saturday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage2'],
                                       sunday_morning="Ferme" if horaires['calendarOpening']['sunday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage1'],
                                       sunday_afternoon="Ferme" if horaires['calendarOpening']['sunday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage2'])

            # Colis deja remis au client
            elif status == 4:
                return render_template("7_colislivre.html",
                                       trackingNumber=TrackingNumber,
                                       status=kolis_file['status'],
                                       relayAddress=relayAddress,
                                       relayName=relayName,
                                       relayMaps=relayMaps,
                                       productHeight=productHeight,
                                       productLength=productLength,
                                       productDescription=productDescription,
                                       productVolume=productVolume,
                                       productWidth=productWidth,
                                       productWeight=productWeight,
                                       historic=historic_status4,
                                       goh=url_for('static', filename="goh.svg"),
                                       gom=url_for('static', filename="gom.svg"),
                                       valide=url_for('static', filename='valide.svg'),
                                       image_delivered=url_for('static', filename='delivered.png'),
                                       monday_morning="Ferme" if horaires['calendarOpening']['monday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage1'],
                                       monday_afternoon="Ferme" if horaires['calendarOpening']['monday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage2'],
                                       tuesday_morning="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                      'plage1'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage1'],
                                       tuesday_afternoon="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                        'plage2'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage2'],
                                       wednesday_morning="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                        'plage1'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage1'],
                                       wednesday_afternoon="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                          'plage2'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage2'],
                                       thursday_morning="Ferme" if horaires['calendarOpening']['thursday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage1'],
                                       thursday_afternoon="Ferme" if horaires['calendarOpening']['thursday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage2'],
                                       friday_morning="Ferme" if horaires['calendarOpening']['friday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage1'],
                                       friday_afternoon="Ferme" if horaires['calendarOpening']['friday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage2'],
                                       saturday_morning="Ferme" if horaires['calendarOpening']['saturday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage1'],
                                       saturday_afternoon="Ferme" if horaires['calendarOpening']['saturday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage2'],
                                       sunday_morning="Ferme" if horaires['calendarOpening']['sunday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage1'],
                                       sunday_afternoon="Ferme" if horaires['calendarOpening']['sunday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage2'])
            elif status == 5:
                return render_template("8_commandeannulee.html",
                                       trackingNumber=TrackingNumber,
                                       status=kolis_file['status'],
                                       relayAddress=relayAddress,
                                       relayName=relayName,
                                       relayMaps=relayMaps,
                                       productHeight=productHeight,
                                       productLength=productLength,
                                       productDescription=productDescription,
                                       productVolume=productVolume,
                                       productWidth=productWidth,
                                       productWeight=productWeight,
                                       historic=historic_status5,
                                       goh=url_for('static', filename="goh.svg"),
                                       gom=url_for('static', filename="gom.svg"),
                                       valide=url_for('static', filename='valide.svg'),
                                       no=url_for('static', filename='no.svg'),
                                       monday_morning="Ferme" if horaires['calendarOpening']['monday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage1'],
                                       monday_afternoon="Ferme" if horaires['calendarOpening']['monday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage2'],
                                       tuesday_morning="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                      'plage1'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage1'],
                                       tuesday_afternoon="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                        'plage2'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage2'],
                                       wednesday_morning="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                        'plage1'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage1'],
                                       wednesday_afternoon="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                          'plage2'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage2'],
                                       thursday_morning="Ferme" if horaires['calendarOpening']['thursday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage1'],
                                       thursday_afternoon="Ferme" if horaires['calendarOpening']['thursday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage2'],
                                       friday_morning="Ferme" if horaires['calendarOpening']['friday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage1'],
                                       friday_afternoon="Ferme" if horaires['calendarOpening']['friday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage2'],
                                       saturday_morning="Ferme" if horaires['calendarOpening']['saturday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage1'],
                                       saturday_afternoon="Ferme" if horaires['calendarOpening']['saturday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage2'],
                                       sunday_morning="Ferme" if horaires['calendarOpening']['sunday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage1'],
                                       sunday_afternoon="Ferme" if horaires['calendarOpening']['sunday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage2'])

            elif status == 6:
                return render_template("8_commandeannulee.html",
                                       trackingNumber=TrackingNumber,
                                       status=kolis_file['status'],
                                       relayAddress=relayAddress,
                                       relayName=relayName,
                                       relayMaps=relayMaps,
                                       productHeight=productHeight,
                                       productLength=productLength,
                                       productDescription=productDescription,
                                       productVolume=productVolume,
                                       productWidth=productWidth,
                                       productWeight=productWeight,
                                       historic=historic_status6,
                                       goh=url_for('static', filename="goh.svg"),
                                       gom=url_for('static', filename="gom.svg"),
                                       valide=url_for('static', filename='valide.svg'),
                                       no=url_for('static', filename='no.svg'),
                                       monday_morning="Ferme" if horaires['calendarOpening']['monday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage1'],
                                       monday_afternoon="Ferme" if horaires['calendarOpening']['monday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage2'],
                                       tuesday_morning="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                      'plage1'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage1'],
                                       tuesday_afternoon="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                        'plage2'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage2'],
                                       wednesday_morning="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                        'plage1'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage1'],
                                       wednesday_afternoon="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                          'plage2'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage2'],
                                       thursday_morning="Ferme" if horaires['calendarOpening']['thursday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage1'],
                                       thursday_afternoon="Ferme" if horaires['calendarOpening']['thursday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage2'],
                                       friday_morning="Ferme" if horaires['calendarOpening']['friday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage1'],
                                       friday_afternoon="Ferme" if horaires['calendarOpening']['friday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage2'],
                                       saturday_morning="Ferme" if horaires['calendarOpening']['saturday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage1'],
                                       saturday_afternoon="Ferme" if horaires['calendarOpening']['saturday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage2'],
                                       sunday_morning="Ferme" if horaires['calendarOpening']['sunday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage1'],
                                       sunday_afternoon="Ferme" if horaires['calendarOpening']['sunday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage2'])

            elif status == 7:
                return render_template("8_commandeannulee.html",
                                       trackingNumber=TrackingNumber,
                                       status=kolis_file['status'],
                                       relayAddress=relayAddress,
                                       relayName=relayName,
                                       relayMaps=relayMaps,
                                       productHeight=productHeight,
                                       productLength=productLength,
                                       productDescription=productDescription,
                                       productVolume=productVolume,
                                       productWidth=productWidth,
                                       productWeight=productWeight,
                                       historic=historic_status7,
                                       goh=url_for('static', filename="goh.svg"),
                                       gom=url_for('static', filename="gom.svg"),
                                       valide=url_for('static', filename='valide.svg'),
                                       no=url_for('static', filename='no.svg'),
                                       monday_morning="Ferme" if horaires['calendarOpening']['monday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage1'],
                                       monday_afternoon="Ferme" if horaires['calendarOpening']['monday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage2'],
                                       tuesday_morning="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                      'plage1'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage1'],
                                       tuesday_afternoon="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                        'plage2'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage2'],
                                       wednesday_morning="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                        'plage1'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage1'],
                                       wednesday_afternoon="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                          'plage2'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage2'],
                                       thursday_morning="Ferme" if horaires['calendarOpening']['thursday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage1'],
                                       thursday_afternoon="Ferme" if horaires['calendarOpening']['thursday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage2'],
                                       friday_morning="Ferme" if horaires['calendarOpening']['friday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage1'],
                                       friday_afternoon="Ferme" if horaires['calendarOpening']['friday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage2'],
                                       saturday_morning="Ferme" if horaires['calendarOpening']['saturday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage1'],
                                       saturday_afternoon="Ferme" if horaires['calendarOpening']['saturday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage2'],
                                       sunday_morning="Ferme" if horaires['calendarOpening']['sunday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage1'],
                                       sunday_afternoon="Ferme" if horaires['calendarOpening']['sunday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage2'])



            # Colis annule
            elif status > 7:
                return render_template("8_commandeannulee.html",
                                       trackingNumber=TrackingNumber,
                                       relayAddress=relayAddress,
                                       relayName=relayName,
                                       relayMaps=relayMaps,
                                       productHeight=productHeight,
                                       productLength=productLength,
                                       productDescription=productDescription,
                                       productVolume=productVolume,
                                       productWidth=productWidth,
                                       productWeight=productWeight,
                                       historic=historic_status8,
                                       status=kolis_file['status'],
                                       goh=url_for('static', filename="goh.svg"),
                                       gom=url_for('static', filename="gom.svg"),
                                       valide=url_for('static', filename='valide.svg'),
                                       no=url_for('static', filename='no.svg'),
                                       monday_morning="Ferme" if horaires['calendarOpening']['monday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage1'],
                                       monday_afternoon="Ferme" if horaires['calendarOpening']['monday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['monday'][
                                           'plage2'],
                                       tuesday_morning="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                      'plage1'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage1'],
                                       tuesday_afternoon="Ferme" if horaires['calendarOpening']['tuesday'][
                                                                        'plage2'] is None else
                                       horaires['calendarOpening']['tuesday'][
                                           'plage2'],
                                       wednesday_morning="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                        'plage1'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage1'],
                                       wednesday_afternoon="Ferme" if horaires['calendarOpening']['wednesday'][
                                                                          'plage2'] is None else
                                       horaires['calendarOpening']['wednesday'][
                                           'plage2'],
                                       thursday_morning="Ferme" if horaires['calendarOpening']['thursday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage1'],
                                       thursday_afternoon="Ferme" if horaires['calendarOpening']['thursday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['thursday'][
                                           'plage2'],
                                       friday_morning="Ferme" if horaires['calendarOpening']['friday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage1'],
                                       friday_afternoon="Ferme" if horaires['calendarOpening']['friday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['friday'][
                                           'plage2'],
                                       saturday_morning="Ferme" if horaires['calendarOpening']['saturday'][
                                                                       'plage1'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage1'],
                                       saturday_afternoon="Ferme" if horaires['calendarOpening']['saturday'][
                                                                         'plage2'] is None else
                                       horaires['calendarOpening']['saturday'][
                                           'plage2'],
                                       sunday_morning="Ferme" if horaires['calendarOpening']['sunday'][
                                                                     'plage1'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage1'],
                                       sunday_afternoon="Ferme" if horaires['calendarOpening']['sunday'][
                                                                       'plage2'] is None else
                                       horaires['calendarOpening']['sunday'][
                                           'plage2'])

    else:
        return redirect(url_for('verifiedClient'))


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
