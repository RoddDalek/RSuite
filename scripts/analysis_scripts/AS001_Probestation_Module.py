"""
    AS001_Probestation_Module.py
    Author: Rodolfo Canet
    Purpose: Script list to analyse big amounts of data coming from the Probestation in the 4th floor of Micronova.
"""

import pandas as pd
import numpy as np

import time
import sys
import os

from dash import Dash, html, dcc


def check_if_sys():
    try:
        if sys.argv[1]:
            setup(sys.argv[1])
    except IndexError:
        return True


def setup(fpath):
    def check_if_setup_run(fpath):
        aux = os.listdir(fpath)
        raw_bool, pruned_bool = False, False
        for item in aux:
            if item == "raw":
                raw_bool = True
            if item == "pruned":
                pruned_bool = True
        if raw_bool and pruned_bool:
            return True
        else:
            return False

    def move_files(fpath):
        aux = os.listdir(fpath)
        for item in aux:
            if os.path.isfile(os.path.join(fpath, item)):
                if not item == "index.html":
                    if not item == "index.txt":
                        os.replace(os.path.join(fpath, item), os.path.join(fpath, "raw", item))

    def build_filter():

        filter, aux_filter = {}, {}
        with open(r"aux_files/extractor_as001.txt", "r") as f:
            lines = f.readlines()
        for line in lines:
            aux_line = line.split(r", ")
            if aux_line[0] in aux_filter:
                aux_filter[aux_line[0]] += 1
            else:
                aux_filter[aux_line[0]] = 0
        for line in lines:
            aux_line = line.split(r", ")
            if aux_line[0] in aux_filter.keys():
                if aux_filter[aux_line[0]] > 1:
                    if aux_line[0] in filter.keys():
                        filter[aux_line[0]][aux_line[1]] = aux_line[2].removesuffix("\n")
                    else:
                        filter[aux_line[0]] = {}
                        filter[aux_line[0]][aux_line[1]] = aux_line[2].removesuffix("\n")
                else:
                    filter[aux_line[0]] = aux_line[1].removesuffix("\n")
        return filter

    def prune_file(fpath, item, filter):

        aux_device, aux_date, aux_test = None, None, None
        aux_lines = []
        with open(os.path.join(fpath, "raw", item), "r") as f:
            lines = f.readlines()
        for line in lines[1:]:
            aux_line = line.split(r", ")
            if aux_line[0] in filter.keys() and not aux_line[0] == "SetupTitle":
                if aux_line[1] in filter[aux_line[0]].keys():
                    aux_lines.append(line)
            elif aux_line[0] == "SetupTitle":
                aux_lines.append(line)
            elif aux_line[0] == "DataName" or aux_line[0] == "DataValue":
                aux_lines.append(line)
            if aux_line[0] == "SetupTitle":
                aux_test = aux_line[1].replace("Canet_", "").removesuffix("\n")
            if aux_line[1] == "TestRecord.TestTarget":
                aux_device = aux_line[2].removesuffix("\n")
            if aux_line[1] == "TestRecord.RecordTime":
                aux_date = aux_line[2].replace("/", "-").replace(":", ".").replace(" ", "_").removesuffix("\n")

        aux_item = aux_test + " - " + aux_device + " - " + aux_date + ".csv"
        with open(os.path.join(fpath, "pruned", aux_item), "w") as f:
            for line in aux_lines:
                f.write(line)

    filter = build_filter()
    if check_if_setup_run(fpath):
        print("Raw and pruned data located. Skipping setup.")
    else:
        os.mkdir(os.path.join(fpath, "raw"))
        os.mkdir(os.path.join(fpath, "pruned"))
        move_files(fpath)
        for item in os.listdir(os.path.join(fpath, "raw")):
            if os.path.isfile(os.path.join(os.path.join(fpath, "raw"), item)):
                prune_file(fpath, os.path.join(os.path.join(fpath, "raw"), item), filter)

    return filter


def extractor(fpath, filter):

    for item in os.listdir(os.path.join(fpath, "pruned")):
        with open(os.path.join(fpath, "pruned", item), "r") as f:
            lines = f.readlines()
        for line in lines:
            pass
            # aux_line = line.split(r", ")


if __name__ == "__main__":

    if check_if_sys():
        fpath = (r"C:\Users\canetr1\OneDrive - Aalto University\Research Projects\008 - Spectro-DoS\251117 - SDoS - "
                 r"v2\v2 without wirebond\test")
        filter = setup(fpath)
        extractor(fpath, filter)
