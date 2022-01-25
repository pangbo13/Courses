#include "std_lib_facilities.h"
#define Max_Equations 100
#define Max_Unknowns 100
class LinearEquations{
    double* matrix[Max_Equations] = {0};
    double* solution;
    int equations_count,unknowns_count,max_unknown_id;
    bool error;
    public:
    LinearEquations();
    ~LinearEquations();
    void add_equation(string& input);
    void solve();
    void print();
    void print_solutions();
    string toString(double &x);
};