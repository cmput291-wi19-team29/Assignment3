import pandas as pd
import numpy as np
import math
import time
import matplotlib.pyplot as plt
import sqlite3
import os
import os.path
import time
import math
import sys

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

# Formatting pie chart labels
def formatLabels(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d})".format(pct, absolute)

def task1(conn):
    print('Running task 1\n')
    PER_PAGE = 5
    
    # read and process SQL query 1 -- get all papers
    try:
        query = open('1a.sql','r')
        sql = query.read()
        query.close()
    except Exception as e:
        print(e)
        return
   
    cur = conn.cursor()
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
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
    try:
        query2 = open('1b.sql','r')
        sql2 = query2.read()
        query2.close()
    except Exception as e:
        print(e)
        return
   
    try:
        cur.execute(sql2, (paper_data[selected][1],))
    except Exception as e:
        print(e)
        return
    
    # display reviewers
    print("\nReviewers of this paper:")
    reviewer_data = cur.fetchall()
    for each in reviewer_data:
        print(each) 

# Show all papers in pages; select a paper and show all potential reviewers
def task2(conn):
    print('Displaying all papers...\n')
    
    # Read in sql
    paper_f = open('2a.sql', 'r')
    paper_sql = paper_f.read()
    paper_f.close()
    reviewers_f = open('2b.sql', 'r')
    reviewers_sql = reviewers_f.read()
    reviewers_f.close()
    reviews_f = open('2c.sql', 'r')
    reviews_sql = reviews_f.read()
    reviews_f.close()
    
    # Create dataframes
    try:
        papers = pd.read_sql_query(paper_sql, conn)
        reviewers = pd.read_sql_query(reviewers_sql, conn)
        reviews = pd.read_sql_query(reviews_sql, conn)
    except Exception as e:
        print(e)
        return
    
    # Make sure the db has papers
    if len(papers)==0:
        print("No papers found!")
        return
    if len(reviewers)==0:
        print("No reviewers found!")
        return
    if len(reviews)==0:
        # Shouldn't be fatal?
        print("Note: No reviews have been made.")

    PERPAGE = 5 # Display all papers in pages
    DELAY = 2 # in seconds, for bad input messages
    page=0 # The current page being displayed

    # Pagination loop
    while (True):

        # Print out the terminal interface
        print('{%i}-PAGE\tSelect paper Id.\t Quit [q]' % ( page+1 ))
        print('-'*50)
        for j in range(page*PERPAGE, (page*PERPAGE)+PERPAGE):
            if j<len(papers):
                print("[%i] %s" % (papers['Id'][j], papers['title'][j]))
            else:
                print()
        print('-'*50)
        if page > 0:
            print('[p] previous page\t', end='')
        else:
            print('\t\t\t', end='')
        if (page * PERPAGE) + PERPAGE < len(papers):
            print('\t[n] next page', end='')
        print()
        
        # Input loop
        while(True):
            action = input() # Should match the paper's Id

            # Does the user want to select a paper or change pages?
            if isInt(action):
                # Select paper. Get its Id.
                # TODO upon reflection, I should have used iloc(). Oh well.
                Id = int(action)
                if Id-1 > len(papers)-1 or Id-1 < 0:
                    print('Invalid paper Id.')
                    time.sleep(DELAY)
                    continue # break to reprint page or continue to not reprint page
                select = Id-1 # The index of the selected paper is one less than its Id
                print("Paper %i: '%s'" % (Id, papers['title'][select]))
                print("by %s" % papers['author'][select])
                
                # Show all reviewers with matching expertise
                print("Potential reviewers in %s:" % papers["area"][select])
                count = 0
                for i in range(0, len(reviewers)):
                    # Exclude people who have already reviewed the selected paper
                    if reviewers["area"][i] == papers["area"][select]:
                        # This reviewer could review this paper
                        canReview = True
                        # Check the reviews db to see if they already reviewed it
                        for j in range(0, len(reviews)):
                            if reviewers["reviewer"][i] == reviews["reviewer"][j] and reviews["paper"][j] == papers["Id"][select]:
                                # They already reviewed this paper.
                                canReview = False
                        if canReview:
                            # This person can review this paper.
                            print(reviewers["reviewer"][i])
                            count+=1
                # Just an extra thing for user feedback.
                if count==0:
                    print("Nobody! Perhaps the paper has already been reviewed?")
            
            else:
                # Change pages
                if action=='q':
                    print('Quit')
                    return
                elif action=='p': # Previous page
                    if page > 0:
                        page -= 1
                        break
                    else:
                        print('This is the first page!')
                elif action=='n': # Next page
                    # Apparently ' / ' in python doesn't cut the decimal so I'll use floor()
                    if page < math.floor(len(papers) / PERPAGE):
                        page += 1
                        break
                    else:
                        print('This is the last page!')
                else:
                    print("Action not recognized.")
                    time.sleep(DELAY)
                    continue # use break to reprint page or continue to not reprint page
        print()

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
    if int(b) < int(a):
        print('Error: b cannot be less than a')
        return

    # read SQL
    try:
        f = open('3a.sql','r')
        sql = f.read()
        f.close()
    except Exception as e:
        print(e)
        return

    # execute
    args = (int(a), int(b))
    cur = conn.cursor()
    try:
        cur.execute(sql, args)
    except sqlite3.Error as e:
        print(e)
        return

    # print
    print('\nResult:')
    for row in cur:
        print(row)

    # special case for [0, X]
    # display reviewers who did not review any papers
    if int(a) == 0:
        # read SQL
        try:
            f = open('3b.sql','r')
            sql = f.read()
            f.close()
        except Exception as e:
            print(e)
            return

        # execute
        cur = conn.cursor()
        try:
            cur.execute(sql)
        except sqlite3.Error as e:
            print(e)
            return

        # print
        for row in cur:
            print(row)

def task4(conn):
    print('Running task 4\n')
    
    # read and process SQL query -- get number of sessions per author
    # note that according to the eclass forum, the session count includes ALL sessions,
    # not just distinct ones
    # discussion: https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1140073#p3001027
    
    try:
        query = open('4a.sql','r')
        sql = query.read()
        query.close()
    except Exception as e:
        print(e)
        return

    try:
        df = pd.read_sql_query(sql,conn)
    except Exception as e:
        print(e)
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
    print('Showing 5 most popular areas of expertise...\n')
    # Create a pie chart of the top 5 most popular areas
    # popularity comes from the number of papers under the area.
    # If there are less than 5 areas, show pie chart of however many areas that exist.
    
    # read SQL
    f = open('5.sql', 'r')
    sql = f.read()
    f.close()
    
    # Create DataFrame
    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as e:
        print(e)
        return
    
    # Make sure the SQL returned something
    if len(df)==0:
        print("No papers found!")
        return
    
    # Extract top 5 most popular areas and display their exact counts
    if len(df) > 5:
        pop = df.iloc[0:5,:]
    else:
        pop = df
    
    print(pop)

    # Display percentages in a pie chart
    plot = pop.plot.pie(
        labels=pop.area, 
        y="count",
        title="Most popular areas of expertise of papers",
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
    try:
        f = open('6.sql','r')
        sql = f.read()
        f.close()
    except Exception as e:
        print(e)
        return
    
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
    # check for DB param
    if len(sys.argv) != 2:
        print('Error: expected exactly one arg (the relative path of the database to connect to)')
        return

    # check that DB exists
    if not os.path.isfile(sys.argv[1]):
        print('The DB at ./{} does not exist'.format(sys.argv[1]))
        return

    # connect to DB
    try:
        print("Connecting to DB at ./{}".format(sys.argv[1]))
        conn = sqlite3.connect(sys.argv[1])
    except sqlite3.Error as e:
        print(e)
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
        print('[5] Find the most popular areas of expertise')
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
