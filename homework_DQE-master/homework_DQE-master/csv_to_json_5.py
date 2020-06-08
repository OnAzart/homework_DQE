import csv
import argparse
import json

parser = argparse.ArgumentParser(description="Enter those data")
parser.add_argument("-csv", help="Path to CSV")
parser.add_argument("-json", help="Path and name of JSON")

args = parser.parse_args()
path_csv, path_json = args.csv, args.json

with open(path_csv, 'r') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    index_password = headers.index("password")
    csv_file = [row[:index_password]+row[index_password+1:] for row in f_csv]
    csv_json = json.dumps(csv_file)

with open(path_json,"w") as f:
     f.write(csv_json)
