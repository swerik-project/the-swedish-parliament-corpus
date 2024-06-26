#!/usr/bin/env python3
"""
Generates a dynamic markdown file for the repo's main README.
    - generate variable dict
    - reads in readme-template.txt
    - substitutess variables
    - writes README.md
"""
from datetime import datetime
from lxml import etree
from py_markdown_table.markdown_table import markdown_table
from pyriksdagen.utils import (
    elem_iter,
    get_data_location,
    parse_protocol,
    protocol_iterators,
)
from tqdm import tqdm
import argparse
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import pandas as pd
import re, subprocess


now = datetime.now()
corpus_paths = {
    "protocols_path": os.environ.get("RECORDS_PATH", 'data'),
    "metadata_path": os.environ.get("METADATA_PATH", 'data')
}
md_row_names = {
    "-": "",
    "corpus_size": "Corpus size (GB)",
    "N_prot": "Number of parliamentary records",
    "N_prot_pages": "Total parliamentary record pages*",
    "N_prot_speeches": "Total parliamentary record speeches",
    "N_prot_words": "Total parliamentary record words",
    "N_mot": "Number of Motions",
    "N_mot_pages": "Total motion pages",
    "N_mot_words": "Total motion words",
    "N_MP": "Number of people with MP role",
    "N_MIN": "Number of people with minister role"
}




def render_markdown(renderd):
    with open(f"readme/readme-template.md", 'r') as inf:
        template = inf.read()
    readme = template.format(**renderd)
    with open(f"README.md", 'w+') as out:
        out.write(readme)
    return True


def mk_table_data(df):
    table_data = []
    D = {}
    version = sorted(list(set([v for v in df['version'] if "rc" not in v])), key=lambda s: list(map(int, s[1:].split('.'))), reverse=True)
    cols = [c for c in df.columns if c != "version"]
    for v in version[:3]:
        dfv = df.loc[df["version"]==v].copy()
        dfv.reset_index(inplace=True, drop=True)
        for col in cols:
            if col not in D:
                D[col] = {}
            D[col][v] = dfv.at[0, col]
    for k, v in D.items():
        n = {'': md_row_names[k]}
        n.update(v)
        table_data.append(n)
    return table_data


def calculate_corpus_size():
    """
    Calculate the corpus size in GB
    """
    print("Calculating corpus size...")
    corpus_size = 0
    for k, v in corpus_paths.items():
        for dirpath, dirnames, filenames in os.walk(v):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                if not os.path.islink(fp):
                    corpus_size += os.path.getsize(fp)
    fsize = "%.2f" % (corpus_size / (1024 * 1024 * 1024)) # converts size to gigabytes
    print(f"...{fsize} GB")
    return fsize


def count_pages_speeches_words(protocol):
    """
    Count pages (\<pb> elems) in protocols and words.
    """
    pages, speeches, words = 0,0,0
    root, ns = parse_protocol(protocol, get_ns = True)
    for tag, elem in elem_iter(root):
        if tag == "u":
            for segelem in elem:
                words += len([_.strip() for _ in segelem.text.split(' ') if len(_) > 0 and _ != '\n'])
        elif tag in ["note"]:
            if 'type' in elem.attrib:
                if elem.attrib['type'] == 'speaker':
                    speeches += 1
    pages = len(root.findall(f".//{ns['tei_ns']}pb"))
    print(pages, speeches, words)
    return pages, speeches, words


def infer_year(protocol):
    return int(protocol.split('/')[-1].split('-')[1][:4])


def calculate_prot_stats():
    """
    Counts protocol docs, number of pages, and words
    """
    print("Calculating protocol summary statistics...")
    D = {"records":{}, "pages":{}, "speeches": {}, "words":{}}
    N_prot, N_prot_pages, N_prot_speeches, N_prot_words = 0,0,0,0
    protocols = sorted(list(protocol_iterators(
                                get_data_location("records"),
                                start=1867, end=2023)))
    for protocol in tqdm(protocols, total=len(protocols)):
        prot_year = infer_year(protocol)
        if prot_year not in D["records"]:
            D["records"][prot_year] = 0
            D["pages"][prot_year] = 0
            D["speeches"][prot_year] = 0
            D["words"][prot_year] = 0
        N_prot += 1
        D["records"][prot_year] += 1
        pp, sp, pw = count_pages_speeches_words(protocol)
        N_prot_pages += pp
        D["pages"][prot_year] += pp
        N_prot_speeches += sp
        D["speeches"][prot_year] += sp
        N_prot_words += pw
        D["words"][prot_year] += pw

    print(f"...{N_prot} protocols, {N_prot_pages} protocol pages, {N_prot_words} protocol words")
    return N_prot, N_prot_pages, N_prot_speeches, N_prot_words, D


def calculate_mot_stats():
    """
    Calculate N motions, N motion pages and N motion words
    """
    print("Calculating motion summary statistics...")
    print("...this function hasn't been written yet, return 0,0,0")
    N_mot, N_mot_pages, N_mot_words = 0,0,0
    return N_mot, N_mot_pages, N_mot_words


def count_MP():
    """
    Counts N unique MEPs (unique wiki id's) in the MP database
    """
    print("Counting MPs (unique people w/ role)...")
    N_MP = 0
    df = pd.read_csv(f"{get_data_location('metadata')}/member_of_parliament.csv")
    N_MP = len(df["person_id"].unique())
    print(f"... {N_MP} individuals have a 'member of parliament' role")
    return N_MP


def count_MIN():
    """
    Counts ministers in the metadata
    """
    print("Counting ministers (unique people with role)...")
    N_MIN = 0
    df = pd.read_csv(f"{get_data_location('metadata')}/minister.csv")
    N_MIN = len(df["person_id"].unique())
    print(f"... {N_MIN} individuals have a 'minister' role")
    return N_MIN


def gen_prot_plot(df, path, title_string, ylab):
    scales = {
        "Words":1e6,
        "Pages":1e3,
        "Speeches":1e3,
        "Records":1
    }
    labels = {
        "Words":"M",
        "Pages":"k",
        "Speeches":"k",
        "Records":""
    }
    path_dir = "plots"#os.path.dirname(path)
    fig_name = os.path.basename(path).split('.')[0]
    versions = df.columns
    versions = [v for v in versions if "rc" not in v]
    versions = sorted(set(versions), key=lambda v: list(map(int, v[1:].split('.'))), reverse=True)
    versions = versions[:4]
    df = df[versions]
    p, a = plt.subplots()
    a.plot(df)
    lines = a.get_children()
    for i, l in enumerate(lines, -len(lines)):
        l.set_zorder(abs(i))
    plt.title(title_string)
    plt.legend(versions, loc ="upper left")
    a.set_xlabel('Year')
    a.set_ylabel(ylab)
    ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}{1}'.format(x/scales[ylab], labels[ylab]))
    a.yaxis.set_major_formatter(ticks_y)
    plt.savefig(f"{path_dir}/{fig_name}.png")


def update_version_d(args):
    if os.path.exists("stats/version-compatibility/versions.json"):
        with open("stats/version-compatibility/versions.json", 'r') as inf:
            version_d = json.load(inf)
    else:
        version_d = {}
        if not os.path.exists("stats/version-compatibility"):
            os.mkdir("stats/version-compatibility")
    version_d[args.version] = {
            "pyriksdagen": args.pyriksdagen_version,
            "riksdagen-persons": args.persons_version,
            "riksdagen-records": args.records_version,
        }
    with open("stats/version-compatibility/versions.json", 'w+') as outf:
        json.dump(version_d, outf, ensure_ascii=False, indent=4)
    return version_d


def versions_table(versions_d):
    cols = ["Dated Release", "Reoisitory Versions"]
    ds = []
    versions_d = dict(sorted(versions_d.items(), reverse=True))
    for version, version_info in versions_d.items():
        if "rc" not in version:
            ds.append({"Dated Release": version, "Repository Versions":'<br>'.join([f"{k}: {v}" for k,v in version_info.items()])})
    return markdown_table(ds).set_params(
                                    quote=False,
                                    padding_width=3,
                                    row_sep="markdown").get_markdown()




def main(args):
    print(f"CALUCLATING SUMSTATS FOR {args.version}")
    print("---------------------------------")
    version_d = update_version_d(args)
    new_version_row = [args.version]
    new_version_row.append(calculate_corpus_size())
    prot_stats = calculate_prot_stats()
    prot_d = prot_stats[4]
    [new_version_row.append(_) for _ in prot_stats[:4]]
    [new_version_row.append(_) for _ in calculate_mot_stats()]
    new_version_row.append(count_MP())
    new_version_row.append(count_MIN())

    # Update running stats
    running_stats = pd.read_csv("stats/descr_stats_version.csv")
    running_stats.drop(running_stats[running_stats.version == args.version].index, inplace=True)
    running_stats.reset_index(inplace=True, drop=True)
    running_stats.loc[len(running_stats)] = new_version_row
    running_stats.to_csv("stats/descr_stats_version.csv", index=False)

    # generate table data
    table_data = mk_table_data(running_stats)
    # generate table
    table = markdown_table(
            table_data
        ).set_params(
            quote=False,
            padding_width=3,
            row_sep="markdown"
        ).get_markdown()

    print("Sumstats, last 3 versions:\n")
    print(table)
    print("\n\n")

    stats = {
        "n-prot":{
            "header": "records",
            "version": args.records_version,
            "title":f"Number of Parliamentary Records over time ({args.records_version})"
        },
        "prot-pages":{
            "header":"pages",
            "version": args.records_version,
            "title":f"Number of Pages in Parliamentary Records over time ({args.records_version})"
        },
        "prot-speeches":{
            "header": "speeches",
            "version": args.records_version,
            "title": f"Number of Speeches in Parliamentary Records over time ({args.records_version})"
        },
        "prot-words":{
            "header": "words",
            "version": args.records_version,
            "title":f"Number of Words in Parliamentary Records over time ({args.records_version})"
        }
    }

    print("GENERATING SUMSTAT PLOTS:")
    for stat, stat_d in stats.items():
        df = pd.read_csv(f"stats/{stat}/{stat}.csv")
        df.set_index("year", inplace=True)
        df[stat_d['version']] = prot_d[stat_d['header']]
        df.to_csv(f"stats/{stat}/{stat}.csv")
        gen_prot_plot(df, f"stats/{stat}/{stat}.csv", stat_d["title"], stat_d["header"].capitalize())

    print("...done")

    print("RENDERING NEW README FILE:")
    to_render = {
            "Version": args.version,
            "Updated": now.strftime("%Y-%m-%d, %H:%M:%S"),
            "version_info": versions_table(version_d),
            "sumstats_table": table,
            "records_repo_version": args.records_version,
            "persons_repo_version": args.persons_version,
        }
    if render_markdown(to_render):
        print("New README generated successfully.")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--version", type=str)
    parser.add_argument("-py", "--pyriksdagen-version", type=str)
    parser.add_argument("-rv", "--records-version", type=str)
    parser.add_argument("-pv", "--persons-version", type=str)
    parser.add_argument("--outdir", type=str, default="plots")
    args = parser.parse_args()
    release_version = re.compile(r"v(20[0-9]{2})([.])((0|1)[0-9])([.])([0-3][0-9]{1})(b|rc)?([0-9]+)?")
    repo_version = re.compile(r"v([0-9]+)([.])([0-9]+)([.])([0-9]+)(b|rc)?([0-9]+)?")
    if release_version.search(args.version) is None:
        print(f"{args.version} is not a valid version number. Exiting")
        exit()
    for v in [args.persons_version, args.records_version]:
        if v is None or repo_version.search(v) is None:
            print(f"{v} is not a valid version number. Exiting")
            exit()
    args.version = release_version.search(args.version).group(0)
    #print(args)
    main(args)
