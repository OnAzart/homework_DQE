import csv
from pymongo import MongoClient
import argparse


parser = argparse.ArgumentParser(description="Enter those data for successful performance of program")
parser.add_argument("-tasks", help="Path to CSV of table Tasks")
parser.add_argument("-projects", help="Path to CSV of table Projects")


args = parser.parse_args()
if not args.tasks or not args.projects:  # введіть в програмі, якщо не ввели в консолі
    projects_path = 'D://DQE//dqe_8_projects.csv'
    tasks_path = 'D://DQE//dqe_8_tasks.csv'
else:
    tasks_path, projects_path = args.tasks, args.projects


def _connect_mongo(host='localhost', port=27017, username="", password="", db=""):
    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)
    return conn


def csv_to_dict(path='D://DQE//dqe_8_projects.csv'):
    with open(path, 'r') as f:
        table_csv = csv.reader(f, delimiter=';')

        headers_table = next(table_csv)

        for it, row in enumerate(table_csv):
            dict_table = {'_id': it}
            for i, data in enumerate(row):
                dict_table[headers_table[i]] = data
            yield dict_table


cluster = _connect_mongo(host='localhost', port=27017)

db = cluster.dqe_9
tasks = db.tasks
projects = db.projects

tasks.delete_many({})  # clearing current data
projects.delete_many({})

projects.insert_many(csv_to_dict(projects_path))  # inserting data from generator
tasks.insert_many(csv_to_dict(tasks_path))


query_canceled = tasks.find({'status': 'canceled'})

canceled_projects = []
for i in query_canceled:
    canceled_projects.append(i['project'])

unique_canceled_projects = set(canceled_projects)

for project in unique_canceled_projects:
    print(project)
