from flask import Blueprint, jsonify, request

from web_backend.utils.mesh import descendantsAndBucketsForTerms

from web_backend.utils.pubmed import getPubMedIdsForMesh, addMeshTermsToIds, \
    countGroupedIds, loadVocabulary, PRIMARY, \
    SECONDARY


api = Blueprint(
    'api',
    __name__,
)


primary_vocab = loadVocabulary(PRIMARY)
secondary_vocab = loadVocabulary(SECONDARY)


@api.route("/query", methods=['POST'])
def query():
    first_mesh_terms = request.json.get('first_list')

    # print(first_mesh_terms)
    second_mesh_terms = request.json.get('second_list')
    pubmed_ids = getPubMedIdsForMesh(
        first_mesh_terms, second_mesh_terms, 1000000)
    mesh_ids = addMeshTermsToIds(pubmed_ids)

    term_to_group = descendantsAndBucketsForTerms(second_mesh_terms)
    #print(term_to_group)
    result = countGroupedIds(term_to_group, mesh_ids)
    #print(result)
    return jsonify(result)


@api.route("/autocomplete", methods=['GET'])
def autocomplete():
    text = request.args.get('text_so_far')
    is_primary = request.args.get('vocab') == 'primary'
    vocab = primary_vocab if is_primary else secondary_vocab
    return jsonify(vocab.autocomplete(text))
