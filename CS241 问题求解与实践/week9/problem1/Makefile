objects = main.o hyperelliptic.o
libpath = E:\C++\fltk\MinGW\lib
includepath = E:\C++\fltk\MinGW\include

main: $(objects)
	g++ -o main -L$(libpath) -L. $(objects) \
	-lbookgui \
	-lfltk_images -lfltk_png -lfltk_z -lfltk_jpeg \
	-lfltk -lole32 -luuid -lcomctl32 -lwsock32 -lm -lgdi32 -luser32 -lkernel32

%.o:%.cpp
	g++ -o $@ -c $< -I$(includepath)

clean:
	rm $(objects)

run: main
	./main
