"""
Estimate and Draw a graph of the introduction mapping accuracy estimate.
"""
from cycler import cycler
from multiprocessing import Pool
from pyriksdagen.utils import (
    get_data_location,
    parse_protocol,
    protocol_iterators,
)
from tqdm import tqdm
import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re




def update_plot(version):
    colors = list('bgrcmyk')
    default_cycler = (cycler(color=colors) +
                      cycler(linestyle=(['-', '--', ':', '-.']*2)[:len(colors)]))
    plt.rc('axes', prop_cycle=default_cycler)
    f, ax = plt.subplots()

    df = pd.read_csv('stats/intro-mapping-accuracy/difference.csv')

    # Overwrite current version
    if len(df[df['version'] == version]) > 1:
        df = df[df['version'] != version]

    # Add current version
    accuracy = pd.read_csv('stats/intro-mapping-accuracy/upper_bound.csv')
    accuracy = accuracy[['year', 'accuracy_upper_bound']].rename(columns={'accuracy_upper_bound':'accuracy'})
    accuracy['version'] = version
    df = pd.concat([df, accuracy])

    # Save new values
    df.to_csv('stats/intro-mapping-accuracy/difference.csv', index=False)

    # prepend 'v' to version nr if not already there
    df['version'] = df['version'].apply(lambda s: s if s.startswith('v') else f'v{s}')

    # sort versions 
    #    (a) first by patch, then minor, then major and 
    #    (b) by int (10, 9 ... 2, 1) not str ('9' ... '2', '10', '1')
    version = sorted(list(set(df['version'])), key=lambda s: list(map(int, s[1:].split('.'))), reverse=True)

    for v in version[:6]:
        dfv = df.loc[df['version'] == v]
        x = dfv['year'].tolist()
        y = dfv['accuracy'].tolist()
        x, y = zip(*sorted(zip(x,y),key=lambda x: x[0]))
        plt.plot(x, y, linewidth=1.75)

    plt.title('Estimated accuracy for identification of speaker')
    plt.legend(version, loc ="upper left")
    ax.set_xlabel('Year')
    ax.set_ylabel('Accuracy')
    return f, ax


# Fix parallellization
def accuracy(protocol):
    root, ns = parse_protocol(protocol, get_ns=True)
    for docDate in root.findall(f".//{ns['tei_ns']}docDate"):
        date_string = docDate.text
        break
    year = int(date_string[:4])
    known, unknown = 0, 0
    for div in root.findall(f".//{ns['tei_ns']}div"):
        for elem in div:
            if "who" in elem.attrib:
                who = elem.attrib["who"]
                if who == "unknown":
                    unknown += 1
                else:
                    known += 1
    return year, known, unknown


def calculate_upper_bound(args):
    if args.start is not None:
        protocols = sorted(list(protocol_iterators(
                                                get_data_location('records'),
                                                start=args.start,
                                                end=args.end)))
    else:
        protocols = sorted(list(protocol_iterators(get_data_location('records'))))
    #print(protocols)
    years = sorted(set([int(p.split('/')[2][:4]) for p in protocols]))
    years.append(max(years)+1)
    df = pd.DataFrame(
                np.zeros((len(years), 2), dtype=int),
                index=years,
                columns=['known', 'unknown'])
    pool = Pool()
    for year, known, unknown in tqdm(pool.imap(accuracy, protocols), total=len(protocols)):
        df.loc[year, 'known'] += known
        df.loc[year, 'unknown'] += unknown
    df['accuracy_upper_bound'] = df.div(df.sum(axis=1), axis=0)['known']
    return df




def main(args):
    print("Calculate Upper Bound...")
    df = calculate_upper_bound(args)
    print(df)
    print(" -- Average:", df['accuracy_upper_bound'].mean())
    print(" -- Weighted average:", df["known"].sum() / (df["known"] + df["unknown"]).sum())
    print(" -- Minimum: {} ({})".format(*[getattr(df['accuracy_upper_bound'], f)() for f in ['min', 'idxmin']]))
    df.to_csv("stats/intro-mapping-accuracy/upper_bound.csv", index_label='year')


    print("Plotting plot")
    f, ax = update_plot(args.version)
    plt.savefig('plots/speaker-mapping-estimate.png', dpi=300)
    if args.show:
        plt.show()
        plt.close()




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-r", "--records-folder",
                        type=str,
                        default=None,
                        help="(optional) Path to records folder, defaults to environment var or `data/`")
    parser.add_argument("-s", "--start", type=int, default=1867, help="Start year")
    parser.add_argument("-e", "--end", type=int, default=2022, help="End year")
    parser.add_argument("-v", "--version", type=str)
    parser.add_argument("--show", type=str, default="True")
    args = parser.parse_args()
    args.show = False if args.show.lower()[:1] == "f" else True
    exp = re.compile(r"v([0-9]+)([.])([0-9]+)([.])([0-9]+)(b|rc)?([0-9]+)?")
    if exp.search(args.version) is None:
        print(f"{args.version} is not a valid version number. Exiting")
        exit()
    else:
        args.version = exp.search(args.version).group(0)
        main(args)

