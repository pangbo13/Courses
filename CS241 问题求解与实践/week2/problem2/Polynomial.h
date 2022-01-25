#include "std_lib_facilities.h"
class Polynomial;
void divide(Polynomial f,Polynomial& s);
class Polynomial{
	float* coefficient;
    bool error;
    int max_exponent;
    string toString(const float x);
    public:
        Polynomial(string input);
        Polynomial();
        Polynomial(Polynomial& c);
        ~Polynomial();
        void print();
        void calculate(const float x);
        void derivation();
        friend void divide(Polynomial f,Polynomial& s);
};