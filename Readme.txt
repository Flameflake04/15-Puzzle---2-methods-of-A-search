Coding assignment: Iterative-deepening-search
Author: Duc Tran
The program helps user solved 16-puzzle by using 2 methods of A*. The program is written in Python.
To run the code, use latest version of Visual Studio Code, install Python 3.11.8 and install necessary library like time, psutil
System: Window 11
Python version: 3.11.8

		A* Manhattan Distance Node Expanded	A* Misplayed Tiles Node Expanded
Move 
D		2					2
UUURRRDDD	10					10
RRURDD		7					7
DRDRD		6					6
LDLDRR		7					7
RDLDDRR		8					8
DLLDRRDR	9					9
URDRURD		8					8
RULLDRDRD	13					22
LUUURDRDD	10					10

We see that A* Manhattan Distance always expanded node equal or less than Misplaced Tiles heuristic. This is due to the manhattan distance heuristic domainates the misplayed tiles heursitic. The heurisitic function with higher value (in this case h(manhattan distance) > h(misplayed tiles)) will provided faster and better search time. 