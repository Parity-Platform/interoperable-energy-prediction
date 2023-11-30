from service_specific_adapter_base import ServiceSpecificAdapterBase
import os
import json
import datetime


if __name__ == "__main__":
    ssa = ServiceSpecificAdapterBase(os.getenv("SSA_SERVER", "localhost:9090"))

    # Service store login with credentials to get Bearer token (bearer token is stored and used in the GA, so you don't have to take care of it)
    ssa.service_store_login(os.getenv("SERVICE_STORE_EMAIL"), os.getenv("SERVICE_STORE_PASSWORD"))

    # Delete all previous ki and kb that left open for the specific service
    smart_connectors = ssa.get_all_smart_connectors()
    
    # TODO: Delete smart connectors
    print(smart_connectors)

    # Link the adapter to the service in the service store
    knowledge_base_id = os.getenv("SSA_KNOWLEDGEBASE_ID")
    if knowledge_base_id == None:
        knowledge_base_id = ssa.register_generic_adapter("9c3dfb3b8ecb7580997ae367e01a951d3e5b9bf3874bd9561a6a997181014a8f8b5442f15c79cdec60a0b4ab848acbeb5a7aa198e5cfc7a218ab1ac6d46d455b")
    else:
        ssa.knowledge_base_id = knowledge_base_id

    # Register the knowledge base by creating a smart connector (use the response from the previous call)
    ssa.add_knowledge_base(knowledge_base_id, 'EV Loader Incentives', 'EV Loader Incentives Knowledge Base')

    # Register the knowledge interaction
    knowledge_interaction_description = 'React to Incentives'
    knowledge_interaction_type = 'ReactKnowledgeInteraction'
    graph_pattern = open('incentive.gp').read()

    communicative_act = {
        'requiredPurposes': [
            'https://www.tno.nl/energy/ontology/interconnect#InformPurpose'
        ],
        'satisfiedPurposes': [
            'https://www.tno.nl/energy/ontology/interconnect#InformPurpose'
        ]
    }

    # add REACT knowledge interaction
    kiid2 = ssa.add_knowledge_interaction(
        knowledge_interaction_description=knowledge_interaction_description,
        knowledge_interaction_type=knowledge_interaction_type,
        argument_graph_pattern=graph_pattern,
        result_graph_pattern=graph_pattern
    )

    # Start long polling - Wait for an incentive
    try:
        print("Starting long polling ...")
        while True:
            # kiid, handleId, binding_set = ssa.get_respond_handle("https://ke.interconnectproject.eu/adapter/9fe8ecd5178dfdd0a64328b1c63e7918102b8db2a30dd7630056058fe8f3eafe530d3666861b918226e9b003974559bd4fc6ad224a4feba97bcffabd3ba2342a")
            kiid, handleId, binding_set = ssa.get_respond_handle(knowledge_base_id)
            print(kiid, handleId, binding_set)
            if binding_set != None:
                with open('./res-data/res_percentage.json', 'w') as fp:
                    json.dump(binding_set, fp)

                # Save json also with timestamp for keeping a history of the files
                timestamp = datetime.datetime.now().isoformat().replace(":", "-").split(".")[0]
                filename = f"./res-data/res_percentage_{timestamp}.json"
                with open(filename, 'w') as fp:
                    json.dump(binding_set, fp)

                # Answer the incoming request
                ssa.answer_incoming_request(kiid, handleId, [])

    except Exception as e:
        print("Exception was raised:", str(e))
        print("Cleaning up the SSA...")
        # 6. clean up
        ssa.remove_knowledge_base(knowledge_base_id)