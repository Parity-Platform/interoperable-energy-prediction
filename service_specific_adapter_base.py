import requests
import json


# This code is illustrative. It is just an example tryout. IC partners may use/copy it. VITO has no responsibility about any use of this code nor the quality of the code.
# This is the Service Specific Adapter (SSA) at the service side and a small test example in the 'main' section to start it up.
# The main performs the necessary registration steps at the GA. Afterwards it waits for incoming ANSWER or REACT reactions from the GA. After 10 times 3 times 25 sec = 375 sec it stops.


#TODO add return values to indicate if the method succeeded or failed
#TODO make more generic
#TODO add error checking, exception hanfdling,...

class ServiceSpecificAdapterBase:

    def __init__(self, server):
        self.knowledge_interactions = {}
        self.server = server

    def service_store_login(self, user, password):
        """
            Register at the service store to get a Bearer token for authentication of the next calls.
            The token is actually stored in the generic adater, so consequent generic adapter API calls
            don't need to include it in the authorization header.
        """
        response = requests.post (
            self.server + '/servicestore/login',
            json = {
                'email': user,
                'password': password
            }
        )
        print(self.server)
        print(response.status_code)

    def get_all_smart_connectors(self):
        response = requests.get(
            self.server + '/smartconnector/',
            json={}
        )
        return response.json()

    def get_all_ki_for_specific_kb(self, kb):
        response = requests.get(
            self.server + '/smartconnector/ki/get',
            json = {},
            headers = {'KnowledgeBaseId': kb}
        )
        return response.json()

    def register_generic_adapter(self, hash):
        """ register the generic adapter at the service store """
        response = requests.post (
            self.server + '/servicestore/adapter/register',
            json = {
                "hash": hash,
                "language": "PYTHON",
                "transport": "HTTP"

                }
        )
        print(f'Generic adapter registered: {response.status_code}')

        self.knowledge_base_id = None
        if response.status_code == 200:
            self.knowledge_base_id = response.text #hash to be used as knowledgebase id
        return self.knowledge_base_id

    def add_knowledge_base(self, knowledge_base_id, knowledge_base_name, knowledge_base_description ):
        """ Add knowledge base   => create a smart connector """
        self.knowledge_base_name = knowledge_base_name
        self.knowledge_base_description = knowledge_base_description

        #create smart connector
        response = requests.post (
            self.server + '/smartconnector/create',
            json = {
                'knowledgeBaseId': knowledge_base_id, #todo should be the hash from the service store registration
                'knowledgeBaseName': knowledge_base_name,
                'knowledgeBaseDescription': knowledge_base_description
                }
        )
        print(f'Knowledge base with id:{knowledge_base_id}, name:{knowledge_base_name} \
                and description{knowledge_base_description} added. \n \
                Return code {response.status_code}')
        return response.status_code

    def remove_knowledge_base(self, knowledge_base_id):
        #delete smart connector for this knowledge base
        response = requests.delete(
            self.server + '/smartconnector/delete',
            headers = {
                'KnowledgeBaseId': knowledge_base_id
            }
        )
        print(f'Knowledge base with id:{knowledge_base_id} has been deleted. \n \
                Return code {response.status_code}')
        return response.status_code

    def add_knowledge_interaction(  self, knowledge_interaction_description, knowledge_interaction_type, communicative_act = None,
                                    graph_pattern = None, argument_graph_pattern = None, result_graph_pattern = None):
        """
            add/register knowledge interaction to this smart connector (via generic adapter api).
            In case of ASK-ANSWER, the graph_pattern parameter has to be filled in.
            In case of POST-REACT, the argument_graph_pattern parameter has to be filled in. The result_graph_pattern parameter is optional.
        """
        knowledge_interaction_id = None
        headers = {'KnowledgeBaseId': self.knowledge_base_id }
        if knowledge_interaction_type == 'AskKnowledgeInteraction' or knowledge_interaction_type == 'AnswerKnowledgeInteraction':
            url = self.server + '/smartconnector/ki/register-ask-answer'
            json_body =  {
                    'knowledgeInteractionType': knowledge_interaction_type,
                    'graphPattern': graph_pattern
                }
        elif knowledge_interaction_type == 'PostKnowledgeInteraction' or knowledge_interaction_type == 'ReactKnowledgeInteraction':
            url = self.server + '/smartconnector/ki/register-post-react'
            json_body =  {
                    'knowledgeInteractionType': knowledge_interaction_type,
                    'argumentGraphPattern': argument_graph_pattern
                }
            if result_graph_pattern:
                json_body['resultGraphPattern'] = result_graph_pattern
            if communicative_act:
                json_body['communicativeAct'] = communicative_act
        else:
            print(f'Invalid interaction type \n \
                    Return code 400')

        response = requests.post(url, headers = headers, json = json_body)

        if response.status_code == 200:
            knowledge_interaction_id = response.text
            knowledge_interaction = {
                'description':knowledge_interaction_description,
                'type': knowledge_interaction_type,
                'communicative act': communicative_act,
                'graphPattern': graph_pattern,
                'argumentGraphPattern': argument_graph_pattern,
                'resultGraphPattern': result_graph_pattern
            }
            self.knowledge_interactions[knowledge_interaction_id] = knowledge_interaction
            print(knowledge_interaction)
            print(f'Knowledge interaction with id:{knowledge_interaction_id} added successfully. \n \
                    Return code {response.status_code}')
        else:
            print(f'Knowledge interaction addition failed. \n \
                    Return code {response.status_code}')
            print(response.json())
        return knowledge_interaction_id

    def remove_knowledge_interaction(self, knowledge_base_id, knowledge_interaction_id):
        """remove/deregister knowledge interaction to this smart connector (via generic adapter api)"""
            #delete smart connector for this knowledge base
        response = requests.delete(
            self.server + '/smartconnector/ki/unregister',
            headers = {
                'KnowledgeBaseId': knowledge_base_id,
                'KnowledgeInteractionId': knowledge_interaction_id
            }
        )
        # del self.knowledge_interactions[knowledge_interaction_id]
        print(f'Knowledge interaction deleted: {response.status_code}')
        return response.status_code

    ###############################################################################
    # reactive Knowledge interaction methods
    ###############################################################################

    def get_respond_handle(self, knowledge_base_id):
        """
        get a handle to respond to a request
        This method loops until a request comes in !!!!!
        """
        #TODO threading
        status_code = 0
        i=0
        while ( str(status_code)[0] != "2" and i<3):
            response = requests.get (
                self.server + '/smartconnector/handle/start',
                headers = {
                    'KnowledgeBaseId': knowledge_base_id
                }
            )
            status_code = response.status_code
            print (f'get_response_handle for KnowledgeBaseId {knowledge_base_id} returns status code {status_code}')
            i+=1

        if i < 3:
            response_dict = response.json()
            # print(response_dict)
            # identification of the request
            try:
                kiid = response_dict['knowledgeInteractionId']
                handleId = response_dict['handleRequestId']

                #input parameters
                binding_set = response_dict['bindingSet']

                return kiid, handleId, binding_set
            except:
                return None, None, None
        else:
            return None, None, None

    def answer_incoming_request(self, kid, handleId, binding_set):
        """answer the request"""

        #map knowledge_interaction_id onto API call or sequence of API calls
        #TODO make a more generic mapping
        # for now, just one API call 'get the forecast from the service'
        #TODO select the right service API call based upon KIID

        #get input parameters
        input_parameters = self.map_bindingset_to_service_input_parameters(kid, binding_set)
        #call the specific service
        # service_response = self.get_service_response(input_parameters)

        #create the bindingset for the answer
        #TODO in case of empty result graph pattern for REACT, bindingset must be empty
        response_bindings = self.map_service_output_parameters_to_bindingset(kid, binding_set, input_parameters)

        #send a response back with the answer
        body = {}
        body['handleRequestId'] = handleId
        body['bindingSet'] = response_bindings

        response = requests.post (
            self.server + '/smartconnector/handle/send',
            headers = {
                'KnowledgeBaseId': self.knowledge_base_id,
                'KnowledgeInteractionId': kid
            },
            json = body
        )
        print(response.text)
        if response.status_code != 200:
            print(f'React response returned error {response.status_code}')
        else:
            print(f'Responded to a request with: {body}')

    ###############################################################################
    # proactive Knowledge interaction methods
    ###############################################################################
    def ask_request(self, kid, binding_set):
        response = requests.post (
            self.server + '/smartconnector/ask',
            headers = {
                'KnowledgeBaseId': self.knowledge_base_id,
                'KnowledgeInteractionId': kid
            },
            json = binding_set
        )

        if response.status_code != 200:
            response_dict = None
            print(f'Ask request returned error {response.status_code}')
        else:
            response_dict = response.json()["bindingSet"]
            print(f'ASK request response: {response_dict}')
        return response_dict


    def post_request(self, kid, binding_set):
        binding_set = json.dumps([binding_set])

        response = requests.post (
            self.server + '/smartconnector/post',
            headers = {
                'Content-Type': 'application/json',
                'KnowledgeBaseId': self.knowledge_base_id,
                'KnowledgeInteractionId': kid
            },
            data = binding_set
        )
        print(response.status_code)
        if response.status_code != 200:
            response_dict = None
            print(f'POST request returned error {response.status_code} \n Response text: {response.text} ')
        else:
            response_dict = response.json()["resultBindingSet"]
            print(f'POST request response: {response_dict}')
        return response_dict



    ###############################################################################
    #   Service specific methods
    #   Override in child class
    ###############################################################################

    def map_bindingset_to_service_input_parameters(self, kid, binding_set):
        #use kid to determine the API call, and do then the mapping onto the API parameters
        pass

    def map_service_input_parameters_to_bindingset(self, kid, input_parameters):
        #use kid to determine the API call, and do then the mapping onto the binding_set
        pass

    def map_service_output_parameters_to_bindingset(self, kid, input_binding_set, service_output):
        #use kid to determine the API call, and do then the mapping onto the API parameters
        return []

    def map_bindingset_to_service_output_parameters(self, kid, binding_set):
        pass

    def get_service_response(self, input_parameters):
        # get the response from the service
        pass
