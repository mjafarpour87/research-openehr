# ISO 13606 & openEHR Research Landscape Analysis  

### A Reproducible Bibliometric, Thematic, and Network Study (2002–2025)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Reproducibility](https://img.shields.io/badge/Reproducible-Yes-brightgreen.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## 📌 Project Description

This repository contains a fully reproducible analytical pipeline supporting the study:

> **ISO 13606 and openEHR in Health Informatics: A Bibliometric and Thematic Analysis across Three Major Databases**

The project systematically maps the evolution, structure, and global dynamics of archetype-based interoperability standards using large-scale bibliometric data.


## 🎯 Research Objectives

- Quantify publication growth and maturity of the field
- Identify influential works and citation structures
- Map global collaboration networks
- Analyze thematic evolution and research priorities
- Detect underexplored domains for future research


## 🔬 Key Features

- ✅ Multi-database integration (PubMed, Scopus, WoS)
- ✅ Metadata harmonization via OpenAlex
- ✅ Fully reproducible Jupyter-based workflow
- ✅ Hybrid thematic classification (deductive + inductive)
- ✅ Network analysis (co-authorship, co-citation, keyword)
- ✅ Publication-ready figures and metrics


## 📁 Repository Structure

```

├── data/
│   ├── dataset.json
│   ├── scimagojr 2023.csv
│
├── src/
│   ├── config.py
│   ├── lib_co_occurrence.py
│   ├── lib_dataset.py
│   ├── lib_visualization.py
│
├── output/
├── integrated_bibliometric_analysis.ipynb
├── requirements.txt
├── README.md

```

## ⚙️ Reproducibility

This project is designed for **full reproducibility**:

- Deterministic workflows
- Transparent preprocessing steps
- Modular notebook structure


### 🔁 Run the Full Pipeline

```bash
git clone https://github.com/mjafarpour87/research-openehr.git
cd research-openehr

pip install -r requirements.txt
jupyter notebook
```


## 🧪 Methodological Framework

### 📈 Bibliometric Indicators

* CAGR (Compound Annual Growth Rate)
* h-index, i10-index
* Citation distribution

### 🌐 Network Analysis

* Co-authorship networks
* Co-citation networks
* Keyword co-occurrence
* Graph metrics (centrality, clustering)

### 🧠 Thematic Modeling

Seven categories:

1. Technical Integration
2. Semantic Interoperability
3. Evaluation & Impact
4. Comparative Studies
5. Clinical Adoption
6. Governance & Ethics
7. Human Factors



## 📊 Key Insights

* 📈 Sustained growth (CAGR ≈ 8.8%)
* 🧱 Dominance of technical research (~70%)
* ⚖️ Translational imbalance (low clinical & governance focus)
* 🌍 Europe-centered research ecosystem
* 🔗 Moderate international collaboration


## 📂 Data Availability

* Aggregated datasets: ✔ Available
* Raw bibliographic data: ⚠ Restricted (database licensing)

OpenAlex metadata used for harmonization.



## 🧾 Citation

If you use this repository, please cite:

```id="citation-block"


```

## 🤝 Contribution Guidelines

We welcome contributions from the research community:

### Ways to contribute:

* Extend thematic classification
* Improve network models
* Add new datasets
* Optimize performance

### Workflow:

1. Fork repository
2. Create feature branch
3. Submit pull request


## 🔮 Future Work

* Topic modeling (NLP-based)
* Integration with HL7 FHIR studies
* Policy impact analysis
* Longitudinal citation modeling


## 📜 License

[MIT License](/LICENSE)


## 🙏 Acknowledgments

* Medical University of Vienna
* OpenAlex
* Research collaborators



## ⭐ Support

If you find this work useful:

* ⭐ Star this repository
* 🔁 Share with your network
* 📄 Cite the associated paper



