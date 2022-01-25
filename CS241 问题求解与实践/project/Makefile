libpath = E:\C++\fltk\MinGW\lib
includepath = E:\C++\fltk\MinGW\include

all: p1 p2 p3 p4
	rm *.o

all_gui: p1 p2 p3 p4 p1_gui
	rm *.o

p1: GraphGenerator.o problem1.o
	g++ -o p1 GraphGenerator.o problem1.o

p1_gui: problem1_gui.o GraphGenerator.o
ifeq ($(OS),Windows_NT) 
	g++ -o p1_gui -L$(libpath) problem1_gui.o GraphGenerator.o \
	-lfltk -lole32 -luuid -lcomctl32 -lgdi32 -luser32 -lkernel32 -lComdlg32
else
	g++ -o p1_gui -L$(libpath) problem1_gui.o GraphGenerator.o -lfltk
endif
	
p2: GraphSplit.o problem2.o
	g++ -o p2 GraphSplit.o problem2.o -O3

p3: SubGraphMerge.o problem3.o
	g++ -o p3 SubGraphMerge.o problem3.o

p4: SubGraphProcess.o problem4.o
	g++ -o p4 SubGraphProcess.o problem4.o

%.o:%.cpp
	g++ -o $@ -c $< -O3

problem1_gui.o:problem1_gui.cpp
	g++ -o $@ -c $< -I$(includepath)

clean:
	rm *.o