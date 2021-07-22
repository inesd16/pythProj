# coding=utf-8
import json
import urllib3
from flask import Flask, request, render_template, redirect, url_for
from time import strftime
from datetime import datetime

app = Flask(__name__, static_folder='static')  # Instancie une nouvelle application


@app.route('/tracking', methods=['GET', 'POST'])
def verifiedClient():  # Premiere fonction
    if request.method == 'GET':  # affichage de la première page
        return render_template("1_verif_numerocolis.html",
                               agrikolis_suivi=url_for('static', filename='agrikolis_suivi.svg'))

    if request.method == 'POST':

        trackingNumber = str(request.form.get("TrackingNumber"))  # Numero de suivi du consommateur

        # URL a changer lorsque la methode sera mise en prod
        url = "https://middleware.misyl.net/api/chatbot/known?trackingNumber=" + trackingNumber
        https = urllib3.PoolManager()

        response = https.request('GET', url)

        fileKnow = json.loads(response.data)

        with open('data/know.json', 'w') as f:
            json.dump(fileKnow, f)

        know_file = json.loads(open('data/know.json', 'rb').read())

        IsColisinDatabase = know_file['data']['isColisInDatabase']

        if IsColisinDatabase == True:  # direction vers la second fonction
            return redirect(url_for('dataClient', TrackingNumber=trackingNumber))

        else:  # gestion d'erreur
            return render_template("9_error_numerocolis.html",
                                   agrikolis_suivi=url_for('static', filename="agrikolis_suivi.svg"))


@app.route('/tracking/<TrackingNumber>', methods=['GET', 'POST'])
def dataClient(TrackingNumber):
    customerEmail = str(request.form.get('EmailUser'))  # Email utilisateur

    # URL a changer lorsque la methode sera mise en prod
    url = "https://middleware.misyl.net/api/chatbot/colis?trackingNumber=" + TrackingNumber + "&email=" + \
          customerEmail
    https = urllib3.PoolManager()

    response = https.request('GET', url)
    fileKolis = json.loads(response.data)

    with open('data/kolis.json', 'w') as fout:
        json.dump(fileKolis, fout)

    if request.method == "GET":  # seconde page
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
            global historical, name
            # Recupere toutes les informations necessaires sur le colis du consommateur
            status = int(kolis_file['data']['data']['status'])
            meetingDateTime = list(kolis_file['data']['data']['meetingDatetime'])
            meetingLink = kolis_file['data']['data']['meetingLink']
            productWidth = kolis_file['data']['data']['productWidth']
            productHeight = kolis_file['data']['data']['productHeight']
            productWeight = kolis_file['data']['data']['productWeight']
            relayMaps = kolis_file['data']['data']['relayMaps']
            productLength = kolis_file['data']['data']['productLength']
            productVolume = kolis_file['data']['data']['productVolume']
            relayAddress = kolis_file['data']['data']['relayAddress']
            relayName = kolis_file['data']['data']['relayName']
            productDescription = kolis_file['data']['data']['productDescription']
            now = datetime.now()
            dateHoraire = now.strftime("%d/%m/%Y")
            mdt = 0

            openings = kolis_file['data']['data']['calendarOpenings']
            closings = kolis_file['data']['data']['closingDays']

            # print(openings[1][1])
            # print(closings[1])

            horaires = {
                "calendarOpening": {
                    "monday": {
                        "plage1": "10:00 - 12:00",
                        "plage2": "14:00 - 17:00",
                    },
                    "thursday": {
                        "plage1": None,
                        "plage2": "14:00 - 17:00",
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
                        "plage2": "14:00 - 17:00",
                    },
                    "sunday": {
                        "plage1": None,
                        "plage2": "14:00 - 17:00",
                    }
                }
            }

            json.dumps(horaires)

            for i in range(len(meetingDateTime)):
                if meetingDateTime[i] >= 'a' and meetingDateTime[i] <= 'z':
                    meetingDateTime[i] = ' '
                if meetingDateTime[i] >= 'A' and meetingDateTime[i] <= 'Z':
                    meetingDateTime[i] = ' '
            if meetingDateTime:
                day1 = meetingDateTime[8]
                day2 = meetingDateTime[9]
                month1 = meetingDateTime[5]
                month2 = meetingDateTime[6]
                years1 = meetingDateTime[0]
                years2 = meetingDateTime[1]
                years3 = meetingDateTime[2]
                years4 = meetingDateTime[3]
                meetingDateTime[0] = day1
                meetingDateTime[1] = day2
                meetingDateTime[2] = "/"
                meetingDateTime[3] = month1
                meetingDateTime[4] = month2
                meetingDateTime[5] = "/"
                meetingDateTime[6] = years1
                meetingDateTime[7] = years2
                meetingDateTime[8] = years3
                meetingDateTime[9] = years4
                mdt = ''.join(meetingDateTime)
            if status == 1:
                historical = "Votre colis est en cours d'acheminement"
                name = '3_acheminementencours.html'
            elif status == 2:
                historical = "Votre colis est disponible dans votre relais. Prenez un rdv via le lien:"
                name = '4_disponibleenpointrelais.html'
            elif status == 3:
                historical = "Vous avez un rendez-vous de fixe"
                name = '6_rdvvalide.html'
            elif status == 4:
                historical = "Votre colis vous a ete remis"
                name = '7_colislivre.html'
            elif status == 5:
                historical = "Votre commande est annulee"
                name = '8_commandeannulee.html'
            elif status == 6:
                historical = "Votre commande est annulee"
                name = '8_commandeannulee.html'
            elif status == 7:
                historical = "Votre commande est annulee"
                name = '8_commandeannulee.html'
            elif status == 8 or status == 9 or status == 10 or status == 11:
                historical = "Votre commande est annulee"
                name = '8_commandeannulee.html'

            return render_template(name,
                                   relayAddress=relayAddress,
                                   trackingNumber=TrackingNumber,
                                   relayName=relayName,
                                   relayMaps=relayMaps,
                                   historic=historical,
                                   productHeight=productHeight,
                                   productLength=productLength,
                                   productDescription=productDescription,
                                   productVolume=productVolume,
                                   productWidth=productWidth,
                                   productWeight=productWeight,
                                   status=kolis_file['status'],
                                   dateHoraire=dateHoraire,
                                   meetingLink=meetingLink if status == 2 or status == 3 else None,
                                   meetingDateTime=mdt if status == 2 or status == 3 else None,
                                   goh=url_for('static', filename="goh.svg"),
                                   gom=url_for('static', filename="gom.svg"),
                                   no=url_for('static',
                                              filename='no.svg') if status != 1 and status != 2 and status != 3 and status != 4 else None,
                                   acheminement=url_for('static', filename="acheminement.svg") if status == 1 else None,
                                   valide=url_for('static', filename='valide.svg') if status != 1 else None,
                                   disporelais=url_for('static', filename='disporelais.svg') if status == 2 else None,
                                   rdvok=url_for('static', filename='rdvok.svg') if status == 3 else None,
                                   image_delivered=url_for('static', filename='delivered.png') if status == 4 else None,
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


if __name__ == '__main__':
    # app.run()
    app.run(debug=True)

