
"""
Version: 0.0.2

"""

from collections import Counter
from itertools import chain
import sys

from src.config import DATA_DIR, DATASET_FILE
from triplea.service.repository.export.dataset import read_dataset_for_analysis

def DATASET():
    scimagojr_csv_file_path = DATA_DIR / 'scimagojr 2023.csv'

    if not scimagojr_csv_file_path.exists():
        print(
            "We need the scimagojr information. "
            "The corresponding file does not exist."
        )
        sys.exit()

    if not DATASET_FILE.exists():
        print(
            """The dataset file is required; however, it is not publicly available.
Due to licensing restrictions associated with certain databases, such as Scopus and Web of Science, access to this file is limited.
Therefore, interested individuals are advised to contact the corresponding author and submit a formal request via email to obtain the dataset."""
        )
        sys.exit()

    # Load, clean, normalize ISSNs, and enrich records with Scimago metadata.
    df = read_dataset_for_analysis(
        DATASET_FILE,
        scimagojr_csv_file_path
    )

    # Keep only publications included in the final corpus.
    filtered_df = df[
        df['inclusion_Decision_v4'] == 'Include'
    ].copy()

    # Remove fields that will be replaced by the final normalized versions.
    filtered_df = filtered_df.drop(
        columns=[
            'citation_count',
            'affiliation_integration_country',
            'DEFA_assigned_category_v3',
        ]
    )

    # Rename the final variables used in the analyses.
    filtered_df = filtered_df.rename(
        columns={
            'alex_cited': 'citation_count',
            'alex_affiliation_integration_country': 'affiliation_country',
            'DEFA_assigned_category_v4': 'DEFA_assigned_category_v3',
        }
    )

    # ------------------------------------------------------------------
    # Canonicalize journal titles using the canonical ISSN.
    #
    # journal_issn has already been normalized and canonicalized before
    # this stage. Therefore, publications sharing the same canonical ISSN
    # must also share one journal title in all downstream analyses.
    #
    # Records without a valid ISSN are NOT grouped together; their
    # existing journal titles are preserved.
    # ------------------------------------------------------------------

    # Clean journal-title formatting.
    filtered_df['journal_title'] = (
        filtered_df['journal_title']
        .astype('string')
        .str.strip()
        .str.replace(r'\s+', ' ', regex=True)
    )

    # Identify records that have a valid canonical ISSN.
    valid_issn = (
        filtered_df['journal_issn'].notna()
        & filtered_df['journal_issn']
            .astype('string')
            .str.strip()
            .ne('')
    )

    # Determine one reproducible journal title for each canonical ISSN.
    #
    # The most frequently occurring enriched journal title is selected.
    # In the rare case of a tie, the alphabetically first title is used
    # to keep the result deterministic.
    canonical_titles = (
        filtered_df.loc[
            valid_issn
            & filtered_df['journal_title'].notna()
            & filtered_df['journal_title'].ne(''),
            ['journal_issn', 'journal_title']
        ]
        .groupby('journal_issn')['journal_title']
        .agg(
            lambda s: sorted(
                s.mode().astype(str).tolist()
            )[0]
        )
    )

    # Assign the same canonical title to all records sharing
    # the same canonical ISSN.
    mapped_titles = (
        filtered_df.loc[valid_issn, 'journal_issn']
        .map(canonical_titles)
    )

    # Replace journal_title only when a canonical title is available.
    has_canonical_title = mapped_titles.notna()

    filtered_df.loc[
        mapped_titles.index[has_canonical_title],
        'journal_title'
    ] = mapped_titles[has_canonical_title]

    # ------------------------------------------------------------------
    # The source database uses the field name 'publisher' for the
    # journal/source title rather than the publishing company.
    #
    # Keep it synchronized with journal_title so that legacy analyses
    # still using df['publisher'] also operate on the canonical title.
    # ------------------------------------------------------------------
    filtered_df['publisher'] = filtered_df['journal_title']

    return filtered_df

def clean_topics(
    df,
    unwanted_keywords,
    keyword_map=None,
    min_freq=0,
    min_freq_doc=0
):
    # Ensure sets/dicts for fast membership checks
    unwanted_keywords = set(unwanted_keywords)
    keyword_map = keyword_map or {}

    # 1) Preprocess: lowercase + strip + map + remove unwanted
    def preprocess_keywords(lst):
        result = []
        append = result.append  # local reference for speed
        for kw in lst:
            kw_clean = kw.lower().strip()
            kw_clean = keyword_map.get(kw_clean, kw_clean)
            if kw_clean and kw_clean not in unwanted_keywords:
                append(kw_clean)
        return result

    df["topics"] = df["topics"].apply(preprocess_keywords)

    # If no filtering is required, return early
    if not min_freq and not min_freq_doc:
        return df

    # 2) Term frequency filtering (global frequency)
    allowed_tf = None
    if min_freq:
        all_keywords = chain.from_iterable(df["topics"])
        freq = Counter(all_keywords)
        allowed_tf = {kw for kw, c in freq.items() if c >= min_freq}

    # 3) Document frequency filtering
    allowed_df = None
    if min_freq_doc:
        doc_freq = Counter()
        for lst in df["topics"]:
            doc_freq.update(set(lst))  # count each keyword once per document
        allowed_df = {kw for kw, c in doc_freq.items() if c >= min_freq_doc}

    # 4) Apply both filters (if enabled)
    def filter_keywords(lst):
        if allowed_tf is not None:
            lst = [kw for kw in lst if kw in allowed_tf]
        if allowed_df is not None:
            lst = [kw for kw in lst if kw in allowed_df]
        return lst

    df["topics"] = df["topics"].apply(filter_keywords)

    return df


def clean_keywords(
    df,
    unwanted_keywords,
    keyword_map=None,
    min_freq=0,
    min_freq_doc=0
):
    # Ensure sets/dicts for fast membership checks
    unwanted_keywords = set(unwanted_keywords)
    keyword_map = keyword_map or {}

    # 1) Preprocess: lowercase + strip + map + remove unwanted
    def preprocess_keywords(lst):
        result = []
        append = result.append  # local reference for speed
        for kw in lst:
            kw_clean = kw.lower().strip()
            kw_clean = keyword_map.get(kw_clean, kw_clean)
            if kw_clean and kw_clean not in unwanted_keywords:
                append(kw_clean)
        return result

    df["keywords"] = df["keywords"].apply(preprocess_keywords)

    # If no filtering is required, return early
    if not min_freq and not min_freq_doc:
        return df

    # 2) Term frequency filtering (global frequency)
    allowed_tf = None
    if min_freq:
        all_keywords = chain.from_iterable(df["keywords"])
        freq = Counter(all_keywords)
        allowed_tf = {kw for kw, c in freq.items() if c >= min_freq}

    # 3) Document frequency filtering
    allowed_df = None
    if min_freq_doc:
        doc_freq = Counter()
        for lst in df["keywords"]:
            doc_freq.update(set(lst))  # count each keyword once per document
        allowed_df = {kw for kw, c in doc_freq.items() if c >= min_freq_doc}

    # 4) Apply both filters (if enabled)
    def filter_keywords(lst):
        if allowed_tf is not None:
            lst = [kw for kw in lst if kw in allowed_tf]
        if allowed_df is not None:
            lst = [kw for kw in lst if kw in allowed_df]
        return lst

    df["keywords"] = df["keywords"].apply(filter_keywords)

    return df



def keyword_map():
    return {
    "ehr":"EHR",
    "electronic health records":"EHR",
    "electronic health record":"EHR",
    "archetypes": "archetype",
    "access-control": "access control",
    "acute respiratory infection (ari)": "acute respiratory infection",
    "ambient assisted living (aal)":"ambient assisted living",
    "algorithms":"algorithm",
    "archetyp":"archetype",
    "architectural styles":"architectural style",
    "best-practices":"best practices",
    "block-chain":"blockchain",
    "breast-cancer":"breast cancer",
    "business-intelligence":"business intelligence",
    "care pathways":"care pathway",
    "cda(clinical document architecture)":"cda",
    "clinical decision support system (cdss)":"clinical decision support system",
    "clinical decision support systems":"clinical decision support system",
    "clinical decision-support systems":"clinical decision support system",
    "clinical domain models":"clinical element model",
    "clinical guidelines":"clinical guideline",
    "clinical information models":"clinical information model",
    "clinical models":"clinical model",
    "clinical practice guidelines":"clinical practice guideline",
    "clinical registries":"clinical repository",
    "clinical research (cr)":"clinical research",
    "clinical trials":"clinical trial",
    "clinical workflows":"clinical workflow",
    "common data elements":"common data element",
    "computer-interpretable guidelines":"computer-interpretable guideline",
    "conditional random fields":"conditional random field",
    "congestive heart failures":"congestive heart failure",
    "continuity of care record (ccr)":"continuity of care record",
    "continuity of care records":"continuity of care record",    
    "continuity of cares":"continuity of care",
    "crowd sourced":"crowdsourcing",
    "data set":"dataset",
    "data sets":"dataset",
    "data warehouses":"data warehouse",
    "data warehousing":"data warehouse",
    "database management systems":"database management system",
    "decision support systems":"decision support system",
    "decision-support-systems":"decision support system",
    "domain specific languages":"domain specific language",
    "domain-specific language":"domain specific language",
    "dual-model approach":"dual model approach",  
    "e health":"ehealth",
    "e-health":"ehealth",
    "ehrs":"EHR",
    "ehr (electronic health record)":"EHR",
    "electronic health care record (ehr)":"EHR",
    "electronic health cares":"electronic health care",
    "electronic health record - ehr":"EHR",  
    "electronic health record (ehr)":"EHR",
    "electronic health record (ehrs)":"EHR",
    "electronic health record systems":"electronic health record system",
    "electronic health record(ehr) system":"electronic health record system",
    "electronic health records (ehr)":"EHR",   
    "electronic health records (ehrs)":"EHR",
    "electronic healthcare record":"EHR",
    "electronic healthcare record (ehr)":"EHR",   
    "electronic healthcare records":"EHR",
    "electronic medical records (emr)":"electronic medical record",
    "electronic patient records":"electronic patient record",   
    "electronic prescribing":"electronic prescription",
    "electronic prescription (ep)":"electronic prescription",
    "eletronic health record":"EHR",   
    "e-mail":"electronic mail",
    "en13606":"en 13606",
    "en13606 standard":"en 13606",   
    "errors":"error",
    "graph databases":"graph database",
    "graphical user interfaces":"graphical user interface",   
    "graphical user interfaces (gui)":"graphical user interface",
    "gui":"graphical user interface",   
    "guideline representation languages":"guideline representation language",
    "guidelines":"guideline",   
    "health information system (his)":"health information system",
    "health information systems":"health information system",   
    "health level 7 (hl7)":"health level 7",
    "health level seven":"health level 7",   
    "health practitioners":"health practitioner",
    "health professionals":"health professional",   
    "health records":"health record",
    "health-care":"healthcare",   
    "healthcare processes":"healthcare process",
    "healthcare standards":"healthcare standard",   
    "health-care system":"healthcare system",
    "healthcare systems":"healthcare system",   
    "heart rate turbulences":"heart rate turbulence",
    "hl7":"health level 7",   
    "hospital information systems":"hospital information system",   
    "his":"hospital information system",
    "identification (control systems)":"identification",   
    "information systems":"information system",
    "information-technology":"information technology",
    "internet architectures":"internet architecture",   
    "iso 13606 standard":"iso 13606",
    "iso 13606; openehr":"iso 13606",   
    "iso 3606":"iso 13606",
    "iso en 13606":"iso 13606", 
    "iso en13606 standard":"iso 13606",   
    "iso/cen 13606":"iso 13606",
    "iso/en 13606":"iso 13606", 
    "iso/en 13606 standard":"iso 13606",   
    "knowledge graphs":"knowledge graph",
    "knowledge representation (computer)":"knowledge representation", 
    "knowledge-representation":"knowledge representation",   
    "m2m":"m2m communication",
    "m2m communications":"m2m communication", 
    "machine to machine (m2m)":"m2m communication",
    "machine-to-machine":"m2m communication", 
    "machine-to-machine (m2m) communications":"m2m communication",
    "machine-to-machine communication":"m2m communication", 
    "machine-to-machine communications":"m2m communication",
    "maternal health services":"maternal health service", 
    "medical computer systems":"medical computer system",
    "medical information systems":"medical information system", 
    "medical ontologies":"medical ontology", 
    "medical records systems":"medical records system",
    "medical records systems, computerized":"medical records system", 
    "memory disorders":"memory disorder", 
    "multi-agent system":"multi agent system",
    "multi agent systems":"multi agent system", 
    "multi agent system (mas)":"multi agent system", 
    "nosql":"nosql database",
    "nosql databases":"nosql database", 
    "ontologies":"ontology", 
    "omop cdm":"omop",
    "ontology's":"ontology", 
    "open source software":"open source", 
    "open sources":"open source",
    "openehr archetypes":"archetype", 
    "openehr archetype":"archetype", 
    "openehr clinical archetypes":"archetype", 
    "open-source":"open source", 
    "open-source software":"open source", 
    "practice guidelines":"practice guideline", 
    "primary health care":"primary healthcare", 
    "service oriented architecture (soa)":"service oriented architecture", 
    "service oriented frameworks":"service oriented architecture", 
    "service-oriented architecture":"service oriented architecture", 
    "snomed":"snomed ct", 
    "snomed-ct":"snomed ct", 
}


def unwanted_keywords():
    return  {
        "humans",
        # "reproducibility of results",
        # "retrospective studies",
        # "female",
        # "child",
        # "language",
        # "workflow",
        "italy",
        "bmj health informatics",
        

        "openehr",
        "australia",
        "austria",
        "brazil",
        "bulgaria",
        "china",
        "cleveland",
        "colombia",
        "czech republic",
        "denmark",
        "ecuador",
        "europe",
        "european countries",
        "european union",
        "germany",
        "global trends",
        "health regions",
        "iran",
        "ireland",
        "japan",
        "london",
        "netherlands",
        "nordic",
        "norway",
        "pakistan",
        "portugal",
        "republic of korea",
        "romania",
        "romanians",
        "russia",
        "scandinavian countries",
        "scotland",
        "singapore",
        "slovenia",
        "spain",
        "sweden",
        "united kingdom",
        "united states",
    }



COUNTRY_ALIASES = {

    # United States
    "usa": "United States",
    "u.s.a.": "United States",
    "u.s.": "United States",
    "us": "United States",
    "united states of america": "United States",

    # United Kingdom
    "uk": "United Kingdom",
    "u.k.": "United Kingdom",
    "great britain": "United Kingdom",
    "england": "United Kingdom",
    "scotland": "United Kingdom",
    "wales": "United Kingdom",
    "northern ireland": "United Kingdom",

    # Korea
    "korea": "Korea, Republic of",
    "south korea": "Korea, Republic of",
    "republic of korea": "Korea, Republic of",
    "korea south": "Korea, Republic of",

    "north korea": "Korea, Democratic People's Republic of",
    "democratic people's republic of korea":
        "Korea, Democratic People's Republic of",

    # Russia
    "russia": "Russian Federation",

    # Iran
    "iran": "Iran, Islamic Republic of",

    # Türkiye
    "turkey": "Türkiye",
    "turkiye": "Türkiye",

    # Vietnam
    "vietnam": "Viet Nam",

    # Taiwan
    "taiwan": "Taiwan, Province of China",

    # Czech Republic
    "czech republic": "Czechia",

    # Bolivia
    "bolivia": "Bolivia, Plurinational State of",

    # Tanzania
    "tanzania": "Tanzania, United Republic of",

    # Syria
    "syria": "Syrian Arab Republic",

    # Laos
    "laos": "Lao People's Democratic Republic",

    # Moldova
    "moldova": "Moldova, Republic of",

    # Venezuela
    "venezuela": "Venezuela, Bolivarian Republic of",

    # Brunei
    "brunei": "Brunei Darussalam",

    # Palestine
    "palestine": "Palestine, State of",
}


DISPLAY_NAMES = {

    "KOR": "South Korea",

    "PRK": "North Korea",

    "RUS": "Russia",

    "IRN": "Iran",

    "TUR": "Türkiye",

    "VNM": "Vietnam",

    "TWN": "Taiwan",

    "BOL": "Bolivia",

    "TZA": "Tanzania",

    "SYR": "Syria",

    "LAO": "Laos",

    "MDA": "Moldova",

    "VEN": "Venezuela",

    "BRN": "Brunei",

    "PSE": "Palestine",
}