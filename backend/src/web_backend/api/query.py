from flask import Blueprint, jsonify, request

from web_backend.utils.mesh import descendantsAndBucketsForTerms

from web_backend.utils.pubmed import getPubMedIdsForMesh, addMeshTermsToIds, descendantsAndBucketsForTerms, countGroupedIds

api = Blueprint(
    'api',
    __name__,
)

@api.route("/query", methods=['POST'])
def query():
    first_mesh_terms = request.json.get('first_list')
    second_mesh_terms = request.json.get('second_list')
    pubmed_ids = getPubMedIdsForMesh(
        first_mesh_terms, second_mesh_terms, 1000000)
    mesh_ids = addMeshTermsToIds(pubmed_ids)

    term_to_group = descendantsAndBucketsForTerms(second_mesh_terms)
    result = countGroupedIds(term_to_group, mesh_ids)
    return jsonify(result)
