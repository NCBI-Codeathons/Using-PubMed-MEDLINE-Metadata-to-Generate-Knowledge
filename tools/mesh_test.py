#!/usr/bin/env python3
import sys
import os.path

from mesh import descendantsAndBucketsForTerms



def main(argv):
    if len(argv) < 2: return 0
    bucketDict = descendantsAndBucketsForTerms(argv[1:])
    buckets = {}
    for name, parents in bucketDict.items():
        for parent in parents:
            buckets.setdefault(parent, []).append(name)
    bucket_names = list(buckets.keys())
    bucket_names.sort()
    for bucket in bucket_names:
        print("bucket", bucket)
        nodes = buckets[bucket]
        nodes.sort()
        for node in nodes:
            print("  ", node)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))