#pragma once
#include "std_lib_facilities.h"
class SimpleLinearRegression{
    struct point{
        double x,y;
    };
    vector<point> list;
    double aim_x;
    bool error;
    public:
    SimpleLinearRegression();
    ~SimpleLinearRegression();
    void set_aim(const string& input);
    void add_point(const string& input);
    void solve();
    bool input_two_double(const string &str, double &x, double &y);
    bool input_one_double(const string &str, double &x);
    string toString(const double x);
};