?incentiveTable <http://ontology.tno.nl/interconnect/incentivetable#hasTierUpperLimit> ?incentiveUpperLimit . 
?incentiveUpperLimit <http://ontology.tno.nl/interconnect/data#hasDataPoint> ?dataPoint . 
?dataPoint <https://saref.etsi.org/core/hasValue> ?value . 
?dataPoint <http://ontology.tno.nl/interconnect/data#hasEffectivePeriod> ?interval . 
?interval <http://www.w3.org/2006/time#hasBeginning> ?beginningInstant . 
?beginningInstant <http://www.w3.org/2006/time#inXSDDateTimeStamp> ?beginningTimeStamp . 
?interval <http://www.w3.org/2006/time#hasEnd> ?endInstant . 
?endInstant <http://www.w3.org/2006/time#inXSDDateTimeStamp> ?endTimestamp . 
