/*
    Romberg���ַ�

    �ࣺ
        Romberg
            ���캯����
                - ����1����������ָ��
                - ����2&3��Ϊ�������ޡ�����
            ��Ա������
                double calculate(double accuracy=0.0001)
                    - ִ�м��㣬ÿһ�ε��ûḴ����һ�ε��õĽ��������еĻ���
                    - ����1[��ѡ]�� ָ�����㾫��

*/

#include<iostream>
#include<vector>
#include<math.h>
using namespace std;

class Romberg{
    // double _accuracy;
    double _upper,_lower;
    int t; //��������
    vector<double*> data;
    double& get_data(int _k,int _m);
    double (*integral_function)(double x);
    public:
        Romberg(double(*f)(double x),double upper,double lower);
        ~Romberg();
        double calculate(double accuracy=0.0001);
};

//���屻������
double f(double x){
    return 1/(x+1);
}

int main(){
    Romberg problem(f,1.5,0);

    cout<<problem.calculate()<<endl;
}

Romberg::Romberg(double(*f)(double x),double upper,double lower):
    integral_function(f),_upper(upper),_lower(lower){
    t = 0;
    data.push_back(new double[1]);
}

Romberg::~Romberg(){
        for(auto p:data) delete[] p;
}

double Romberg::calculate(double accuracy){

    if(t==0) get_data(0,0) = (integral_function(_upper)+integral_function(_lower))*(_upper-_lower)/2;
    else if(abs(get_data(0,t)-get_data(0,t-1))>accuracy) return get_data(0,t);
    
    do{
        t ++;
        //����m=0
        data.push_back(new double[t]);
        double temp = 0;
        for(int j=0;j<=pow(2,t-1)-1;j++) 
            temp += integral_function(_lower+(2*j+1)*(_upper-_lower)/pow(2,t));
        get_data(t,0) = 0.5*get_data(t-1,0) + temp*(_upper-_lower)/pow(2,t);

        //��m=1,k=t-1�����㵽k=0,m=t
        for(int m = 1;m <= t;m++)
            get_data(t-m,m) = (pow(4,m)*get_data(t-m+1,m-1)-get_data(t-m,m-1))/(pow(4,m)-1);

    }while(abs(get_data(0,t)-get_data(0,t-1))>accuracy);
    return get_data(0,t);
}

double& Romberg::get_data(int _k,int _m){
    return data[_k+_m][_m];
}