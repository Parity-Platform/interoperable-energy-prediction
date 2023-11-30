EV Loader sample repository for SSA
===============================

## Interconnect

[https://gitlab.inesctec.pt/groups/interconnect-public/-/wikis/home](https://gitlab.inesctec.pt/groups/interconnect-public/-/wikis/home)

1. Create account at [https://store.interconnectproject.eu](https://store.interconnectproject.eu/) with evloader email selecting evloader organization
2. Run Generic Adapter locally
3. Login via Postman to Generc Adapter [localhost:9090](http://localhost:9090) using credentials from 1.
4. Create evloader service on service store
5. Get service id
6. Get hash from this request {{baseUrl}}/servicestore/services/<SERVICE ID FROM 5> 
7. Use hash from 6 in the request body to th post request to {{baseUrl}}/servicestore/adapter/register
8. the response from 7 is the knowledge base ID
9. REgister the KnowLedge base (create smart connector). Use the above knowledgeBaseId in the POST request to {{baseUrl}}/smartconnector/create 
10. Now using the above KnowledgeBaseID in the subsequent requests’ header, we can register Knowledge Interactions
11. Register React to Gridnet

```json
POST {{baseUrl}}/smartconnector/ki/register-post-react

KnowledgeBaseId: https://ke.interconnectproject.eu/adapter/9fe8ecd5178dfdd0a64328b1c63e7918102b8db2a30dd7630056058fe8f3eafe530d3666861b918226e9b003974559bd4fc6ad224a4feba97bcffabd3ba2342a

Request:
{
    "knowledgeInteractionType": "ReactKnowledgeInteraction",
    "argumentGraphPattern": "?incentiveTable <http://ontology.tno.nl/interconnect/incentivetable#hasTierUpperLimit> ?incentiveUpperLimit . ?incentiveUpperLimit <http://ontology.tno.nl/interconnect/data#hasDataPoint> ?dataPoint . ?dataPoint <https://saref.etsi.org/core/hasValue> ?value . ?dataPoint <http://ontology.tno.nl/interconnect/data#hasEffectivePeriod> ?interval . ?interval <http://www.w3.org/2006/time#hasBeginning> ?beginningInstant . ?beginningInstant <http://www.w3.org/2006/time#inXSDDateTimeStamp> ?beginningTimeStamp . ?interval <http://www.w3.org/2006/time#hasEnd> ?endInstant . ?endInstant <http://www.w3.org/2006/time#inXSDDateTimeStamp> ?endTimestamp . ",
    "resultGraphPattern": "?incentiveTable <http://ontology.tno.nl/interconnect/incentivetable#hasTierUpperLimit> ?incentiveUpperLimit . ?incentiveUpperLimit <http://ontology.tno.nl/interconnect/data#hasDataPoint> ?dataPoint . ?dataPoint <https://saref.etsi.org/core/hasValue> ?value . ?dataPoint <http://ontology.tno.nl/interconnect/data#hasEffectivePeriod> ?interval . ?interval <http://www.w3.org/2006/time#hasBeginning> ?beginningInstant . ?beginningInstant <http://www.w3.org/2006/time#inXSDDateTimeStamp> ?beginningTimeStamp . ?interval <http://www.w3.org/2006/time#hasEnd> ?endInstant . ?endInstant <http://www.w3.org/2006/time#inXSDDateTimeStamp> ?endTimestamp . ",
    "prefixes": {
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "ex": "http://example.org/"
    }
}

Response:
{
    "knowledgeInteractionId": "https://ke.interconnectproject.eu/adapter/9fe8ecd5178dfdd0a64328b1c63e7918102b8db2a30dd7630056058fe8f3eafe530d3666861b918226e9b003974559bd4fc6ad224a4feba97bcffabd3ba2342a/interaction/50ef3415-b69b-4577-a354-6051ef815600"
}
```

1. If running 11 results in error of knowledge base inactivity, then run 9. again
2. Initiate long-polling request loop via GET {{baseUrl}}/smartconnector/handle/start
3. **On response → custom EVLoader logic →send reaction via POST** {{baseUrl}}/smartconnector/handle/send?polling=false 

The above steps are also described in the following 

[https://www.youtube.com/watch?v=W7ywyJSNEGs](https://www.youtube.com/watch?v=W7ywyJSNEGs)

This is our service

[ServiceStore](https://store.interconnectproject.eu/ServiceStore/#/service/service-details/631431)

This project may be useful for our implementation

[https://gitlab.inesctec.pt/interconnect-public/service-specifc-adapters/-/blob/main/project-SSAs/Cosmote Real Time Data Retrieval(POST_REACT) SSA/service_specific_adapter_base.py](https://gitlab.inesctec.pt/interconnect-public/service-specifc-adapters/-/blob/main/project-SSAs/Cosmote%20Real%20Time%20Data%20Retrieval(POST_REACT)%20SSA/service_specific_adapter_base.py)