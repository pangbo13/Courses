#include "std_lib_facilities.h"
#include "Polynomial.h"

int main()
{
    //����ļ�Ŀ¼�޸�Polynomial.h��Polynomial.cpp����exercise_2.cpp
    /********** Begin **********/
    
    bool exercise1=false;
    if(exercise1)    {
    //��һ��ִ�д���
    string str;          
    getline(cin,str); 

    float x;
    cin>>x;

    Polynomial p(str);
    p.print();
    cout<<endl;
    p.derivation();
    cout<<endl;
    p.calculate(x);
    
    }   else     {
    //�ڶ���ִ�д���
    string str1,str2;          
    getline(cin,str1);
    getline(cin,str2);
    Polynomial f(str1),s(str2);
    divide(f,s);
    }
	/********** End **********/
  	return 0;
}
