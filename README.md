# Remove People from VIVO


Remove people from VIVO who do not satisfy criteria for remaining in VIVO.

## The criteria

1. OptIn
1. An author
1. An investigator
1. A teacher
1. A UF person past or present with one or more qualifying HR types:
    1. Faculty
	1. Emeritus
	1. Salaried staff
	1. Postdoc
	1. Housestaff

## The algorithm for removal

1.  Define set A as all people in VIVO
1.  Define set B as all people meeting one or more criteria for inclusion
1.  Define set C as A-B
1.  For each person in set C
    1. Remove all triples with person as subject
	1. Remove all triples with person as object
1.  Take the resulting subtraction RDF and aply it to VIVO through the web interface
	
## Notes

1.  Removing triples as described will result in data integrity errors for roles 
and other _connector_ entities.  These will be cleaned up by other data management 
processes.
1.  The definitions of A and B are contained in SPARQL queries and are easily modified.
