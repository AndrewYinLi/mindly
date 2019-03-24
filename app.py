# 3rd base
from flask import Flask, jsonify, request, make_response

# local
# from database import db
from database import add_person, get_person

# initialize the flask app server
app = Flask(__name__)


# Person object class
class Person(object):
    """ Class implemented to create a person and add it to the database. A person is someone relevant to the
    user (relative, friend, ...). At the moment the person has 3 fields into it: name, relationship status and
    contact number.
    """

    def __init__(self, name=None, rel=None, contact=None, newperson=True):
        self.name = name
        self.rel = rel
        self.contact = contact
        self.newperson = newperson

    def add_name(self, name):
        self.name = name

    def add_rel(self, rel):
        self.rel = rel

    def add_contact(self, contact):
        self.contact = contact

    def del_person(self):
        self.__init__()


person_obj = Person()


# default route
@app.route('/')
def index():
    return 'Hello World!'


# create a route for webhook
# you need to provide the url provided by ngrok + "/webhook"
@app.route('/webhook')
def hello():
    return 'Hello World!'


# function for responses
def act_on_response():
    """ Function built for getting and processing responses from the chatbot.
    """

    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    print(req.get('queryResult'))

    action = req.get('queryResult').get('action')
    print('ACTION', action)

    # Person's name response
    if action == 'AddPerson.AddPerson-Name':
        # check if person object was semi-defined and add person intent was started again
        if person_obj.name is not None:
            person_obj.del_person()

        # get person's name from the response
        name = req.get('queryResult')['parameters']['given-name']
        # add name to person's object
        person_obj.add_name(name)

        return {'fulfillmentText': 'What is your relationship to %s?' % name}

    # Person's relationship response
    if action == 'AddPerson.AddPerson-Name.AddPerson-Name-Relationship':
        rel = req.get('queryResult')['parameters']['Relationship']
        name = person_obj.name
        person_obj.add_rel(rel)
        return {'fulfillmentText': 'What is %s\'s contact number?' % name}

    # Person's contact response
    if action == 'AddPerson.AddPerson-Name.AddPerson-Name-Relationship.AddPerson-Name-Relationship-Contact':
        name = person_obj.name
        rel = person_obj.rel
        contact = req.get('queryResult')['parameters']['phone-number']
        # print(name, rel, contact)
        # add person to the user base
        add_person(name, rel, contact)
        person_obj.del_person()
        return {'fulfillmentText': 'Person added.'}

    # Whois response
    if action == 'Whois':
        name = req.get('queryResult')['parameters']['given-name']
        person = get_person(name)
        if not person:
            return {'fulfillmentText': 'I do not know who %s is, sorry. Do you want to add %s? Type "Add Person".' % (name, name)}
        return {'fulfillmentText': '%s is your %s. You can contact them at %s' % (name, person['relationship'], person['contact'])}


# create a route for webhook
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # return response object
    return make_response(jsonify(act_on_response()))


# run the app
if __name__ == '__main__':
    app.run()

