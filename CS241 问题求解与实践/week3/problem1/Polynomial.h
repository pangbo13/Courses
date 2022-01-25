#include "std_lib_facilities.h"

#ifndef _Polynomial_h
#define _Polynomial_h
class Polynomial{
	float* coefficient;
    bool error;
    int max_exponent;
    string toString(const float x);
    public:
        Polynomial(string input);
        ~Polynomial();
        void print();
        float calculate(const float x);
        float derivation(const float x);
        bool if_error();
};

float solve(Polynomial& equation,float lower,float upper,bool* error=nullptr);

#endif