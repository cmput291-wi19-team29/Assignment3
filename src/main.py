import pandas as pd
import numpy as np
import matplotlib.pyplot as mpl
import sqlite3

def task1():
    print('Run task 1')
    
def task2():
    print('Run task 2')

def task3():
    print('Run task 3')

def task4():
    print('Run task 4')
    
def task5():
    print('Run task 5')
    
def task6():
    print('Run task 6')

def main():
    print('--- ASSIGNMENT 3 PROGRAM ---')
    # Other terminal instructions here

    tasks = {}
    tasks[1] = task1 # Set manually for changing func names
    tasks[2] = task2
    tasks[3] = task3
    tasks[4] = task4
    tasks[5] = task5
    tasks[6] = task6

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
        
        if action.lower()=='e':
            break

        # Does not catch exceptions
        tasks[int(action)]()

        print('Done.')
        
    print('Goodbye.')

main()
