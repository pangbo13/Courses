#include "std_lib_facilities.h"
#include "Polynomial.h"

int main()
{
    //����ļ�Ŀ¼�޸�Polynomial.h��Polynomial.cpp����exercise_2.cpp
    /********** Begin **********/
    
    bool exercise1=true;
    if(exercise1)    {
    //��һ��ִ�д���
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
    //�ڶ���ִ�д���


    }
	/********** End **********/
  	return 0;
}

