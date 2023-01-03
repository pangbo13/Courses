objects = main.o Graph.o GUI.o Simple_window.o Window.o righttriangle.o
libpath = E:\C++\fltk\MinGW\lib
includepath = E:\C++\fltk\MinGW\include

main: $(objects)
	g++ -O2 -s -o main -L$(libpath) $(objects) \
	-lfltk_images -lfltk_png -lfltk_z -lfltk_jpeg \
	-lfltk -lole32 -luuid -lcomctl32 -lwsock32 -lm -lgdi32 -luser32 -lkernel32

%.o:%.cpp
	g++ -O2 -s -o $@ -c $< -I$(includepath)

clean:
	rm $(objects)

run: main
	./main
