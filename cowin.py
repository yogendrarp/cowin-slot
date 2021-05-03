import externalwebservice.webservicehelpers as web
import json
import datetime
import smtplib
import os


def sendmail(slotdate,center,availableslot):
        try:
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"

            EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
            EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
            EMAIL_RECIPIENT = os.environ.get('EMAIL_RECIPIENT')
            message = """
                        Subject: Cowin 18+ slot availability

                        {slotdate}\t{center}\t{availableslot}
                      """
            message = message.replace("{slotdate}",str(slotdate)).replace("{center}",str(center)).replace("{availableslot}",str(availableslot))    
            
            with smtplib.SMTP_SSL(smtp_server, port) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, EMAIL_RECIPIENT, message)        
        except:
            traceback.print_exc()


def fetch():
    today=datetime.datetime.now()
    pincode="560066"
    dateformatted = today.strftime('%d') + "-" + today.strftime('%m') + "-" + today.strftime('%Y')
    url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={datetocheck}"
    url=url.replace("{pincode}",pincode).replace("{datetocheck}",dateformatted)
    response = web.make_get_call(url)
    cowinobject=json.loads(response.text)
    for center in cowinobject['centers']:
        for session in center['sessions']:
            if session['min_age_limit'] == 18 and session['available_capacity'] > 0:
                sendmail(session['date'], center['name'], session['available_capacity'])

fetch()
