import attr
import datetime
from Bio import Entrez
from Bio import Medline
from collections import Counter
from typing import Dict, List, Optional, Set


# Return list of pubmed ids for the query
def getPubMedIds(search_string: str, max_records: int):
    Entrez.email = "Preeti.Kochar@nih.gov"
    handle = Entrez.esearch(
        db="pubmed",
        term=search_string,
        retmax=max_records)
    result = Entrez.read(handle)["IdList"]
    handle.close()
    return result


def searchQueryStringForMeshTermIntersection(
        first_mesh_terms: List[str],
        second_mesh_terms: List[str],
        first_pub_date: Optional[datetime.date] = None,
        last_pub_date: Optional[datetime.date] = None) -> str:
    """Return the query string that would be used to search documents
    containing any of the first mesh terms and any of the second mesh
    terms"""

    def append_mh(all_terms: List[str]) -> List[str]:
        return [term + " [MH] " for term in all_terms]

    def ored_terms(all_terms: List[str]) -> str:
        return " OR ".join(append_mh(all_terms))

    def entrez_date_str(
            the_date: Optional[datetime.date],
            default: str) -> str:
        if the_date is None:
            return default
        else:
            return f"{the_date.year:04}/{the_date.month:02}/{the_date.day:02}"

    def date_term() -> str:
        first = entrez_date_str(first_pub_date, "0001/01/01")
        second = entrez_date_str(first_pub_date, "8166/12/31")
        return f" AND ({first} [PDAT] : {second} [PDAT])"

    return (f"( {ored_terms(first_mesh_terms)} ) AND "
            f"( f{ored_terms(second_mesh_terms)} ) + {date_term()}")


def getPubMedIdsForMesh(first_mesh_terms: List[str],
                        second_mesh_terms: List[str],
                        max_records: int,
                        first_pub_date: Optional[datetime.date] = None,
                        last_pub_date: Optional[datetime.date] = None):
    """Return the pubmed ids that contain any of the first mesh terms and
    any of the second mesh terms"""
    return getPubMedIds(
        searchQueryStringForMeshTermIntersection(
            first_mesh_terms, second_mesh_terms),
        first_pub_date, last_pub_date, max_records)


@attr.s
class MeshAndId:
    """PubMed Id and List of associated MeSH terms"""
    pmid: int = attr.ib()
    mesh_terms: List[str] = attr.ib(factory=list)


def meshAndIdFromMedlineRecord(record: dict) -> MeshAndId:
    """Create from a medline record. It must have a PMID field defined."""
    return MeshAndId(pmid=record["PMID"], mesh_terms=record.get("MH", []))


def getMedLineRecordChunk(pmid_list: List[str], start: int):
    """Return a generator of the 10000 (or fewer) medline records for a
    given list of pubmed ids starting at index start within the entire
    list"""
    return Medline.parse(
        Entrez.efetch(
            db="pubmed",
            id=pmid_list,
            rettype="medline",
            retstart=str(start),
            retmode="text",
            retmax="10000"))


def addMeshTermsToIds(pubmed_ids: List[str]) -> List[MeshAndId]:
    cur_start = 0
    result = []
    while(True):
        mesh_chunk = [
          meshAndIdFromMedlineRecord(record) for record in
          getMedLineRecordChunk(pubmed_ids, cur_start)
          if "PMID" in record]
        result.extend(mesh_chunk)
        if len(mesh_chunk) < 10000:
            break
    return result


def removeQualifiers(mesh_term: str) -> str:
    return mesh_term.split("/")[0].replace("*", "")


def countGroupedIds(
        term_to_groups: Dict[str, Set[str]],
        id_meshes: List[MeshAndId]) -> Dict[str, int]:
    """Return number of ids that had a mesh term that, after removing
    qualifiers, mapped to each group using the term_to_group
    dictionary Mesh terms with no group are not counted
    """
    counts = Counter()
    for m_id in id_meshes:
        clean_terms = {removeQualifiers(term) for term in m_id.mesh_terms}
        groups = Counter({group for clean_term in clean_terms
                          if clean_term in term_to_groups
                          for group in term_to_groups[clean_term]})
        counts.update(groups)
    return counts


class AutocompleteVocabulary:
    def __init__(self):
        pass

    def autocomplete(self, text: str) -> List[str]:
        return []


PRIMARY = 'primary'
SECONDARY = 'secondary'


def loadVocabulary(vocab_name: str) -> AutocompleteVocabulary:
    return AutocompleteVocabulary()
