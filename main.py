# importing libraries
from multiprocessing import Process, Pipe
from zipfile import ZipFile
import time
import csv
import os
import random

#Creating definition or function for the calculation of prime numbers where conn, j, num are arguments
def prime(conn, j, num):
    #Initialization of the variables
    startingInput = num
    #Specifying the random time (from library RANDOM and TIME imported ) between the Range of 30-60 specified by Dr. Issam Raïs
    randomSec = random.randint(30, 60)
    t_end = time.time() + randomSec
    print ('\nStarting point to compute prime number by this Process is', num, '\nTime to be taken by this process is', randomSec, 'Seconds\n')
    #Initiating the counter for the numbering of data stored in csv file
    count = 0
    #Initiating the loop for the calculation of Prime Numbers in the specified random time
    while time.time() < t_end:
        #Inserting > 1 condition as 1 is neither prime nor composite
        if num > 1:
            #Using modulo operation as recommended by Dr. Issam in 'for' loop in order to compute the number 'num' for primality
            #if num has a remainder 0, it is incremented followed by break
            for i in range(2, int(num / 2) + 1):
                if (num % i) == 0:
                    num = num + 1
                    break
                #This 'If' condition resolves the issue reagarding the computation of the large number that takes more than generated random time
                #Sending the value directly through the pipe to the connection.send
                if time.time() > t_end:
                    timeoutValue = num
                    break
            #In Else, the num obtained is the prime number which is stored in the csv Files generated according to the Process running
            #tickTime (sec) denotes the time when the prime number is obtained
            else:
                tickTime = round(randomSec - (t_end - time.time()), 2)
                with open(f'process({j})_cal_prime_num.csv', 'a') as csvProcesses:
                    count = count + 1
                    csvProcesses.write('%d,' %count)
                    csvProcesses.write('%f,' %tickTime)
                    csvProcesses.write('%d\n' %num)
                    print(str(tickTime)+'sec :', num)
                    sendValue = num
                    num = num + 1
        #Else: Input 'num' is less than equal to 1 it is incremented and loop continues
        else:
            num = num + 1
    with open(f'process({j})_cal_prime_num.csv', 'a') as csvProcesses:
        csvProcesses.write('Random Time for this Process has been ')
        csvProcesses.write('%s' %randomSec)
        csvProcesses.write('seconds')
    #UnboundLocalError is here catched and Values are accordingly send to pipe
    try:
        conn.send(sendValue)
    except UnboundLocalError:
        if startingInput == timeoutValue:
            print(f'\nTime Insufficient to compute any Prime Number starting from {timeoutValue}')
        else:
            print(f'\nNo Prime Numbers found on checking between {startingInput} and {timeoutValue}. \nInsufficient time to check for prime numbers from {timeoutValue}')
        #timeoutValue is decremented, so that it can be calculated again
        conn.send(timeoutValue-1)
    conn.close()

#__name__ is a built-in variable which evaluates to the name of the current module
if __name__ == '__main__':
    #Providing the input for the processes
    while True:
        try:
            numProcess = int(input("Number of Processes: "))
            assert numProcess > 0
            break
        except ValueError:
            print("Number of Processes must be a Natural Number")
        except AssertionError:
            print("The processes should be greater than or equal to 1")
    #Specifying the Processes with the endpoints of the Pipe
    #'For loop' for the forward computation of the Processes (i.e Process0==>Process1==>....==>ProcessN)
    for j in range(numProcess):
        end_a_pipe = j
        end_b_pipe = j + 1
        if j == 0:
            #Providing the input for the initial Prime Number from which calculation begins
            while True:
                try:
                    num = int(input('Input Number starting from which Prime Numbers are to be computed: '))
                    assert num >= 0
                    break
                except ValueError:
                    print("Only positive integer accepted...")
                    continue
                except AssertionError:
                    print("The Number should be greater than or equal to 0")
        print('--------------------------------------------------------------------------------','\nProcess-{} starts'.format(j))
        #Adding Headers and other specifications to the csv File
        with open('process({})_cal_prime_num.csv'.format(j), 'w') as csvProcesses:
            csvProcesses.truncate()
            dheader = csv.DictWriter(csvProcesses, delimiter=',', fieldnames=['Ser Num','Time Taken(in sec)', 'Prime Numbers Generated'])
            dheader.writeheader()
            csvProcesses.write('Forward Process Data\n')
        #Adding ends to the current pipe
        end_a_pipe, end_b_pipe = Pipe()
        #Starting the Transference process where the last prime obtained in a Process is send through Pipe to consecutive Process
        p = Process(target=prime, args=(end_a_pipe, j, num ))
        p.start()
        #Receiving the previous processes's last prime number and incrementing by 1 for continuing the calculation
        num = int(end_b_pipe.recv()) + 1
        p.join()
        print('\nProcess-{} Ends'.format(j))
        #Condition 'If' and Loop 'For' for the reversal of the Processes (i.e ProcessN==>ProcessN-1==>....==>Process0)
        if j == numProcess - 1 :
            print('\n--------------------------------------------------------------------------------', '\nReverse processes starts from this point')
            for j in reversed(range(numProcess - 1)):
                end_a_pipe = j
                end_b_pipe = j - 1
                print('--------------------------------------------------------------------------------','\nReverse Process-{} starts'.format(j))
                with open('process({})_cal_prime_num.csv'.format(j), 'a') as csvProcesses:
                    csvProcesses.write('\nReverse Process Data\n')
                end_b_pipe, end_a_pipe = Pipe()
                p = Process(target=prime, args=(end_b_pipe, j, num ))
                p.start()
                num = int(end_a_pipe.recv()) + 1
                p.join()
                print('\nReverse Process-{} Ends'.format(j))
            print('\n--------------------------------------------------------------------------------', '\nAll Processes End Successfully', '\n--------------------------------------------------------------------------------')
    #date:-Timestamp
    date = time.time()
    #Generating Zip File with time stamp where all csv of Processes are ARCHIVED (using zipfile library)
    with ZipFile(f'UiT_{date}_({numProcess}-processes)_primeNum.zip', 'w') as zipProcesses:
        for j in range(numProcess):
            zipProcesses.write(f'process({j})_cal_prime_num.csv')
            #Removing the csv Files after archiving (using os library methods)
            os.remove(f'process({j})_cal_prime_num.csv')
