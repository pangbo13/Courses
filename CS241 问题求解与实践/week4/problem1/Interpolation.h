#pragma once
#include "std_lib_facilities.h"
class Interpolation{
    struct point{
        double x,y;
        bool operator<(const point& other) const;
    };
    vector<point> list;
    double aim_x;
    bool error;
    public:
    Interpolation();
    ~Interpolation();
    void set_aim(const string& input);
    void add_point(const string& input);
    void solve();
    bool input_two_double(const string &str, double &x, double &y);
    bool input_one_double(const string &str, double &x);
    string toString(double& x);
};

