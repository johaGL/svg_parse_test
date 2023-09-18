"""
test the parsing of a svg file
with the objective of creating :
   lib/galaxy/tool_util/verify/asserts/image_svg.py in Galaxy

@author : johanna sept 2023
"""
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from xml.dom import minidom
import pandas as pd


def verify_this_svg(filename):
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

    return np.alltrue(bool_allids), np.alltrue(bool_url), np.alltrue(bool_styles), np.alltrue(bool_tt)


if __name__ == '__main__':
    os.getcwd()
    files_names = os.listdir("figures_folder")
    txt = "file\tids_tags\turl_tags\tstyles_tags\ttranslate_scale_tag\n"
    for k in files_names:
        if "," in k: # skip files that have ',' in filename, as not opened correctly
            continue
        res = verify_this_svg(os.path.join(os.getcwd(), "figures_folder", k))
        txt += f"{k}\t{res[0]}\t{res[1]}\t{res[2]}\t{res[3]}\n"

    with open("output.txt", "w") as f:
        f.write(txt)