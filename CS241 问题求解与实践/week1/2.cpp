/*
    ���ַ��󷽳̵Ľ�
    ������
        int solve(double(*f)(double x),double lower,double upper,double& root,double accuracy=0.00001)
            - ����1����Ҫ���ĺ���ָ��
            - ����2&3�����������
            - ����4�������������
            - ����5[��ѡ]����⾫��
            - ����ֵ��0��ʾ������-1��ʾ�����޽�
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
    printf("����������:");
    scanf("%lf",&lower);
    printf("����������:");
    scanf("%lf",&upper);
    if(!solve(f,lower,upper,root)) printf("��Ϊ%lf",root);
    else printf("[%lf,%lf]�����Ͽ����޽�",lower,upper);
}