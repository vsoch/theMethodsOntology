#!/usr/bin/env python2

# Use theMethodsOntology module to parse pubmed xml
import MethodsOntology as MO

# Test xml file
owl = "/home/vanessa/Documents/Dropbox/Code/Python/theMethodsOntology/root-ontology.owl"
article = "/home/vanessa/Documents/Dropbox/Code/Python/theMethodsOntology/pone.0046493.nxml"

# Read in ontology
ontology = MO.Owl(owl)

# Create Pubmed parser for article
parser = MO.Pubmed(ontology)

# Text is also stored in parser object
text = parser.getXMLText(article)

# Now find sentences with methods
matches = parser.extractMethods()

