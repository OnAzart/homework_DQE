import argparse
from argparse import Namespace
import csv
import numpy as np

parser = argparse.ArgumentParser(description="Введи такі дані")
parser.add_argument('-path', '-dir', help="Шлях до файлу")
parser.add_argument('-bed', help="Кількість HRR")


if __name__ == "__main__":
    args: Namespace = parser.parse_args()
    path, bed = args.path, int(args.bed)

    total_Hospital_Beds = []
    thb_header = "Total Hospital Beds"
    available_Hospital_Beds = []
    avb_header = "Available Hospital Beds"

    HRR = []

    with open(path) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)

        thb_index = headers.index(thb_header)
        avb_index = headers.index(avb_header)

        row = next(f_csv)

        for row in f_csv:
            total_Hospital_Beds.append(int(row[thb_index].replace(',', '')))
            available_Hospital_Beds.append(int(row[avb_index].replace(',', '')))
            HRR.append(row[0])

        np_free = np.array(available_Hospital_Beds) / np.array(total_Hospital_Beds) * 100
        free_place_dict = {hrr: value.round(2) for hrr, value in zip(HRR, np_free)}

    i = 0
    for key, value in sorted(free_place_dict.items(), key=lambda x: x[1], reverse=True):  # sort dict by value
        if i >= bed:
            break
        print(key, str(value) + '%')
        i += 1
