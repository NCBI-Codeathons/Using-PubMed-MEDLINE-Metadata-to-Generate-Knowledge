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

scrList = []


DECL_PREFIX = "d2020"
SCR_PREFIX  = "c2020"

OUT_PREFIX  = "mesh2020"


def createNode(heading, nodes, synonyms):
#    print(heading + " : " + " ".join(nodes))
    for node in nodes:
        nodeList.append((node, heading))
    if len(synonyms) > 0:
        synonymList.append((heading, synonyms))

def createSCRNode(heading, nodes, synonyms):
#    print(heading + " : " + " ".join(nodes))
    for node in nodes:
        nodeList.append((node, heading))
    scrList.append(heading)
    for synonym in synonyms: scrList.append(synonym)

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

nodeDict = {}
pathSet = set()

def buildNodeDict():
    for tree_node, heading in nodeList:
        nodeDict.setdefault(heading, []).append(tree_node)
        pathSet.add(tree_node)

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
                    createSCRNode(heading, nodes, synonyms)
                    heading = ""
                    nodes = []
                    synonyms = []
                continue
            mo = re_line.match(line)
            if not mo: continue
            ty, content = mo.groups()
            if ty == "NM":
                heading = content
            elif False: # disable putting SCR terms in the hierarchy ty == "HM":
                if len(content) and content[0] == '*':
                    content = content[1:]
                tree_paths = nodeDict.get(content, [])
                # get all node paths for this entry, create our own paths for this node
                for tree_path in tree_paths:
                    for i in range(1000):
                        new_tree_path = tree_path + '.' + str(i)
                        if not new_tree_path in pathSet:
                            pathSet.add(new_tree_path)
                            nodes.append(new_tree_path)
                            break
            elif ty == "SY":
                synonym = content
                try:
                    i = content.index('|')
                    synonym = content[:i]
                except ValueError: pass
                synonyms.append(synonym)
    if heading:
        createSCRNode(heading, nodes, synonyms)

def writeFiles():
    with open(OUT_PREFIX+".nodes", "w") as f:
        for tree_node, heading in nodeList:
            f.write(tree_node+'\t'+heading+'\n')
    with open(OUT_PREFIX+".synonyms", "w") as f:
        for name, synonyms in synonymList:
            f.write(name+'\t'+'\t'.join(synonyms)+'\n')
    
    with open(OUT_PREFIX+".scr", "w") as f:
        for name in scrList:
            f.write(name+'\n')


def main(argv):
    parseDescriptors()
#    buildNodeDict()
    parseSCR()
    writeFiles()

    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
