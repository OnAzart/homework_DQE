import sqlite3
import csv
from os import remove
from os import path
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

filename = 'dqe_8.db'
if path.isfile(filename):
    remove(filename)

conn = sqlite3.connect(filename)
c = conn.cursor()

c.execute('''CREATE TABLE Projects(
            name text,
            description text,
            deadline date,
            PRIMARY KEY (Name)
            )
            ''')

c.execute('''CREATE TABLE Tasks(	
            id integer,
            priority integer,
            details text,
            status text,
            deadline date,
            completed date,
            project text,
            PRIMARY KEY (id),
            FOREIGN KEY (project) REFERENCES Projects(name)
            )
            ''')

projects_csv = csv.reader(open(projects_path), delimiter=";")
headers = next(projects_csv)
projects_values = []
for col in projects_csv:
    data = (col[0], col[1], col[2])
    projects_values.append(data)

tasks_csv = csv.reader(open(tasks_path), delimiter=";")
headers_task = next(tasks_csv)
tasks_values = []
for col in tasks_csv:
    data = (col[0], col[1], col[2], col[3], col[4], col[5], col[6])
    tasks_values.append(data)

c.executemany('''INSERT INTO Projects (name, description, deadline) VALUES (?, ?, ?)''',
              projects_values)  # inserting multiple rows
print("Total", c.rowcount, "Records inserted successfully into 'Projects' table")

c.executemany('''INSERT INTO Tasks VALUES (?, ?, ?, ?, ?, ?, ?)''', tasks_values)
print("Total", c.rowcount, "Records inserted successfully into 'Tasks' table\n")


def request_tasks_of_project(project="TeslaPhone"):
    tasks_of_project = c.execute("SELECT * from Tasks where project = '{}'".format(project, )).fetchall()
    if not tasks_of_project:
        project = "TeslaPhone"
        tasks_of_project = c.execute("SELECT * from Tasks where project = '{}'".format(project, )).fetchall()

    for task in tasks_of_project:
        print()
        print(headers_task[0].upper() + ":", task[0])
        print(headers_task[1].upper() + ":", task[1])
        print(headers_task[2].upper() + ":", task[2])
        print(headers_task[3].upper() + ":", task[3])
        print(headers_task[4].upper() + ":", task[4])
        print(headers_task[5].upper() + ":", task[5])
        print(headers_task[6].upper() + ":", task[6])
        print()


project = input("Explore tasks of certain project.\n"
                "Enter name of this project or press any letter (in this way you will see 'TeslaPhone' tasks): ")
request_tasks_of_project(project)
