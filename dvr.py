import sys
from sys import argv
import time
import queue
import threading 
import signal
from _thread import *


q = queue.Queue()									#shared queue
lock = threading.Lock()								#lock


class myClass:
    def __init__(self, sender, table):				#router adds objects of this class to shared queue
        self.sender = sender
        self.table = table
        
def new_thread(router, file, N):
    graph = {}
    neighbours = []

    with open(file) as f:							#open the file
        matrix=[line.split() for line in f]
    nodes = matrix[1]
    matrix.pop(0)
    matrix.pop(0)

    #initializing the distances
    for i in nodes:
        if(i == router):
            graph[i] = float(0) 
        else:
            graph[i] = float('inf')

    for item in matrix:
        if(item[0] == router):									#if the first item is router itself
            graph[item[1]] = float(item[2])						#update the distance
            if(item[1] not in neighbours):
                neighbours.append(item[1])						#if not present in neighbours list, add ot
        if(item[1] == router):									#if the second item is router itself,similar process
            graph[item[0]] = float(item[2])
            if(item[0] not in neighbours):
                neighbours.append(item[0])

    lock.acquire()
    
    print("----------------------------------------------------------------------------------------------------------------------------------")
    print("					Hi!! I am router " + router + " 							")
    print("					meet my neighbours" )
    print("\t\t\t\t\t",*neighbours , sep="  ")
    print("----------------------------------------------------------------------------------------------------------------------------------")
    print("					Here is my initial status")
    print()
    for dst,w in graph.items():
        print("           				"+ router + ' --> ' + dst + ' = ' + str(w))
    print()
    print("----------------------------------------------------------------------------------------------------------------------------------")
    lock.release()

    tables = []
    iterationCount = 0

    while True:

        iterationCount += 1

        time.sleep(2)
        wrapper = myClass(router, graph)

        for i in range(len(neighbours)):
            lock.acquire()
            q.put(wrapper)
            lock.release()

        temp = neighbours

        #read neighbours table
        while True:																
            lock.acquire()
            if(q.empty()):
                lock.release()
                break
            if(q.queue[0].sender in temp):
                temp.remove(q.queue[0].sender)
                tables.append(q.get())
            lock.release()
        
        #bellman ford algorithm
        showUpdates = []
        for dst,w in graph.items():
            for table in tables:
                new_wt = graph[table.sender] + table.table[dst]					#get the new distance between the two nodes
                if(new_wt < w):													#if less that the previous distance
                    graph[dst] = new_wt
                    if(dst not in showUpdates):
                        showUpdates.append(dst)									#update it in the routing table

        lock.acquire()
        if(iterationCount > 2):													#stop after the given number of iteration. 2 over here. can be changed manually
        	lock.release()
        	print()
        	print("given number of iterations completed...")
        	print("Terminating the program...!!!!!!")
        	break
        print("----------------------------------------------------------------------------------------------------------------------------------")
        print("					Welcome again to router " + router )
        print("----------------------------------------------------------------------------------------------------------------------------------")
        #if(iterationCount > 2):
        #    lock.release()
        #    break
        print("					This is the " + str(iterationCount) + " iteration")
        print("					My current status is")
        print()
        for dst,w in graph.items():
            if(dst in showUpdates):											#if destination router is updated
                print("           				"+ router + ' --> ' + dst + ' = ' + str(w) + '***')
            else:															#if no updates in destination router
                print("           				"+ router + ' --> ' + dst + ' = ' + str(w))
        print()
        print("----------------------------------------------------------------------------------------------------------------------------------")
        time.sleep(0.5)														#waits for 0.5 sec
        lock.release()


script, file = argv  
fileobj = open(file)														#opening the file
numrouters = fileobj.readline()												#read the file
numrouters = int(numrouters)												# first line has total number of routers
routerinfostr = fileobj.readline()											# second line has names of all routers
routerinfolist = routerinfostr.split()										#following lines contains the routing info.
i = 0
while numrouters > 0:     													#counting the number of routers
    start_new_thread(new_thread, (routerinfolist[i], file, numrouters))		# creating a new thread for each router
    i += 1
    numrouters = numrouters - 1

while 1:
    pass
