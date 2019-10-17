#!/usr/bin/env python3
from typing import List, Dict
import sys
import os.path

# MH -> List[MH]
descendantDict = {}
# MN -> MH
nodesDict = {}

DECL_PREFIX = "d2020"

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

def createDescendantDict(cache_nodes=False):
    if cache_nodes:
        f = open(DECL_PREFIX+".nodes", "w")
    for tree_node, heading in nodesDict.items():
        if cache_nodes:
            f.write(tree_node+'\t'+heading+'\n')
        try:
            ri = tree_node.rindex('.')
            parent_node = tree_node[:ri]
            parent_header = nodesDict[parent_node]
            descendantDict.setdefault(parent_header, []).append(heading)
        except ValueError:
            pass
    if cache_nodes:
        f.close()
    
readNodesDict()
createDescendantDict()
