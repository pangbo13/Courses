#pragma once

#include "Graph.h"
#include "Simple_window.h"
#include "std_lib_facilities.h"
#include <time.h>
#include <math.h>
#include <iostream>

#define PI 3.1415926

using namespace Graph_lib;

class AnalogClock : public Graph_lib :: Shape {
    private:
        const double second_length = 180,minute_length = 100, hour_length = 60;
        Point center;
        void draw_lines() const;
        
    public:
        AnalogClock(Point c):center(c) {}
        void update();
        ~AnalogClock(){}
};
