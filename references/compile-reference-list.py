#!/usr/bin/env python3
"""
Compile `references/bibtex/*.bib` to a single reference list file.
"""
from glob import glob
from tqdm import tqdm
import argparse
import warnings





def validate_bib_data(data, bib):
    OK = True
    errors = []
    if not data[0].startswith("@"):
        errors.append("First line of .bib needs to start with '@'.")
        OK = False

    try:
        bibtype, key = data[0].split("{")
        #print(filename, key[:-1], filename[:-4])
        if key[:-1] != bib.split("/")[-1][:-4]:
            errors.append("Key must be the same as the filename without '.bib'.")
            if not key.endswith(","):
                errors.append("Malformed first line. (missing comma?)")
            OK = False
    except:
        errors.append("Malformed first line.")
        OK = False

    for ix, l in enumerate(data, start=1):
        #print(ix, l)
        if ix != 1 and ix != len(data) and ix != len(data)-1:
            if not l.endswith(","):
                errors.append(f"Line {ix} (1 index) doesn't end with a comma and it should.")
                OK = False
        if ix == len(data):
            if not l == "}":
                errors.append("Last line must == '}'")
                OK = False
        if ix != 1 and ix != len(data):
            if "=" not in l:
                errors.append(f"Line {ix} (1 index) is malformed. Must contain '='.")
                OK = False
        if ix == len(data)-1:
            if l.endswith(","):
                errors.append("Second to last line shouln't end with a comma, but it does.")
                OK = False
    # More validation (planned?):
    # --- reference type (right of @) are from valid set
    # --- Fields (left of =) are from valid set

    if OK:
        return True, errors
    else:
        return False, errors




def main(args):

    with open(args.output_file, "w+") as outf:
        for bib in tqdm(sorted(glob(f"{args.bibfiles}*.bib"))):
            print(bib)
            with open(bib, 'r') as inf:
                data = [l.strip() for l in inf.readlines() if l.strip() != ""]

            valid, errors = validate_bib_data(data, bib)
            if valid:
                for idx, l in enumerate(data):
                    if idx == 0 or idx == len(data)-1:
                        outf.write(f"{l}\n")
                    else:
                        outf.write(f"    {l}\n")
                outf.write("\n\n")
            else:
                warnings.warn(f"There are some problems with bibfile: {bib}")
                [print(f"  ~~ {e}\n") for e in errors]




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-b", "--bibfiles",
                        type=str,
                        default="./references/bibtex/",
                        help="Directory where bibtex files are stored.")
    parser.add_argument("-o", "--output-file",
                        type=str,
                        default="./references/_compiled-references.bib",
                        help="Where do you want the compiled reference list?")
    args = parser.parse_args()
    main(args)
