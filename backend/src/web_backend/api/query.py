from flask import Blueprint, jsonify, request
from web_backend.utils.pubmed import getPubMedIdsForMesh, addMeshTermsToIds, descendantsAndBucketsForTerms, countGroupedIds

api = Blueprint(
    'api',
    __name__,
)

@api.route("/query", methods=['POST'])
def query():
    first_mesh_terms = request.json.get('first_list')

    print(first_mesh_terms)
    second_mesh_terms = request.json.get('second_list')
    print(second_mesh_terms)
    pubmed_ids = getPubMedIdsForMesh(first_mesh_terms, second_mesh_terms, 1000000)
    #print(pubmed_ids)
    mesh_ids = addMeshTermsToIds(pubmed_ids)
    #print(mesh_ids)
    
    term_to_group = descendantsAndBucketsForTerms(second_mesh_terms)
    #print(term_to_group)
    result = countGroupedIds(term_to_group, mesh_ids)
    #print(result)
    return jsonify(result)
