from flask import Flask, request, make_response
import json
import os
from flask_cors import cross_origin
from SendEmail import EmailSender
from logger import logger
from covidcountry import countrywise
from covidworld import worldwide


app = Flask(__name__)



# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    res = processRequest(req)

    #res = json.dumps(res, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    log = logger.Log()

    sessionID=req.get('responseId')


    result = req.get("queryResult")
    user_says=result.get("queryText")
    log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")

    user_choice = parameters.get("user_choice")
    user_name = parameters.get("user_name")
    user_contact = parameters.get("user_contact")
    user_location = parameters.get("user_location")
    user_pincode = user_location.get("zip-code")
    user_email = parameters.get("user_email")

    intent = result.get("intent").get('displayName')
    if (intent=='covid_info'):

        email_sender=EmailSender()
        covid_world = worldwide()
        email_message = ""
        if (user_choice == 1):
            covid_state = countrywise()
            email_message=covid_state.send_country_info()
        elif(user_choice == 2):
            email_message = covid_world.send_world_info()
        elif(user_choice == 3):
            email_message = "https://www.accuweather.com/en/in/national/covid-19"

        email_sender.send_email_to_user(user_email,email_message)
        #email_file_support = open("email_templates/support_team_Template.html", "r")
        #email_message_support = email_file_support.read()
        #email_sender.send_email_to_support(cust_name=cust_name,cust_contact=cust_contact,cust_email=cust_email,course_name=course_name,body=email_message_support)
        fulfillmentText="We have sent the details to your email id. Do you have any other query"
        if(user_choice == 3):
            fulfillmentText = "https://www.accuweather.com/en/in/national/covid-19"
        #fulfillmentText = "https://www.accuweather.com/en/in/national/covid-19"
        log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText
        }
    else:
        log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
