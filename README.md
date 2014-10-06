# TheMethodsOntology

Python module and scripts for parsing the ontology (owl file) and searching pubmed articles for methods. *under development*

# MethodsOntology.py

## Owl
- Protege output (owl files)
- ._readMethods:   Read in methods from ontology (owl) file
- .getMethods:     Return list of methods
- ._parseMethods:   Returns list of methods with alternate terms

## Pubmed
- Methods for working with on and offline pubmed data
- .getXMLText:  Get raw text from pubmed xml file.  Uses:
- ._recursiveTextExtract: pull text from all xml elements
- .findMethods: Find methods in paper
- .extractMethods: return dictionary ["methodname","sentence it's in!'"]

# Example usage

### Use theMethodsOntology module to parse pubmed xml
	import MethodsOntology as MO

### Test xml file
	owl = "root-ontology.owl"
	article = "pone.0046493.nxml"

### Read in ontology
	ontology = MO.Owl(owl)

### Create Pubmed parser for article
	parser = MO.Pubmed(ontology)

### Text is also stored in parser object
	text = parser.getXMLText(article)

### Now find sentences with methods
	matches = parser.extractMethods()




