#!/usr/bin/env/python

"""
    remove_people.py: Create subtraction RDF to remove people who do not meet
    the criteria for inclusion in VIVO
"""

__author__ = "Michael Conlon"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause license"
__version__ = "0.1"

from datetime import datetime
import random # for testing purposes, select subsets of records to process
import tempita
import sys
import vivotools as vt
import codecs

def all_people():
    """
    Return a list of all people in VIVO
    """
    query = tempita.Template("""
    SELECT ?uri
    WHERE {
        ?uri a foaf:Person .
    }
    """)
    query = query.substitute()
    result = vt.vivo_sparql_query(query)
    uris = []
    for b in result["results"]["bindings"]:
        uri = b['uri']['value']
        uris.append(uri)
    return uris

def keep_people():
    """
    return a list of all people who meet one or more criteria for
    remaining in VIVO
    """
    query = tempita.Template("""
    SELECT ?uri
    WHERE {
      {
      ?uri vivo:authorInAuthorship ?a .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri vivo:hasTeacherRole ?t .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri vivo:hasPrincipalInvestigatorRole ?t .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri a ufVivo:VIVOOptIn .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri a vivo:FacultyMember .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri a vivo:NonAcademic .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri a vivo:Postdoc .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri a ufVivo:CourtesyFaculty .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri a ufVivo:TemporaryFaculty .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri a ufVivo:Housestaff .
      ?uri a foaf:Person .
      }
      UNION {
      ?uri a ufVivo:ClinicalFaculty .
      ?uri a foaf:Person .
      }
    }
    GROUP BY ?uri
    """)
    query = query.substitute()
    result = vt.vivo_sparql_query(query)
    uris = []
    for b in result["results"]["bindings"]:
        uri = b['uri']['value']
        uris.append(uri)
    return uris

# Start here

sample = 0.01 
srdf = ""
#log_file = open('remove_people_log.txt',"w")
log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
list_a = all_people()
print >>log_file, datetime.now(), len(list_a), "persons in VIVO"
list_b = keep_people()
print >>log_file, datetime.now(), len(list_b), "people to keep in VIVO"

#   Generate the list to remove

list_c = []
for uri in list_a:
    if uri not in list_b:
        list_c.append(uri)
print >>log_file, datetime.now(), len(list_c), "people to remove from VIVO"

#   Process the people to remove

for uri in list_c:
    if random.random() > sample:
        continue
    sub = vt.remove_uri(uri)
    srdf = srdf + sub

sub_file = codecs.open("remove_people_sub.rdf", mode="w", encoding="ascii",
                      errors = "xmlcharrefreplace")
sub_file.write(vt.rdf_header())
sub_file.write(srdf)
sub_file.write(vt.rdf_footer())
subfile.close()

print >>log_file, datetime.now(), "Finish"

