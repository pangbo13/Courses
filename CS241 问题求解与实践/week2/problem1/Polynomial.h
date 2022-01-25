#include "std_lib_facilities.h"
class Polynomial{
	double* coefficient;
    bool error;
    int max_exponent;
    string toString(const double x);
    public:
        Polynomial(string input);
        ~Polynomial();
        void print();
        void calculate(const double x);
        void derivation();
};