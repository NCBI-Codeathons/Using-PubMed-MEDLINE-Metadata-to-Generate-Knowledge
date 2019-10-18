#!/usr/bin/env python3
from typing import List, Dict
import re
import sys
import os.path

re_line = re.compile(r"([A-Z]+) *= *(.+)")

# MN (tree path), MH (main name)
nodeList = [
  ('A', 'Anatomy'),
  ('B', 'Organisms'),
  ('C', 'Diseases'),
  ('D', 'Chemicals and Drugs'),
  ('E', 'Analytical, Diagnostic and Therapeutic Techniques, and Equipment'),
  ('F', 'Psychiatry and Psychology'),
  ('G', 'Phenomena and Processes'),
  ('H', 'Disciplines and Occupations'),
  ('I', 'Anthropology, Education, Sociology, and Social Phenomena'),
  ('J', 'Technology, Industry, and Agriculture'),
  ('K', 'Humanities'),
  ('L', 'Information Science'),
  ('M', 'Named Groups'),
  ('N', 'Health Care'),
  ('V', 'Publication Characteristics'),
  ('Z', 'Geographicals')
]

# main name, [ synonyms ]
synonymList = []


DECL_PREFIX = "d2020"
SCR_PREFIX  = "c2020"

OUT_PREFIX  = "mesh2020"


def createNode(heading, nodes, synonyms):
#    print(heading + " : " + " ".join(nodes))
    for node in nodes:
        nodeList.append((node, heading))
    if len(synonyms) > 0:
        synonymList.append((heading, synonyms))


def parseDescriptors():
    heading = ""
    nodes = []
    synonyms = []
    # process Declarations file - record type D
    # MH - MeSH heading, main name
    # MN - node path
    # ENTRY - synonym
    with open(DECL_PREFIX+".bin", "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line == "*NEWRECORD":
                if heading:
                    createNode(heading, nodes, synonyms)
                    heading = ""
                    nodes = []
                    synonyms = []
                continue
            mo = re_line.match(line)
            if not mo: continue
            ty, content = mo.groups()
            if ty == "MH":
                heading = content
            elif ty == "MN":
                nodes.append(content)
            elif ty == "ENTRY":
                synonym = content
                try:
                    i = content.index('|')
                    synonym = content[:i]
                except ValueError: pass
                synonyms.append(synonym)
    if heading:
        createNode(heading, nodes, synonyms)

def parseSCR():
    heading = ""
    nodes = []
    synonyms = []
    # Process SCR file - record type C
    # NM - main name
    # SY - synonym
    # HM - reference to MeSH heading
    with open(SCR_PREFIX+".bin", "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            if line == "*NEWRECORD":
                if heading:
                    createNode(heading, nodes, synonyms)
                    heading = ""
                    nodes = []
                    synonyms = []
                continue
            mo = re_line.match(line)
            if not mo: continue
            ty, content = mo.groups()
            if ty == "NM":
                heading = content
            elif ty == "HM":
                pass
                # get all node paths for this entry, create our own paths for this node
                #nodes.append(content)
            elif ty == "SY":
                synonym = content
                try:
                    i = content.index('|')
                    synonym = content[:i]
                except ValueError: pass
                synonyms.append(synonym)
    if heading:
        createNode(heading, nodes, synonyms)

def writeFiles():
    with open(OUT_PREFIX+".nodes", "w") as f:
        for tree_node, heading in nodeList:
            f.write(tree_node+'\t'+heading+'\n')
    with open(OUT_PREFIX+".synonyms", "w") as f:
        for name, synonyms in synonymList:
            f.write(name+'\t'+'\t'.join(synonyms)+'\n')
    


def main(argv):
    parseDescriptors()
    parseSCR()
    writeFiles()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
