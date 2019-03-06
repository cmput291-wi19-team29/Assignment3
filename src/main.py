import pandas as pd
import numpy as np
import math
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
    print('Running task 1\n')
    PER_PAGE = 5
    
    # read and process SQL query 1 -- get all papers
    query = open('1a.sql','r')
    sql = query.read()
    query.close()
   
    df = None
    try:
        df = pd.read_sql_query(sql,conn)
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return
    
    # calculate number of pages of 5 papers each
    # (except possibly the last page)
    num_rows = len(df)
    batches = math.ceil(num_rows/PER_PAGE)
    showing = 1         # the batch currently showing

    # show five papers per page until one is selected
    valid = False
    while(not valid):
        
      if showing == batches:
        # the last batch may not have 5 rows
        print(df.iloc[showing*PER_PAGE-PER_PAGE:num_rows,:1])

      else:
        print(df.iloc[showing*PER_PAGE-PER_PAGE:showing*PER_PAGE,:1])

      # show options --
      # N should not show for the last page, P should not show for the first page
      print("\nSelect a paper")
      if showing > 1:
        print("[P] Previous Page")
      if showing < batches:
        print("[N] Next Page")

      # process get user input
      option = input()

      # let's be kind to the user and not make it case sensitive

      if option.lower() == "n" and showing < batches:
        # next page
        showing += 1
        continue
    
      if option.lower() == "p" and showing >1:
        # prev page
        showing -= 1
        continue
    
      if option.isdigit():
        # only accept numbers currently showing
        if (showing == batches and int(option) in range(showing*PER_PAGE-PER_PAGE,num_rows)) or (showing != batches and int(option) in range(showing*PER_PAGE-PER_PAGE,showing*PER_PAGE)):
          selected = int(option)
          valid = True
        else:
          print("\nInvalid option. Select the number of a paper on the page.")
          continue
        
      else:
        # not valid
        print("\nInvalid option. Enter N, P, or a paper number.")
        continue
    # end while
    

    # read and process SQL query 2 -- get all reviewers of the paper selected
    query2 = open('1b.sql','r')
    sql2 = query2.read()
    query2.close()
   
    df2 = None
    try:
        df2 = pd.read_sql_query(sql2,conn,params=[int(df.iloc[selected,1])])
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return

    print("\nReviewers of this paper:")
    for each in df2['reviewer'].values:
        print(each) 

    
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
