#include "LinearEquations.h"
// #include "Polynomial.h"

float solve(Polynomial& equation,float lower,float upper,bool* error){
    if(equation.calculate(lower)*equation.calculate(upper)>=0||lower>=upper){
        if(error) *error = true;
        return 0;
    }
    float fx,dfx,x,lx;
    // x = lower;
    // lx = upper;
    x = upper;
    lx = lower;
    while(abs(x-lx)>0.00002){
        lx = x;
        fx = equation.calculate(x);
        dfx = equation.derivation(x);
        if(dfx==0){
            if(error) *error = true;
            return 0;
        }else{
            x = x - fx/dfx;
            if(x<lower||x>upper){
                if(error) *error = true;
                return 0;
            }
        }
    }
    return x;
}
