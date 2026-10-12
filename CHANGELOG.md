# Changelog
All notable changes to this project will be documented in this file.
We use [Semantic Versioning](https://semver.org/)


## Task


## [v2.0.4] - 2026-10-04
- Change output images format


## [v2.0.3] - 2026-09-09
- Change the code based on the reviewer's feedback

## [v2.0.2] - 2026-04-17
- Update Cartogram
- Update Font in `journal_productivity_vs_citation_impact.png` and `thematic_strategic_diagram_category_based.png`



## [v2.0.1] - 2026-04-10
- Update `README.md`
- Update `DATASET` function
- Remove `output/*` from `.gitignore`
- Finalize `requirements.txt`

## [v2.0.0] - 2026-03-09

### Added

#### Bibliometric Analysis
- Implemented integrated bibliometric indicators including:
  - Publication output per year
  - Compound Annual Growth Rate (CAGR)
  - Total, mean, and median citation counts
  - h-index calculation
- Added collaboration metrics:
  - International collaboration rate
  - Country-level coverage
- Added source coverage metrics (number of journals)



#### Citation Analysis
- Implemented normalized citation impact:
  - Citations per year (age-adjusted)
  - Yearly aggregation (mean and median)
- Added dual-axis visualization combining:
  - Publication count
  - Normalized citation impact



#### Thematic Analysis
- Implemented thematic category distribution analysis
- Added cross-national thematic distribution
- Computed Shannon diversity index over time
- Added decomposition of thematic diversity into:
  - Richness (number of active themes)
  - Evenness (distribution balance)



#### Advanced Thematic Modeling
- Implemented thematic strategic diagram:
  - Keyword-based version (community detection)
  - Category-based version (DEFA_assigned_category_v3)
- Computed centrality and density for thematic positioning
- Classified themes into:
  - Motor themes
  - Basic themes
  - Niche themes
  - Emerging/declining themes



#### Temporal Analysis
- Implemented temporal trends of high-frequency keywords:
  - Normalized yearly frequencies
  - Keyword standardization using `keyword_map`
  - Removal of non-informative terms using `unwanted_keywords`
- Replaced line charts with bubble chart visualization for improved interpretability


#### Emerging Trend Detection
- Implemented top growing keywords:
  - Linear trend estimation (slope-based ranking)
  - Filtering by minimum frequency and temporal presence
- Implemented keyword burst detection using Kleinberg algorithm:
  - Poisson-based burst modeling
  - Multi-state burst detection
  - Extraction of burst intervals and strengths
  - Timeline visualization of burst periods



#### Network and Structural Analysis
- Implemented keyword co-occurrence network (VOSviewer-compatible)
- Added three-field plot:
  - Authors – Keywords – Journals
  - Weighted co-occurrence relationships
- Implemented thematic co-occurrence structures and evolution analysis



#### Visualization Enhancements
- Added stacked area chart for temporal thematic distribution
- Improved plotting consistency and readability across all figures
- Standardized figure export (PNG + HTML where applicable)
- Introduced bubble charts for temporal keyword dynamics


#### Data Processing Improvements
- Standardized keyword normalization pipeline using:
  - `keyword_map`
  - `unwanted_keywords`
- Improved data cleaning:
  - Safe parsing of list-like fields
  - Deduplication while preserving order
- Ensured consistency across all analyses (keywords, categories, networks)



#### Reproducibility
- Structured analysis into modular notebook sections:
  - Growth indicators
  - Citation indicators
  - Collaboration indicators
  - Thematic analysis
- Exported all intermediate datasets to CSV for transparency and reuse



### Notes
- Analysis covers publications up to the end of 2025
- All metrics are based on harmonized multi-database records (PubMed, Scopus, Web of Science via OpenAlex)
- The workflow is designed for full reproducibility and extension


## [v1.0.0] - 2025-07-11

### Improvements
- Initial Project

### Bug Fixes