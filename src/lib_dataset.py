
"""
Version: 0.0.2

"""

from collections import Counter
from itertools import chain

from src.config import DATA_DIR, DATASET_FILE
from triplea.service.repository.export.dataset import read_dataset_for_analysis

def DATASET():
    scimagojr_csv_file_path = DATA_DIR / 'scimagojr 2023.csv'
    df = read_dataset_for_analysis(DATASET_FILE, scimagojr_csv_file_path)
    return df


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
    "ehr": "electronic health record",
    "electronic health records": "electronic health record",
    "archetypes": "archetype",
    "e-health": "electronic health",
}


def unwanted_keywords():
    return  {
        "humans",
        "reproducibility of results",
        "retrospective studies",
        "female",
        "child",
        "language",
        "workflow",
        "metadata",
        "aged",
        


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