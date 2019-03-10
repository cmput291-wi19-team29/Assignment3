import pandas as pd
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import sqlite3
import os
import time
import math

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
   
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return
    
    # calculate number of pages of 5 papers each
    # (except possibly the last page)
    paper_data = cur.fetchall()
    num_rows = len(paper_data)
    batches = math.ceil(num_rows/PER_PAGE)
    showing = 1         # the batch currently showing

    # show five papers per page until one is selected
    valid = False
    while(not valid):
      
      # last refers to the last paper on the page
      # this is the fifth paper on every page except possibly the last

      if showing == batches:
        last = num_rows
      else:
        last = showing*PER_PAGE
        
      # the last batch may not have 5 rows
      print("\n")
      for i in range(showing*PER_PAGE-PER_PAGE,last):
        print(i,paper_data[i][0])

      # show options --
      # N should not show for the last page, P should not show for the first page
      print("\nSelect a paper. Showing page",showing,"/",batches)
      if showing > 1:
        print("[P] Previous Page")
      if showing < batches:
        print("[N] Next Page")

      # process get user input
      option = input()

      # let's be kind to the user and not make it case sensitive

      if option.lower() == "n":
        if showing < batches:
            # next page
            showing += 1
            clear()
            continue
        else:
          # no next page
          print("\nThere are no more pages. Enter P to go back a page, or choose a paper number.")
          time.sleep(2.5)
          clear()
          continue
    
      if option.lower() == "p":
        if showing >1:
          # prev page
          showing -= 1
          clear()
          continue
        else:
          # no prev page
          print("\nThere are no previous pages. Enter N to go to the next page, or choose a paper number.")
          time.sleep(2.5)
          clear()
          continue

    
      if option.isdigit():
        # only accept numbers currently showing
        if (showing == batches and int(option) in range(showing*PER_PAGE-PER_PAGE,num_rows)) or (showing != batches and int(option) in range(showing*PER_PAGE-PER_PAGE,showing*PER_PAGE)):
          selected = int(option)
          valid = True
        else:
          print("\nInvalid option. Select the number of a paper on the page.")
          time.sleep(2.5)
          clear()
          continue
        
      else:
        # not valid
        print("\nInvalid option. Enter N, P, or a paper number.")
        time.sleep(2.5)
        clear()
        continue
    # end while
    

    # read and process SQL query 2 -- get all reviewers of the paper selected
    query2 = open('1b.sql','r')
    sql2 = query2.read()
    query2.close()
   
    try:
        cur.execute(sql2, (paper_data[selected][1],))
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return
    
    # display reviewers
    print("\nReviewers of this paper:")
    reviewer_data = cur.fetchall()
    for each in reviewer_data:
        print(each) 

# Show all papers in pages; select a paper and show all potential reviewers
def task2(conn):
    print('Displaying all papers...\n')
    
    PER_PAGE = 5
    DELAY = 2.5

    # Read SQL query for geting all papers
    try:
        f = open('2a.sql','r')
        sql = f.read()
        f.close()
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return

    # Create cursor and execute first query (get all papers)
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return
    
    # Calculate number of pages of 5 papers each
    papers = cur.fetchall() # Get result of the sql execution
    num_papers = len(papers)
    num_pages = math.ceil(num_papers/PER_PAGE)
    page = 1 # The page to show

    #time.sleep(DELAY) # annoying when trying to check them all
    clear()

    # Page selection loop
    valid = False
    while(not valid):
        print("\n")

        # Print out the interface. Stop printing when the last paper is reached. 
        for i in range( (page*PER_PAGE)-PER_PAGE, page*PER_PAGE ):
            if i < num_papers:
                print("[%i]  %s  %s" % (i, papers[i][2], papers[i][0]))
            else:
                print()
        print()

        # Show pagination
        print("Select a paper. Showing page (%i / %i)" % (page, num_pages))
        if page > 1:
            print("[P] Previous Page")
        else:
            print()
        if page < num_pages:
            print("[N] Next Page")
        else:
            print()
        print("[Q] Quit to  main menu")

        # User input
        option = input()
        if option.lower() =="q":
            return
        # Change pages
        if option.lower() == "n":
            if page < num_pages:
                page += 1
                clear()
                continue
            else:
                print("There are no more pages. Enter P to go back a page, or choose a paper number.")
                time.sleep(DELAY)
                clear()
                continue
        
        if option.lower() == "p":
            if page > 1:
                page -= 1
                clear()
                continue
            else:
                print("There are no previous pages. Enter N to go to the next page, or choose a paper number.")
                time.sleep(DELAY)
                clear()
                continue
    
        # Select a paper
        if option.isdigit():
            # Only allow papers on this page to be selected
            if (page == num_pages and int(option) in range(page*PER_PAGE-PER_PAGE, num_pages)) or (page != num_pages and int(option) in range(page*PER_PAGE-PER_PAGE, page*PER_PAGE)):
                selected = int(option)
                valid = True
            else:
                print("Invalid option. Select the number of a paper on the page.")
                time.sleep(DELAY)
                clear()
                continue
        else:
            # not valid
            print("Invalid option. Enter Q, N, P, or a paper number.")
            time.sleep(DELAY)
            clear()
            continue

    # For the selected paper, display potential reviewers in that area of expertise
    # First execute the query (uses set difference)
    try:
        f2 = open('2b.sql','r')
        sql2 = f2.read()
        f2.close()
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return
    try:
        cur.execute(sql2, (papers[selected][1], papers[selected][1]))
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return
    
    # Display the result from the query -- potential reviewers
    print("Selected paper: '%s' \nby %s" % (papers[selected][0], papers[selected][3]))
    print("Potential reviewers for this paper in %s:" % papers[selected][2])
    reviewer_data = cur.fetchall()
    if len(reviewer_data)==0:
        print("Nobody! Perhaps the paper has already been reviewed?")
    else:
        for each in reviewer_data:
            print(each)

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
    print('Running task 4\n')
    
    # read and process SQL query -- get number of sessions per author
    # note that according to the eclass forum, the session count includes ALL sessions,
    # not just distinct ones
    # discussion: https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1140073#p3001027
    
    query = open('4a.sql','r')
    sql = query.read()
    query.close()

    try:
        df = pd.read_sql_query(sql,conn)
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return

    # display options menu
    print("Select a display option:\n (1) Bar plot of all authors \
\n (2) Individual author")

    # validate user option
    valid = False
    while(not valid):
        option = input()

        if option.isdigit():

            # bar plot
            if int(option) == 1:
                
                valid = True
                plot = df.plot.bar(x="author")
                plt.plot()
                plt.show()
                return

            # allow selection of author and display session count
            elif int(option) == 2:
            
                valid = True
                print("\n",df.iloc[:,0:1])  # all rows, and first col (author emails)
                print("\nSelect an author")

                # validate author choice
                valid_author = False
                while(not valid_author):
                    author = input()
                    
                    if author.isdigit() and int(author) in range(len(df)):
                        # show that author's name and session column
                        print(df.iloc[int(author),0],"is participating in",df.iloc[int(author),1],"session(s) (total number of accepted papers)")
                        valid_author = True
                        return
                    else:
                        print("Invalid author number. Please enter a number from the list of authors above")
                        continue

            else:
                print("Invalid option. Please enter 1 or 2")
                continue

        else:
            print("Invalid option. Please enter a number")
            continue
    
def task5(conn):
    print('Showing 5 most popular areas of expertise by paper counts...\n')
    # Create a pie chart of the top 5 most popular areas
    # popularity comes from the number of papers under the area.
    # If there are less than 5 areas, show pie chart of however many areas that exist.
    
    # read SQL
    try:
        f = open('5.sql', 'r')
        sql = f.read()
        f.close()
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return
    
    # Create DataFrame
    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as e:
        print("Error: {}".format(e.args[0]))
        return
    
    # Make sure the SQL returned something
    if len(df)==0:
        print("No papers found!")
        return
    
    # Extract top 5 most popular areas and display their exact counts
    if len(df) > 5:
        # First we need to account for ties.
        # Keep extending the end limit until the tie is broken.
        #print(df)
        end = 4
        for i in range(5, len(df)):
            #print("Checking ", i-1, i)
            if df["count"][i-1] != df["count"][i]:
                break
            else:
                end = i
                #print("Match")
        # Now create the popular dataset and include the ties on the end.
        pop = df.iloc[0:end+1,:]
    else:
        pop = df
    
    print(pop)
    
    # Display percentages in a pie chart
    plot = pop.plot.pie(
        labels=pop.area, 
        y="count",
        title="Most popular areas of expertise (by paper counts)",
        legend=False,
        autopct='%1.1f%%'
    )
    plt.plot()
    plt.show()

    print("Generated a pie chart of the results.")

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
        print('[1] Fetch all reviewers for a paper')
        print('[2] Find potential reviewers for papers')
        print('[3] Reviewers that have made [a, b] reviews')
        print('[4] Total number of sessions with accepted papers per author')
        print('[5] Find the most popular areas of expertise (by paper counts)')
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
