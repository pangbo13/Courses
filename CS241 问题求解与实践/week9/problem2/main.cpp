#include "Simple_window.h"
#include "Graph.h"
#include "std_lib_facilities.h"
#include "righttriangle.h"
#include <iostream>

int main() {
    Simple_window win(Point(100,200), 600, 400, "RightTriangle");

    double A = 100.0, B = 50.0;

    Color colors[8] = {Color::blue,Color::green,Color::yellow,Color::white,Color::red,Color::black,Color::magenta,Color::cyan};

    RightTriangle *tri[8];
    double cx,cy,nx,ny,angle = 0;
    cx = 100;
    cy = 200;
    for(int i = 0;i<8;++i){
        tri[i] = new RightTriangle(Point(cx,cy),A,B,angle);
        tri[i] -> set_color(colors[i]);
        win.attach(*tri[i]);
        double beta = atan(A / B);
        cx = cx + A * cos(angle - beta );
        cy = cy + A * sin(angle - beta );
        angle += PI/4;
    }

    win.wait_for_button();

    for (int i = 0; i < 8; ++ i) delete tri[i];
    return 0;
}
