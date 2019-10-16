# Using-PubMed-MEDLINE-Metadata-to-Generate-Knowledge
## MVP Descriptor
This tool allows the user to cross-examine two concepts of interest across PubMed citations using a MeSH terms of interest.  For example, suppose I wanted to know "the where" of publications about about Zika virus.  In such a query, I may choose to enter one of more the relevant MeSH terms (the MVP will support multiple MeSH terms), "Zika Virus" and "Zika Virus Infection", to build my PubMed corpus of interest.  Since I am interested in geographic information about these publications, I may wish to enter "Geographic Locations" as my second input parameter.  The tool would analyze the data by quantifying the citations across the first child nodes of "Geographic Locations", which can be explored using the [Mesh Browser](https://meshb.nlm.nih.gov/search) (for this particular term, the children can be seen [here](https://meshb.nlm.nih.gov/record/ui?ui=D005842)
## Basic Workflow
1. User supplies two MeSH-based input parameters.
2. PM search executed via `eSearch` from the Biopython module
3. UIDs are posted to history server via `ePost`
4. MEDLINE format is collected via `eFetch`
5. A function in parallel extracts  all matching MeSH terms based on paramater 2
6. The MeSH terms from the search corpus are collected and counted for their frequency in a given document compared to the item set in step 5 (i.e. a document with two matching MeSH terms from parameter 2 is counted only once if they share a parent node within the tree)
