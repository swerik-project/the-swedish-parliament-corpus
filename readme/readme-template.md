[![Perform unit tests](https://github.com/swerik-project/riksdagen-records/actions/workflows/push.yml/badge.svg)](https://github.com/swerik-project/riksdagen-records/actions/workflows/push.yml)
[![Validate Parla-Clarin XML](https://github.com/swerik-project/riksdagen-records/actions/workflows/validate.yml/badge.svg)](https://github.com/swerik-project/riksdagen-records/actions/workflows/validate.yml)


# Swedish parliamentary proceedings --- 1867--today --- {Version}

_Westac Project_, 2020--2024 |
_Swerik Project_, 2023--2025


## The data set

The full data set consists of multiple parts:

- ```records.zip``` -- Parliamentary records (riksdagens protokoll) from 1867 until today in the [Parla-clarin](https://github.com/clarin-eric/parla-clarin) format
- ```metadata.zip``` -- Comprehensive list of members of parliament, ministers and governments during this period + associated metadata (mandate periods, party info, etc)
- ```dumps.zip``` -- various files containing merged / filtered / wrangled (meta)data
- [In progress] -- An annotated catalog of motions submitted to the parliament with linked metadata


## Basic use

Get the most recent version of the data can be found [here](https://github.com/swerik-project/the-swedish-parliament-corpus/releases/). It has the following structure

- Annual Parliamentary record (protocol) files organized in subdirectories according to parliament years
- Structured metadata on members of parliament, ministers, and governments

Archives (```.zip``` files) can be downloaded, extracted, and used in whatever way. We offer some examples and tools for working with the corpus in Python and R.


### Pyriksdagen: a Python module

[Pyriksdagen](https://github.com/swerik-project/pyriksdagen) is a Python module developed in parallel with the corpus, designed spedifically for working with the corpus. It can be installed via [PyPi](https://pypi.org/project/pyriksdagen/) in the ordinary way

   (venv) ~$  pip install pyriksdagen

A simple workflow is demonstrated in [this Google Colab notebook](https://colab.research.google.com/drive/1C3e2gwi9z83ikXbYXNPfB6RF7spTgzxA?usp=sharing).

### rcr: an R module

There's an R package; to install, run:

```
library(remotes)
remotes::install_github('swerik-project/rcr')
```

As a first step, we point to the directory where the corpus files are stored.

	set_riksdag_corpora_path("[THE PATH TO THE CORPORA HERE]")

To extract speeches, we use ```extract_speeches_from_records()```. Below is an example that assumes that the corpora path has been set and extracts the speeches from three different records.

```
fps <-
  c("protocols/1896/prot-1896--ak--042.xml",
    "protocols/1951/prot-1951--fk--029.xml",
    "protocols/1975/prot-1975--036.xml")
sp <- extract_speeches_from_records(fps)
```

## Design choices of the project

The Riksdagen corpus is released as an iterative process, where the corpus is continuously curated and expanded. Semantic versioning is used for the whole corpus, following the established major-minor-patch practices as they apply to data. For each major and minor release, a battery of unit tests are run and a statistical sample is drawn, annotated and quantitatively evaluated to ensure integrety and quality of updated data. Errors are fixed as they are detected in order of priority. Moreover, the edit history is kept as a traceable git repository.

While the contents of the corpus will change due to curation and expansion, we aim to keep the deliverable API, the `corpus/` folder, as stable as possible. This means we avoid relocating files or folders, changing formats, changing columns in metadata files, or any other changes that might break downstream scripts. Conversely, files outside the `corpus/` folder are internal to the project. End users may find utility in them but we make no effort to keep them consistent.

The data in the corpus is delivered as TEI XML files to follow established practices. The metadata is delivered as CSV files, following a [normal form](https://en.wikipedia.org/wiki/Database_normalization) database structure while allowing for a legible git history. A more detailed description of the data and metadata structure and formats can be found in the README files in the `corpus/` folder.

## Documentation

Documentation and example usage of Pyriksdagen and rcr can be found in their respective repositories [¿add links?]. Additionally some documentation about the curation process can be found in the scripts repo [¿link?].

## Descriptive statistics at a glance

Currently, we have an extensive set of Parliamentary Records (Riksdagens Protokoll) from 1867 until now. We are in the process of preparing Motions for inclusion in the corpus and other document types will follow.

{sumstats_table}

\* Digital original parliamentary records for some years in the 1990s are not paginated and thus do not contribute to the page count.See also §_Number of Pages in Parliamentary Records_.

### Parliamentary Records over time

#### Number of Parliamentary Records

![Number of Parliamentary Records](plots/n-prot.png)

#### Number of Pages in Parliamentary Records

![Number of Pages in Parliamentary Records](plots/prot-pages.png)

#### Number of Speeches in Parliamentary Records

![Number of Speeches in Parliamentary Records](plots/prot-speeches.png)


#### Number of Words in Parliamentary Records

![Number of Words in Parliamentary Records](plots/prot-words.png)

### Members of Parliament over time

![Members of Parliament over time](plots/mp-coverage.png)

## Quality assessment

### Speech-to-speaker mapping

We check how many speakers in the parliamentary records our algorithms idenify in each release. 

![Estimate of mapping accuracy](https://raw.githubusercontent.com/welfare-state-analytics/riksdagen-corpus/main/input/accuracy/version_plot.png)

### Correct number of MPs over time

![Ratio of MP to seats over time](plots/mp-coverage-ratio.png)


## Participate!

If you would like to participate in the curation or quality control of data contained in the Swedish Parliament Corpus, please [be in touch](https://github.com/orgs/swerik-project/discussions)!

## Acknowledgement of support

- Westac funding: Vetenskapsrådet 2018-0606

- Swerik funding:Riksbankens Jubileumsfond IN22-0003

<img src="scripts/stats-dashboard/figures/logos/rj.png" width="250"/>
<img src="scripts/stats-dashboard/figures/logos/vr.png" width="250"/>

---
Last update: {Updated}
