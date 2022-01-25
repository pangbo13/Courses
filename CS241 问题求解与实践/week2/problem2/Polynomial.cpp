#include "std_lib_facilities.h"
#include "Polynomial.h"

Polynomial::Polynomial(){
    coefficient = new float[20];
    error = false;
    for(int i=0;i<20;i++) coefficient[i] = 0;
}

Polynomial::Polynomial(string input){
    coefficient = new float[20];
    error = false;
    max_exponent = 0;
    for(int i=0;i<20;i++) coefficient[i] = 0;

    int j = 0;
    while(input[j]){
        int integer = 0,decimal = 0,exponent = 0,sign = 1;
        float decimal_exponent = 1;
        if((!(input[j]>='0'&&input[j]<='9'))&&input[j]!='+'&&input[j]!='-'&&input[j]!='.'&&input[j]!='x'&&input[j]!='^'){
            error = true;
            break;
        }
        if(input[j]=='+'){
            sign = 1;
            j++;
            if(!(input[j]>='0'&&input[j]<='9')&&input[j]!='x'){
                error = true;
                break;
            }
        }else if(input[j]=='-'){
            sign = -1;
            j++;
            if(!(input[j]>='0'&&input[j]<='9')&&input[j]!='x'){
                error = true;
                break;
            }
        }
        while(input[j]>='0'&&input[j]<='9'){
            integer = integer*10+input[j]-'0';
            j++;
        }
        if(input[j]=='.'){
            j++;
            if(!(input[j]>='0'&&input[j]<='9')&&input[j]!='x'){
                error = true;
                break;
            }
            while(input[j]>='0'&&input[j]<='9'){
                decimal = decimal*10+input[j]-'0';
                decimal_exponent *= 0.1;
                j++;
            }
        }
        if(input[j]=='x'){
            exponent = 1;
            if(integer==0&&decimal==0) integer = 1;
            j++;
        }
        if(input[j]=='^'){
            j++;
            exponent = 0;
            if(!(input[j]>='0'&&input[j]<='9')){
                error = true;
                break;
            }
            while(input[j]>='0'&&input[j]<='9'){
                exponent = exponent*10+input[j]-'0';
                j++;
            }
        }
        coefficient[exponent] += sign*(integer+decimal*decimal_exponent);
        if(exponent>max_exponent) max_exponent = exponent;
    }
}

Polynomial::Polynomial(Polynomial& c){
    max_exponent = c.max_exponent;
    error = c.error;
    coefficient = new float[20];
    for(int i=0;i<20;i++){
        coefficient[i] = c.coefficient[i];
    }
}


Polynomial::~Polynomial(){
    delete[] coefficient;
}

string Polynomial::toString(float x){
    string s = to_string(x);
    // res = to_string((int)x)+'.'+to_string(abs((int)(x*10000))%10000);
    s.erase(s.find('.')+5);
    return s;
}

// string Polynomial::toString(const float val)
// {
//     char* chr;
//     chr = new char[20];
//     sprintf(chr, "%.4lf", val-0.000049);
//     string str(chr);
//     delete[] chr;
//     return str;
// }

void Polynomial::print(){
    if(error) {
        cout<<"error";
        return;
    }
    bool first = true,zero=true;
    for(int j=19;j>=0;j--){
        if(coefficient[j]!=0&&abs(coefficient[j])>0.00005){
            zero = false;
            if(first){
                first = false;
            }else if(coefficient[j]>0) cout<<'+';
            cout<<toString(coefficient[j]);
            if(j>1) cout<<"x^"<<j;
            else if(j==1) cout<<'x';
        }
    }
    if(zero) cout<<toString(0.0);
}

void Polynomial::derivation(){
    if(error) {
        cout<<"error";
        return;
    }
    bool first = true,zero=true;
    for(int j=19;j>=1;j--){
        if(coefficient[j]!=0){
            zero = false;
            if(first){
                first = false;
            }else if(coefficient[j]>0) cout<<'+';
            cout<<toString(coefficient[j]*j);
            if(j-1>1) cout<<"x^"<<j-1;
            else if(j==2) cout<<'x';
        }
    }
    if(zero) cout<<toString(0.0);
}

void Polynomial::calculate(const float x){
    if(error) {
        cout<<"error";
        return;
    }
    float ans = 0;
    for(int j=19;j>=0;j--){
        // if(coefficient[j]!=0){
        //     ans+=coefficient[j]*pow(x,j);
        // }
        ans = ans*x+coefficient[j];
    }
    cout<<toString(ans);
}

void divide(Polynomial f,Polynomial& s){
    Polynomial consult;
    if(s.max_exponent==0&&s.coefficient[0]==0){
        cout<<"error"<<endl<<"error";
        return;
    }
    consult.max_exponent = f.max_exponent-s.max_exponent;
    for(int i = f.max_exponent-s.max_exponent;i>=0;i--){
        float con = f.coefficient[i+s.max_exponent]/s.coefficient[s.max_exponent];
        consult.coefficient[i] = con;
        for(int j= s.max_exponent;j>=0;j--){
            f.coefficient[i+j] -= s.coefficient[j]*con;
        }
    }
    consult.print();
    cout<<endl;
    f.print();

}