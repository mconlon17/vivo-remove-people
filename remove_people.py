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
import sys
from vivotools import read_csv
from vivotools import remove_uri
from vivotools import rdf_header
from vivotools import rdf_footer
import codecs
import operator

def uri_set(file_name):
    """
    Return a set of uris from  a csv file
    """
    data = read_csv(file_name)
    return set(row['uri'] for row in data.values())

# Start here

sample = 0.01 
srdf = ""
#log_file = open('remove_people_log.txt',"w")
log_file = sys.stdout
print >>log_file, datetime.now(), "Start"
set_all = uri_set('all_list.txt')
print >>log_file, datetime.now(), len(set_all), "persons in VIVO"
set_keep = uri_set('keep_list.txt')
print >>log_file, datetime.now(), len(set_keep), "people to keep in VIVO"

#   Generate the list to remove

set_remove = set_all - set_keep
print >>log_file, datetime.now(), len(set_remove), "people to remove from VIVO"

#   Process the people to remove

report = {}
for uri in set_remove:
    if random.random() > sample:
        continue
    sub = remove_uri(uri)
    report[uri] = len(sub)
    srdf = srdf + sub

#   Print report

for uri,size in sorted(report.iteritems(), key=operator.itemgetter(1), reverse=True):
    print >>log_file, datetime.now(), uri, size

sub_file = codecs.open("remove_people_sub.rdf", mode="w", encoding="ascii",
                      errors = "xmlcharrefreplace")
sub_file.write(rdf_header())
sub_file.write(srdf)
sub_file.write(rdf_footer())
sub_file.close()

print >>log_file, datetime.now(), "Finish"

