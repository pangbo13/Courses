# include "righttriangle.h"

RightTriangle :: RightTriangle(Point c, double a, double b, double angle) :
  c(c), a(a), b(b), angle(angle), lcolor(fl_color()), ls(0) {
    //calculate();
    double beta = atan(a / b);
    add(Point(c.x, c.y));
    add(Point(c.x + a * cos(angle - beta), c.y + a * sin(angle - beta)));
    add(Point(c.x + b * cos(angle - beta + PI / 2), c.y + b * sin(angle - beta + PI / 2)));
  }
