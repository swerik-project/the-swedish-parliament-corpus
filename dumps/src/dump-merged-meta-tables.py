#!/usr/bin/env python3
"""
Dump some of metadata related to MPs, Ministers, and Speakers merged on the person_id.
"""
from pyriksdagen.metadata import load_Corpus_metadata
import argparse



def main(args):
    corpus = load_Corpus_metadata()
    for file_ in ['member_of_parliament', 'minister', 'speaker']:
        df  = corpus[corpus['source'] == file_]

        # Sort the df to make easier for git
        sortcols = list(df.columns)
        print(f"sort by {sortcols}")
        df = df.sort_values(sortcols)
        df.to_csv(f"{args.outfolder}/{file_}.csv", index=False)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outfolder", type=str, default="dumps/dumps")
    args = parser.parse_args()
    main(args)
