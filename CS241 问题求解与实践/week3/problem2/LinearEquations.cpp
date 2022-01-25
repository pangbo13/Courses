#include "LinearEquations.h"

LinearEquations::LinearEquations():
    equations_count(0),unknowns_count(0),error(false),max_unknown_id(0),solution(nullptr){}

LinearEquations::~LinearEquations(){
    for(int i = 0;i < equations_count;i++) delete[] matrix[i];
    if(solution) delete[] solution;
}

string LinearEquations::toString(double& x){
    string s = to_string(x);
    s.erase(s.find('.')+5);
    return s;
}

void LinearEquations::add_equation(string& input){
    matrix[equations_count] = new double[Max_Unknowns+1];
    double* coefficient = matrix[equations_count];
    for(int i=0;i<Max_Unknowns+1;i++) coefficient[i]=0;
    equations_count++;
    
    int j = 0;
    while(input[j]){
        int integer = 0,decimal = 0,unknown_id = 0,sign = 1;
        double decimal_exponent = 1;
        bool after_equation=false;
        if((!(input[j]>='0'&&input[j]<='9'))&&input[j]!='+'&&input[j]!='-'&&input[j]!='.'&&input[j]!='x'&&input[j]!='_'&&input[j]!='='){
            error = true;
            break;
        }
        if(input[j]=='='){
            if(after_equation){
                error = true;
                break;
            }else {
                after_equation = true;
                j++;
                }
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
        if(input[j]=='x'&&input[j+1]=='_'){
            j+=2;
            if(integer==0&&decimal==0) integer = 1;
            unknown_id = 0;
            if(!(input[j]>='0'&&input[j]<='9')){
                error = true;
                break;
            }
            while(input[j]>='0'&&input[j]<='9'){
                unknown_id = unknown_id*10+input[j]-'0';
                j++;
            }
        }
        sign = sign * (after_equation?-1:1); //如果已经读取到过等号，移项后符号相反
        coefficient[unknown_id] += sign*(integer+decimal*decimal_exponent);
        if(unknowns_count<unknown_id) unknowns_count = unknown_id;
    }
}

void LinearEquations::print(){
    for(int i=0;i<equations_count;i++){
        for(int j=0;j<=unknowns_count;j++) cout<<matrix[i][j]<<" ";
        cout<<endl;
    }
}

void LinearEquations::solve(){
    if(error) return;
    if(unknowns_count>equations_count){
        error = true;
        return;
    }

    for(int line_index = 0;line_index<equations_count;line_index++){
        for(int i = line_index;i<equations_count;i++){
            if(matrix[i][unknowns_count-line_index]!=0){
                //交换两行
                double* temp;
                temp = matrix[line_index];
                matrix[line_index] = matrix[i];
                matrix[i] = temp;
                break;//找到第一个非零即可
            }
        }
        if(matrix[line_index][unknowns_count-line_index]==0){
            //交换之后还为零，说明没有交换，无穷解
            error = true;
            return;
        }else{
            for(int i = line_index+1;i<equations_count;i++){
                double consult = matrix[i][unknowns_count-line_index]/matrix[line_index][unknowns_count-line_index];
                for(int j = 0;j<=unknowns_count-line_index;j++){
                    matrix[i][j] -= matrix[line_index][j]*consult;
                    if(abs(matrix[i][j])<0.00000002) matrix[i][j] = 0; //解决精度问题导致残留
                }
                // print();
            }
        }
    }
    //开始回带
    if(equations_count>unknowns_count){     //未知数数量小于方程数
        for(int i = unknowns_count;i<equations_count;i++){
            if(matrix[i][0]!=0){
                error = true;
                return;
            }
        }
    }
    solution = new double[unknowns_count+1];
    for(int i = equations_count-1;i>=0;i--){
        //开始解x_{equations_count-i}，位于第i行
        double temp = -matrix[i][0];
        for(int j=equations_count-i-1;j>0;j--){
            temp -= matrix[i][j] * solution[j];
        }
        solution[equations_count-i] = temp/matrix[i][equations_count-i];
    }

}

void LinearEquations::print_solutions(){
    if(error) cout<<"error";
    else for(int i = 1;i<=unknowns_count;i++) printf("%s ",toString(solution[i]).c_str());
}
