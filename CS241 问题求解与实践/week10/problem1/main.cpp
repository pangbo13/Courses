# include "Simple_window.h"
# include "Graph.h"
# include "BarChart.h"
# include "std_lib_facilities.h"
# include <iostream>

int main() {
  Simple_window win(Point(100, 100), 1000, 600, "Temperature Bar Chart");

  BarChart bc;
  bc.load_data();
  win.attach(bc);

  win.wait_for_button();
  return 0;
}
