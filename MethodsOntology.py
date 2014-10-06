#!/usr/bin/env python2

"""

MethodsOntology.py - Methods for working with the Methods Ontology (oma!
)


Owl:   Protege output (owl files)
       ._readMethods:   Read in methods from ontology (owl) file
       .getMethods:     Return list of methods
       ._parseMethods:   Returns list of methods with alternate terms

Pubmed: Methods for working with on and offline pubmed data
       .getXMLText:  Get raw text from pubmed xml file.  Uses:
       ._recursiveTextExtract: pull text from all xml elements
       .findMethods: Find methods in paper
       .extractMethods: return dictionary ["methodname","sentence it's in!'"]

SAMPLE USAGE: Please see README included with package


"""

import re
from lxml import etree
from fuzzywuzzy import fuzz

__author__ = ["Vanessa Sochat (vsochat@stanford.edu)","Natalie Telis ()","Jonathan Mortensen ()"]
__version__ = "$Revision: 1.0 $"
__date__ = "$Date: 2011/09/09 $"
__license__ = "Python"

# Owl------------------------------------------------------------------------------
class Owl:
    def __init__(self,infile):
        self.file = infile  # name of the owl input file
        self.rawmethod = self._readMethods()
        self.methods = self._parseMethods()

    ''' Return raw list of methods'''
    def getMethods():
      return self.methods

    ''' Read methods from owl file - no spaces'''
    def _readMethods(self):
      methods = []
      filey = open(self.file,"r")
      filey = filey.readlines()
      islabel = re.compile("^<rdfs:label>*")
      # The method names will not have http
      for line in filey:
        line = line.replace(" ","").replace("\n","")
        if islabel.match(line):
          method = line.replace("<rdfs:label>","").replace(" ","").replace("</rdfs:label>","")
          methods.append(method)
      return methods

    '''Return dictionary of methods with alternate terms'''
    def _parseMethods(self):
      methods = []
      # TODO: we should add the "searchable term" as a field in ontology?

      # Add spaces to methods - return in list
      # TODO: return in dict with alternate terms
      for m in self.rawmethod:
        # add a space to capital letters
        capitals = [c for c, (letter) in enumerate(m) if letter.isupper()]
        tmp = []
        for c in capitals:
          tmp.append(m[:c] + " ")
        tmp.append(m[c:len(m)])
        tmp = ''.join(tmp).strip().lower()
        methods.append(tmp)
      
      # TODO: Debug why the first methods in the list are single letters
      # For now get rid of them!
      methods = [m for m in methods if len(m) > 1]
      return methods
      # TODO: Use JMort method to look up alternative terms for each


# Pubmed ---------------------------------------------------------------------------
class Pubmed:
    def __init__(self,owl):
        self.owl = owl # an owl object

    '''Get XML text from methods section (raw)'''
    def getXMLText(self,xml):
      with open (xml, "r") as myfile:
        data = myfile.read().replace('\n', '')
      data = etree.XML(data)

      # Find the methods section
      # TODO: Check if section label consistent between journals
      for elem in iter(data):
        for e in iter(elem):
          if "materials|methods" in e.values():
            methodsection = e

      if methodsection is None:
        print "ERROR: Cannot find methods section!"
        sys.exit(32)

      # Get text - recursively go through elements
      text = self._recursiveTextExtract(methodsection)
      return text

    '''Return text for section'''
    def _recursiveTextExtract(self,xml):
      methodstext = []
      queue = []
      for elem in reversed(list(xml)):
        queue.append(elem)
      
      while (len(queue) > 0):
        # Pop the first element off
        current = queue.pop()
        if current.text != None:
          methodstext.append(current.text)
        if len(list(current)) > 0:
          for elem in reversed(list(current)):
            queue.append(elem)
      self.text = methodstext
      return methodstext

    '''Match methods to sentences in xml using fuzzy wuzzy'''
    def extractMethods(self):
      matches = dict()
      print "Searching article for methods..."
      fulltext = " ".join(self.text)
      # Find all the periods (sentence starts and ends)
      periods = [p.start() for p in re.finditer('[.]', fulltext)]
      for m in self.owl.methods:
        matchlist = list()
        try:
          expression = re.compile(m)
          match = expression.search(fulltext)
          if match:
            print "Found match for " + m + "!"
            # Extract the sentence - the period before and after.
            start = [p for p in periods if p < match.start()]
            if not start:
              start = 0
            else:
              start = start[-1]
            end = [p for p in periods if p > match.start()][0]
            matchlist.append(fulltext[start:end])
            matches[m] = matchlist
        except:
          print "Cannot parse method " + m + "... skipping!"

        # Another idea
        # Return list of match scores for method to all lines of text
        # [fuzz.partial_ratio(m,c) for c in self.text]
      self.matches = matches
      return matches

# MAIN ----------------------------------------------------------------------------------
def main():
    print __doc__

if __name__ == "__main__":
    main()
