#!/usr/bin/env python3
from typing import List, Dict
import sys
import os.path

# MH -> List[MH]
descendantDict = {}
# MN -> MH
nodesDict = {}

base_dir = os.path.dirname(os.path.realpath(__file__))
DECL_PREFIX = base_dir + "/mesh2020"

def getDescendants(term: str, level, cumulative=True):
    all_descendants = []
    cur_level = 0
    descendants = descendantDict.get(term, [])
    all_descendants += descendants
    if level > 0:
        for descendant in descendants:
            all_descendants += getDescendants(descendant, level-1)
    return all_descendants


def descendantsAndBucketsForTerms(mesh_terms: List[str], level=1) -> Dict:
    res = {}
    for term in mesh_terms:
        roots = getDescendants(term, level)
#        print(roots, file=sys.stderr)
        roots_to_keep = {x: None for x in roots}
        for root in roots:
            descendants = getDescendants(root, 1000000)
            for descendant in descendants:
                if descendant in roots_to_keep:
                    del roots_to_keep[descendant]
        roots = list(roots_to_keep.keys())
#        print(roots, file=sys.stderr)
        for root in roots:
            res.setdefault(root, set()).add(root)
            descendants = getDescendants(root, 1000000)
            for descendant in descendants:
                res.setdefault(descendant, set()).add(root)
    return res

def readNodesDict():
    with open(DECL_PREFIX+".nodes", "r") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parts = line.split('\t')
            nodesDict[parts[0]] = parts[1]

def createDescendantDict():
    for tree_node, heading in nodesDict.items():
        parent_node = None
        try:
            ri = tree_node.rindex('.')
            # Dot separated path, tree node in a form A01.236.249, parent - A01.236
            parent_node = tree_node[:ri]
        except ValueError:
            # Second level category, tree_node in a form A01, parent - A
            if len(tree_node) > 1:
                parent_node = tree_node[0]
        if parent_node:
            parent_header = nodesDict[parent_node]
            descendantDict.setdefault(parent_header, []).append(heading)
    
readNodesDict()
createDescendantDict()
