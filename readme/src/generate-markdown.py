#!/usr/bin/env python3
"""
Generates a dynamic markdown file for the repo's main README.
"""
from datetime import datetime
from py_markdown_table.markdown_table import markdown_table
import argparse
import json
import os
import re

now = datetime.now()




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


def update_version_d(args):
    if os.path.exists("version-compatibility/versions.json"):
        with open("version-compatibility/versions.json", 'r') as inf:
            version_d = json.load(inf)
    else:
        version_d = {}
        if not os.path.exists("version-compatibility"):
            os.mkdir("version-compatibility")
    version_d[args.version] = {
            "pyriksdagen": args.pyriksdagen_version,
            "riksdagen-persons": args.persons_version,
            "riksdagen-records": args.records_version,
            "riksdagen-motions": args.motions_version,
            "riksdagen-interpellations": args.interpellations_version,
            "scripts": args.scripts_version,
            "rcr-version": args.rcr_version
        }
    with open("version-compatibility/versions.json", 'w+') as outf:
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
    version_d = update_version_d(args)
    print("RENDERING NEW README FILE:")
    to_render = {
            "Version": args.version,
            "Updated": now.strftime("%Y-%m-%d, %H:%M:%S"),
            "version_info": versions_table(version_d),
            "records_repo_version": args.records_version,
            "persons_repo_version": args.persons_version,
            "pyriksdagen_repo_version": args.pyriksdagen_version,
            "motions_repo_version": args.motions_version,
            "interpellations_repo_version": args.interpellations_version,
            "scripts_repo_version": args.scripts_version,
            "rcr_repo_version": args.rcr_version
        }
    if render_markdown(to_render):
        print("New README generated successfully.")




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-v", "--version", type=str)
    parser.add_argument("-py", "--pyriksdagen-version", type=str, required=True)
    parser.add_argument("-rv", "--records-version", type=str, required=True)
    parser.add_argument("-pv", "--persons-version", type=str, required=True)
    parser.add_argument("-mv", "--motions-version", type=str, required=True)
    parser.add_argument("-iv", "--interpellations-version", type=str, required=True)
    parser.add_argument("-sv", "--scripts-version", type=str, required=True)
    parser.add_argument("-r", "--rcr-version", type=str, required=True)
    args = parser.parse_args()
    release_version = re.compile(r"v(20[0-9]{2})([.])((0|1)[0-9])([.])([0-3][0-9]{1})(b|rc)?([0-9]+)?")
    repo_version = re.compile(r"v([0-9]+)([.])([0-9]+)([.])([0-9]+)(b|rc)?([0-9]+)?")
    if release_version.search(args.version) is None:
        print(f"{args.version} is not a valid version number. Exiting")
        exit()
    for v in [
                args.persons_version,
                args.records_version,
                args.pyriksdagen_version,
                args.motions_version,
                args.interpellations_version,
                args.scripts_version,
                args.rcr_version
            ]:
        if v is None or repo_version.search(v) is None:
            print(f"{v} is not a valid version number. Exiting")
            exit()
    args.version = release_version.search(args.version).group(0)
    #print(args)
    main(args)
