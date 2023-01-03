# ifndef _BARCHART_H_
# define _BARCHART_H_

# include "Graph.h"
# include <iostream>
# include <assert.h>
# include <vector>
# include <cmath>

using namespace Graph_lib;
using namespace std;

const int Xsize_per_month = 65, Ysize_per_deg = 10;

class BarChart : public Shape {
  private:
    Fl_Color newYork_color,austin_color;
    static string double_2_str(double x);
    vector <double> newYork_avg, austin_avg;
    void draw_lines() const;

  public:
    BarChart() {
      newYork_avg.resize(13);
      austin_avg.resize(13);
      newYork_color = fl_rgb_color(0,0,255);
      austin_color = fl_rgb_color(13,150,106);
    }

    void load_data();

    ~ BarChart() { };
};

# endif
