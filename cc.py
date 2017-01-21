import requests
import json

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }



def get_currency_in_session(intent, session):
    
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    json_file = "codes.json"
    json_data = open(json_file)
    data = json.load(json_data)
    json_data.close()
    conversion = {}
    for item in data:
        conversion[str(item['name']).upper()] = str(item['code'])
    #conversion = {'dollar': 'USD', 'euro': 'EUR', 'pound': 'GBP','rupee': 'INR','dollars': 'USD', 'euros': 'EUR', 'pounds': 'GBP','rupees': 'INR' }

    if 'orgcurrency' in intent['slots']:
        orgcurr = intent['slots']['orgcurrency']['value'].upper()
        targcurr = intent['slots']['targetcurrency']['value'].upper()
        number = intent['slots']['number']['value']
        conval = 1
        if orgcurr in conversion.keys() :
            url = ('https://currency-api.appspot.com/api/%s/%s.json') % (conversion[orgcurr], conversion[targcurr])
            r = requests.get(url)
            rate = r.json()['rate']
            conval = int(number) * rate

        #session_attributes = create_favorite_color_attributes(favorite_color)
        speech_output = number + " " + orgcurr + "s is equivalent to  " + str(int(conval)) + " " + targcurr  \
                        + "s "   \

        reprompt_text = "I can convert amounts in  dollar, rupee, euro and pound"
    else:
        speech_output = "I'm not sure what the currency is. " \
                        "Please try again."
        reprompt_text = "Sample Utterance is GetCurrency convert 1000 dollar to rupee " \

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetCurrency":
        return get_currency_in_session(intent, session)
    else:
        raise ValueError("Invalid intent")


def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    #if event['session']['new']:
     #   on_session_started({'requestId': event['request']['requestId']},
      #                     event['session'])

    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])