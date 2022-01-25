#ifndef WIN32
#define WIN32
#endif

#include "Simple_window.h"
#include "Graph.h"
#include "Binary_tree.h"
#include "TriangleBinary_tree.h"
#include "std_lib_facilities.h"
#include <iostream>

int main() {
    int levels;
    cout << "Please input levels: ";
    cin >> levels;

    Simple_window win1(Point(100,100), 600, 400, "BinaryTree");
    Simple_window win2(Point(600,200), 600, 400, "BinaryTree");
    Binary_tree bin(levels);
    TriangleBinary_tree bin2(levels);

    bin.set_color(Color :: red);
    bin2.set_color(Color :: blue);

    win1.attach(bin);
    win2.attach(bin2);

    win2.wait_for_button();
    return 0;
}
