#include "std_lib_facilities.h"
#include "Polynomial.h"

string toString(float x){
    string s = to_string(x);
    // res = to_string((int)x)+'.'+to_string(abs((int)(x*10000))%10000);
    s.erase(s.find('.')+5);
    return s;
}

int main()
{
    /********** Begin **********/
    
    bool exercise1=true;
    if(exercise1)    {
    //第一关执行代码
		//Please fix Polynomial.h and Polynomial.cpp
    string str;          
    getline(cin,str);    
    Polynomial p(str);
    float l,u;
    cin>>l>>u;
    // cout<<p.derivation(x);
    // cout<<"error";
    if(p.if_error()){
      cout<<"error";
      return -1;
    }else{
      bool err_flag = false;
      float solution;
      solution = solve(p,l,u,&err_flag);
      if(err_flag){
        cout<<"error";
        return -1;
      }else{
        cout<<toString(solution);
      }
    }
      
    }   else     {
    //第二关执行代码
    //Please fix LinearEquations.h and LinearEquations.cpp

    cout<<"error";
    }
	/********** End **********/
  	return 0;
}

