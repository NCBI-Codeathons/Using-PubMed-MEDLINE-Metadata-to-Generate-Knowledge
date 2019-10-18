# PubMed2Knowledge - Exploratory data analysis for PubMed Using MeSH
## What does PubMed2Knowledge Do?
PubMed2Knowledge (PM2K) is a tool that allows users to explore relationships between two topics of interest by leveraging PubMed citations indexed with MeSH terms.  The user can quickly learn how two topics (MeSH terms) are related across the PubMed citation corpus.
For example, suppose I wanted to know "the where" of publications about Zika virus.  In such a query, I may choose to begin my analysis by selecting one or more of the relevant MeSH terms, in this case, "Zika Virus" and "Zika Virus Infection", to create my records of interest.  Since I would like to know about geographic information among these publications, I may decide to enter "Geographic Locations" as my second input parameter.  The tool would analyze the data by quantifying the citations across the first child nodes of "Geographic Locations", which can be explored using the [Mesh Browser](https://meshb.nlm.nih.gov/search) (for this particular term, the children can be seen [here](https://meshb.nlm.nih.gov/record/ui?ui=D005842)
**PLEASE NOTE**: PubMed citations are not immediately indexed with MeSH terms, so the latest abstracts will not be included in your analysis.

## What is MeSH?
From the National Library of Medicine website: "The Medical Subject Headings (MeSH) thesaurus is a controlled and hierarchically-organized vocabulary produced by the National Library of Medicine. It is used for indexing, cataloging, and searching of biomedical and health-related information." There are plenty of resources for understanding and leveraging MeSH from the [dedicated NLM page](https://www.nlm.nih.gov/mesh/meshhome.html).  The file used in this application to make the matches between the primary and secondary topic of interest is the RDF found on the [MeSH Downloads page](https://www.nlm.nih.gov/databases/download/mesh.html) (downloaded 2019-10-16).

## Basic Workflow
1. User supplies two MeSH-based input parameters, the first is the term that generates the "anchor" search, the second is the "exploratory" parameter.
2. A PubMed is search executed via `eSearch` from the Biopython module
3. UIDs are posted to history server via `ePost`
4. The MEDLINE-formatted citations are retrieved via `eFetch`
5. A function in parallel extracts all matching MeSH terms based on paramater two, which are then used to filter the corpus set.
6. The MeSH terms from the search corpus matching paramater two are counted for their frequency in the original record set.
7. The child nodes of the exploratoary parameter are displayed in a bar chart

## Visually - What is PM2K Doing?
![alt text](/.images/search-schema.png)
> A user starts a search using a MeSH term of interest.  A corpus of citations is retrieved.  The number of those citations that intersect (match) the corpus are quantified and displayed in a chart.

## How to use PM2K
The beta web app can be found here: http://104.196.160.13/#/

![alt text](/.images/example.png)
> This figures illustrates the output for the example proposed above, displaying the regions tagged on the publications that were about Zika Virus.

## Additional Features
- The MeSH terms can be found with autocomplete after the user begins to type
- Support for Entry Terms & SCRs
- Date filtering

## Forthcoming features
- Time series analysis
- Support for publication type (PT) search
- Support PMID list upload instead of search
- Send user to PubMed to perform a search based on click on bar in output figure

## Team
- Kurtis Haro, PhD NLM/NCBI
- Eric Moyer, NLM/NCBI
- Evgeny Ivanchenko, PhD NLM/NCBI
- Victor Joukov, NLM/NCBI
- Preeti G. Kochar, PhD NLM/LO/BSD

## Architecture
    +---------+
    |         |
    | Browser |
    |         |
    +----+----+
         |
         |
         |
         v
    +----+-----+
    |          |
    |   Vue    |
    |          |
    | Frontend |
    |          |
    +----+-----+
         |
         |
         v
    +----+----+      +----------+
    |         |      |          |
    |  Flask  |      |  Entrez  |
    |         +----->+          |
    | Backend |      |  EUtils  |
    |         |      |          |
    +---+-----+      +----------+
        |
        v
    +---+----------+
    |              |
    | Preprocessed |
    | MeSH         |
    | Datafiles    |
    |              |
    |              |
    +--------------+
