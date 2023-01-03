/*
    二分法求方程的解
    函数：
        int solve(double(*f)(double x),double lower,double upper,double& root,double accuracy=0.00001)
            - 参数1：需要求解的函数指针
            - 参数2&3：求解上下限
            - 参数4：求解结果的引用
            - 参数5[可选]：求解精度
            - 返回值：0表示正常，-1表示可能无解
*/

#include<iostream>
#include<math.h>
using namespace std;

int solve(double(*f)(double x),double lower,double upper,double& root,double accuracy=0.00001){
    double a,b,fa,fb,mid,fmid;
    a=lower;
    b=upper;
    fa = f(a);
    fb = f(b);
    if(fa*fb>0){
        return -1;
    }else if(fa==0){
        root = a;
        return 0;
    }else if(fb==0){
        root = b;
        return 0;
    }
    while(abs(b-a)>accuracy){
        mid=(a+b)/2;
        fmid = f(mid);
        if(fmid==0){
            break;
        }
        if(f(a)*fmid<0) b=mid;
        else a = mid;
    }
    root = mid;
    return 0;
}

double f(double x){
    return pow(x,3)+pow(x,2)+sin(x)+1;
}

int main(){
    double root,lower,upper;
    printf("请输入下限:");
    scanf("%lf",&lower);
    printf("请输入上限:");
    scanf("%lf",&upper);
    if(!solve(f,lower,upper,root)) printf("解为%lf",root);
    else printf("[%lf,%lf]区间上可能无解",lower,upper);
}