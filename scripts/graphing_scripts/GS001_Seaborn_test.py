"""
    GS001_Seaborn_test.py
    Author: Rodolfo Canet
    Purpose:
"""

from tkinter import filedialog

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import os


def import_data(aux_path):
    aux_data = pd.read_csv(aux_path, header=None)
    wavelength = aux_data.iloc[:, 0]
    aux_list = []
    for item in wavelength:
        aux_list.append(int(round(item, 0)))
    aux_list = pd.Series(aux_list)
    aux_data = aux_data.iloc[:, 1:-1]
    aux_data = aux_data.transpose().rename(columns=aux_list)
    print(aux_data)
    return aux_data


def col_norm(df):
    df_norm = (df - df.mean()) / df.std()
    return df_norm


def row_norm(df):
    df_norm = df.apply(lambda x: (x - x.mean()) / x.std(), axis=1)
    return df_norm


if __name__ == "__main__":
    sns.set_theme(style="white")

    path = filedialog.askopenfilename()
    data = import_data(path)
    filename = os.path.split(path)[-1]
    filename = filename[0:filename.index(".")]

    bands = sns.heatmap(data, xticklabels=454, yticklabels=False, cbar=False)

    bands.set(xlabel='Wavelength (nm)', ylabel=None)
    plt.ylim(230, 800)

    plt.savefig(filename + ".png")
    plt.show()
