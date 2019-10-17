# PubMed2Knowledge - Exploratory data analysis for PubMed Using MeSH
## What does PubMed2Knowledge Do?
PubMed2Knowledhe (PM2K) is tool that allows the users to explore relationships between two topics of interest by leveraging PubMed citations indexed with MeSH terms.  The user can quickly learn how two topics (MeSH terms) are related across the PubMed citation corpus.
For example, suppose I wanted to know "the where" of publications about about Zika virus.  In such a query, I may choose to begin my analysis by selecting one of more the relevant MeSH terms, in this case, "Zika Virus" and "Zika Virus Infection", to build my PubMed corpus of interest.  Since I am interested in geographic information about these publications, I may wish to enter "Geographic Locations" as my second input parameter.  The tool would analyze the data by quantifying the citations across the first child nodes of "Geographic Locations", which can be explored using the [Mesh Browser](https://meshb.nlm.nih.gov/search) (for this particular term, the children can be seen [here](https://meshb.nlm.nih.gov/record/ui?ui=D005842)
**PLEASE NOTE**: PubMed citations are not immediately indexed with MeSH terms, so the latest abstracts will not be included in your analysis.

## What is MeSH?
From the National Library of Medicine website: "The Medical Subject Headings (MeSH) thesaurus is a controlled and hierarchically-organized vocabulary produced by the National Library of Medicine. It is used for indexing, cataloging, and searching of biomedical and health-related information." There are plenty of resources for understanding and leveraging MeSH from the [dedicated NLM page](https://www.nlm.nih.gov/mesh/meshhome.html).  The file used in this application is the RDF found on the [MeSH Downloads page](https://www.nlm.nih.gov/databases/download/mesh.html) (downloaded 2019-10-16).

## Basic Workflow
1. User supplies two MeSH-based input parameters, the first is the "anchor" search, the second is the "exploratory" parameter.
2. A PubMed is search executed via `eSearch` from the Biopython module
3. UIDs are posted to history server via `ePost`
4. MEDLINE format is collected via `eFetch`
5. A function in parallel extracts  all matching MeSH terms based on paramater 2 which are used to filter the corpus set.
6. The MeSH terms from the search corpus matching paramater two are counted for their frequency in the anchor search.
7. The child nodes of the exploratoary parameter are displayed in a bar chart

## Visually - What is PM2K Doing?
![alt text](/.images/search-schema.png)
A user starts a search using a MeSH term of interest.  A corpus of citations is retrieved.  The number of those citations that intersect (match) the corpus are quantified and displayed in a chart.

## How to use PM2K
Beta app can be found here: http://104.196.160.13/#/

![alt text](/.images/mockup.png)

## Using Locally
For exploratory and developmental work, we have provided a PM2K development notebook.  To use, create a Python 3.6 virtual environment (or use a conda installation) and install the requirements.txt file before launching your notebook

```
conda create --name py36 python=3.6
source activate py36
conda install --file requirements.txt
jupyter-notebook
```
## Forthcoming features
- Autocomplete
- Support for Entry Terms & SCRs
- Support PMID list upload instead of search
- Time series analysis

## Team
- Kurtis Haro, PhD NLM/NCBI
- Eric Moyer, PhD NLM/NCBI
- Evgeny Ivanchenko, NLM/NCBI
- Victor Joukov, NLM/NCBI
- Preeti G. Kochar, PhD NLM/LO/BSD
