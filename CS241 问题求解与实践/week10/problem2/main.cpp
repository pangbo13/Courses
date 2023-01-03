# include "Simple_window.h"
# include "Graph.h"
# include "AnalogClock.h"
# include "std_lib_facilities.h"
# include <iostream>
# include <math.h>

Simple_window win(Point(100, 100), 600, 500, "Analog Clock");
AnalogClock cl(Point(300,250));
void callback(void*){
    cl.update();
    win.clear_output();
    Fl::repeat_timeout(0.2,callback);
}

int main() {
    win.attach(cl);
    Fl::add_timeout(0.0,callback);//���ö�ʱ�����ص�����
    win.wait_for_button();
    return 0;
}
