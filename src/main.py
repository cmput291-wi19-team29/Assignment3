import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

# check if a variable is an integer
def isInt(x):
    try:
        int(x)
        return True
    except:
        return False

# clear screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def task1(conn):
    print('Run task 1')
    
def task2(conn):
    print('Run task 2')

# given a number range, find all reviewers whose number of reviews is in that range (the range should include the bounds)
def task3(conn):
    # notify
    print('Running task 3\n')

    # get the interval [a, b]
    print('Enter integers for the interval [a, b]')
    a = input('a: ')
    b = input('b: ')

    # validate
    if not ( isInt(a) and isInt(b) ):
        print('Error: a,b must be integers')
        return
    if b < a:
        print('Error: b cannot be less than a')
        return

    # read SQL
    f = open('3.sql', 'r')
    sql = f.read()
    f.close()

    # execute
    args = (int(a), int(b))
    cur = conn.cursor()
    try:
        cur.execute(sql, args)
    except sqlite3.Error as e:
        print("Error: {}".format(e.args[0]))
        return

    # print
    print('\nResult:')
    for row in cur:
        print(row)

def task4(conn):
    print('Run task 4')
    
def task5(conn):
    print('Run task 5')

# for each reviewer, give a bar chart of their average review scores for each category. You must return a single grouped bar chart.
def task6(conn):
    # notify
    print('Running task 6\n')

    # read SQL
    f = open('6.sql', 'r')
    sql = f.read()
    f.close()
    
    # execute
    try:
        df = pd.read_sql_query(sql, conn)
    except:
        # use custom message since sql error won't propagate
        print("Error: query failed")
        return

    # display
    df.plot.bar(x='reviewer')
    plt.show()

def main():
    # connect to DB
    try:
        conn = sqlite3.connect("database.db")
    except sqlite3.Error as e:
        print("Error: {}".format(e.args[0]))
        return

    # use dict since python has no switch
    tasks = {}
    tasks['1'] = task1
    tasks['2'] = task2
    tasks['3'] = task3
    tasks['4'] = task4
    tasks['5'] = task5
    tasks['6'] = task6

    # message pump
    while(True):
        # display API
        print('\n--- ASSIGNMENT 3 PROGRAM ---')
        print('What do you want to know?')
        print('[q] Quit')
        print('[1] Task 1')
        print('[2] Task 2')
        print('[3] Reviewers that have made [a, b] reviews')
        print('[4] Task 4')
        print('[5] Task 5')
        print('[6] Average scores per cateogry for each reviewer (bar chart)')
        action = input()

        # exit condition
        if action == 'q':
            break

        # execute action
        try:
            print('') # newline
            tasks[action](conn)
        except:
            print('Error: invalid action')

# make .py safe to use in import
if __name__== "__main__":
  main()
