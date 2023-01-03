# ifndef _HYPERELLIPTIC_H_
# define _HYPERELLIPTIC_H_

# include "Graph.h"
# include <assert.h>
# include <vector>
# include <cmath>

using namespace Graph_lib;
using namespace std;

class Hyperelliptic : public Shape {
  private:
    double a, b, m, n;
    int N;

    Point center;

    vector <Point> points;

    Color lcolor;
    Line_style ls;

    void draw_lines() const;

  public:
    Hyperelliptic(double a, double b, double m, double n, int N , Point center);

    ~ Hyperelliptic() { };
};

# endif
