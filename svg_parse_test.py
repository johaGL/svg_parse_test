"""
test the parsing of a svg file
with the objective of creating :
   lib/galaxy/tool_util/verify/asserts/image_svg.py in Galaxy

@author : johanna sept 2023
"""
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from xml.dom import minidom
import pandas as pd


def print_the_svg(filename):
    tips = sns.load_dataset("tips")

    fig, axs_k = plt.subplots(
        nrows=1, ncols=1,
        figsize=(5, 4))

    sns.barplot(
        ax=axs_k,
        x="sex",
        y="total_bill",
        hue="smoker",
        data=tips,
        palette='Accent',
        edgecolor="black",
        errcolor="black",
        errwidth=1.5,
        capsize = 0.1,
    )
    np.random.seed(123)  # to force the jitter not to randomly change
    # map data to stripplot
    sns.stripplot(
        ax=axs_k,
        data=tips,
        x='sex',
        y='total_bill',
        hue='smoker',
        palette='Accent',
        dodge=True,
        edgecolor="black",
        linewidth=1.3,
        alpha=1
    )
    plt.savefig(filename)
    plt.close()


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


if __name__ == '__main__':
    filename = "myfig.svg"
    print_the_svg(filename)
    with open(filename, "r") as f:
        d0 = minidom.parse(f)

    firstelem = d0.nodeName

    allids = [elem.getAttribute('id') for elem
            in d0.getElementsByTagName('g')]

    path_strings = [path.getAttribute('d') for path
                    in d0.getElementsByTagName('path')]

    styles = [path.getAttribute('style') for path
                    in d0.getElementsByTagName('path')]

    urls = [p.getAttribute('clip-path') for p
              in d0.getElementsByTagName('path')]

    tt = [t.getAttribute('transform') for t
          in d0.getElementsByTagName('g')]

    # clear each list from empty strings
    allids_array = pd.Series([i for i in allids if i != ''])
    styles_arr = pd.Series([i for i in styles if i != ''])
    urls_arr = pd.Series([i for i in urls if i != ''])
    tt_arr = pd.Series([i for i in tt if i != ''])

    # verifications
    bool_allids = allids_array.str.contains(
        "fig|ax|patch|Collection|line|tick|text|legend",
        regex=True
    )
    bool_styles = styles_arr.str.contains("stroke|fill", regex=True)
    bool_url = urls_arr.str.startswith("url")
    bool_tt = tt_arr.str.contains("translate|scale")

    print(np.alltrue(bool_allids))
    print(np.alltrue(bool_url))
    print(np.alltrue(bool_styles))
    print(np.alltrue(bool_tt))

