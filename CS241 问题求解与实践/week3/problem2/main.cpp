#include "std_lib_facilities.h"
#include "LinearEquations.h"

int main()
{
    /********** Begin **********/
    
    bool exercise1=false;
    if(exercise1)    {
    //��һ��ִ�д���
		//Please fix Polynomial.h and Polynomial.cpp
      
    }   else     {
    //�ڶ���ִ�д���
    //Please fix LinearEquations.h and LinearEquations.cpp
    string str;
    LinearEquations l;
    while(getline(cin, str)){
      l.add_equation(str);
    }
    cout<<flush;
    l.solve();
    l.print_solutions();
    }
	/********** End **********/
  	return 0;
}