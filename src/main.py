import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
import sqlite3

# Other functions here...



def main():
    print('--- ASSIGNMENT 3 PROGRAM ---')
    # Other terminal instructions here

    # Initializations here

    # Main interface loop
    while(True):
        print('What do you want to do?')
        print('[e] Exit')
        print('[1] Task 1')
        print('[2] Task 2')
        print('[3] Task 3')
        print('[4] Task 4')
        print('[5] Task 5')
        print('[6] Task 6')
        action = input()
        try:
            if action.lower() == 'e':
                break # Exit interface
            # Perhaps make a function for each task
            if int(action)==1:
                print('Run task 1')
            elif int(action)==2:
                print('Run task 2')
            elif int(action)==3:
                print('Run task 3')
            elif int(action)==4:
                print('Run task 4')
            elif int(action)==5:
                print('Run task 5')
            elif int(action)==6:
                print('Run task 6')
            else:
                break # Just exit for now
            print('Done.')
        except:
            # For catching input errors & edge cases
            # Just exit the loop for now
            break

    print('Goodbye.')

main()
