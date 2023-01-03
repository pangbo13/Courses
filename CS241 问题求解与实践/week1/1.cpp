/*
    Romberg积分法

    类：
        Romberg
            构造函数：
                - 参数1：被积函数指针
                - 参数2&3：为积分上限、下限
            成员函数：
                double calculate(double accuracy=0.0001)
                    - 执行计算，每一次调用会复用上一次调用的结果（如果有的话）
                    - 参数1[可选]： 指定计算精度

*/

#include<iostream>
#include<vector>
#include<math.h>
using namespace std;

class Romberg{
    // double _accuracy;
    double _upper,_lower;
    int t; //迭代次数
    vector<double*> data;
    double& get_data(int _k,int _m);
    double (*integral_function)(double x);
    public:
        Romberg(double(*f)(double x),double upper,double lower);
        ~Romberg();
        double calculate(double accuracy=0.0001);
};

//定义被积函数
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
        //计算m=0
        data.push_back(new double[t]);
        double temp = 0;
        for(int j=0;j<=pow(2,t-1)-1;j++) 
            temp += integral_function(_lower+(2*j+1)*(_upper-_lower)/pow(2,t));
        get_data(t,0) = 0.5*get_data(t-1,0) + temp*(_upper-_lower)/pow(2,t);

        //从m=1,k=t-1，计算到k=0,m=t
        for(int m = 1;m <= t;m++)
            get_data(t-m,m) = (pow(4,m)*get_data(t-m+1,m-1)-get_data(t-m,m-1))/(pow(4,m)-1);

    }while(abs(get_data(0,t)-get_data(0,t-1))>accuracy);
    return get_data(0,t);
}

double& Romberg::get_data(int _k,int _m){
    return data[_k+_m][_m];
}