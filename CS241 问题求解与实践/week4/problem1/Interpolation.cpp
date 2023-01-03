#include "Interpolation.h"

bool Interpolation::point::operator<(const Interpolation::point& other) const{
    return x<other.x;
}

Interpolation::Interpolation():error(false){};
Interpolation::~Interpolation(){};

void Interpolation::set_aim(const string& input){
    // if(sscanf(input.c_str(),"%lf",&aim_x)!=1) error = true;
    if(!input_one_double(input,aim_x)) error = true;
}

void Interpolation::add_point(const string& input){
    double x,y;
    // if(sscanf(input.c_str(),"%lf%lf%lf",&x,&y,&temp)!=2) error = true;
    if(!input_two_double(input,x,y)) error = true;
    list.push_back({x,y});
}

void Interpolation::solve(){
    if(error) {
        cout<<"error";
        return;
        }

    sort(list.begin(),list.end());

    double det = list[1].x - list[0].x;
    for(int i = 1;i<list.size();i++){
        if(abs((list[i].x - list[i-1].x)-det)>0.00001) error = true;
    }
    if(error) {
        cout<<"error";
        return;
        }

    int size = list.size();
    double** table;
    table = new double* [size];
    for(int i=0;i<size;i++) table[i] = new double[size];

    for(int i = 0;i < size;i++){
        table[i][0] = list[i].y;
    }
    for(int j = 1;j < size;j++){
        for(int i = j;i < size;i++){
            table[i][j] = table[i][j-1] - table[i-1][j-1];
        }
    }

    double t = (aim_x-list[0].x)/det;
    double ans = list[0].y;
    double coefficient = 1.0;
    for(int i = 1;i < size;i++){
        coefficient *= ((t+1-i)/i);
        ans += table[i][i]*coefficient;
    }
    cout<<toString(ans);
    for(int i=0;i<size;i++) delete[] table[i];
    delete[] table;
}

string Interpolation::toString(double& x){
    string s = to_string(x);
    s.erase(s.find('.')+5);
    return s;
}

bool Interpolation::input_two_double(const string &str, double &x, double &y) {
    bool f = 0; x = 0; y = 0;
    int index;
    if(str[0] == '-') f = 1;
    index = f;
    double base = 1.0;
    while(index < str.size() && isdigit(str[index]) || str[index] == '.') {
      if(str[index] == '.') {
        if(base != 1.0) return false;
        else base = 0.1;
      } else {
        if(base != 1.0) {
          x = x + base * (str[index] - '0');
          base *= 0.1;
        } else x = x * 10 + (str[index] - '0');
      }
      ++ index;
    }
    if(index == f) return false;
    if(f) x = -x;
    
    if(str[index] != ' ') return false;
    ++ index; f = 0; base = 1.0;
    if(str[index] == '-') f = 1, ++ index;
    int lst = index;
    
    while(index < str.size() && isdigit(str[index]) || str[index] == '.') {
      if(str[index] == '.') {
        if(base != 1.0) return false;
        else base = 0.1;
      } else {
        if(base != 1.0) {
          y = y + base * (str[index] - '0');
          base *= 0.1;
        } else y = y * 10 + (str[index] - '0');
      }
      ++ index;
    }
    while(str[index]==' '&&index < str.size()) ++index;
    if(index == lst) return false;
    if(index != str.size()) return false;
    if(f) y = -y;
    return true;
}

bool Interpolation::input_one_double(const string &str, double &x) {
    bool f = 0; x = 0;
    int index;
    if(str[0] == '-') f = 1;
    index = f;
    double base = 1.0;
    while(index < str.size() && isdigit(str[index]) || str[index] == '.') {
      if(str[index] == '.') {
        if(base != 1.0) return false;
        else base = 0.1;
      } else {
        if(base != 1.0) {
          x = x + base * (str[index] - '0');
          base *= 0.1;
        } else x = x * 10 + (str[index] - '0');
      }
      ++ index;
    }
    while(str[index]==' '&&index < str.size()) ++index;
    if(index == f) return false;
    if(index != str.size()) return false;
    if(f) x = -x;
    return true;
}