#include "std_lib_facilities.h"
#include "Polynomial.h"

int main()
{
    //请打开文件目录修改Polynomial.h，Polynomial.cpp，和exercise_2.cpp
    /********** Begin **********/
    
    bool exercise1=true;
    if(exercise1)    {
    //第一关执行代码
    string str;          
    getline(cin,str); 

    double x;
    cin>>x;

    Polynomial p(str);
    p.print();
    cout<<endl;
    p.derivation();
    cout<<endl;
    p.calculate(x);
    
    }   else     {
    //第二关执行代码


    }
	/********** End **********/
  	return 0;
}

