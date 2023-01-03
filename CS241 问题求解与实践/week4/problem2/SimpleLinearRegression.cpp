#include "SimpleLinearRegression.h"


SimpleLinearRegression::SimpleLinearRegression():error(false){}
SimpleLinearRegression::~SimpleLinearRegression(){}

void SimpleLinearRegression::set_aim(const string& input){
    // if(sscanf(input.c_str(),"%lf",&aim_x)!=1) error = true;
    if(!input_one_double(input,aim_x)) error = true;
}

void SimpleLinearRegression::add_point(const string& input){
    double x,y;
    // if(sscanf(input.c_str(),"%lf%lf%lf",&x,&y,&temp)!=2) error = true;
    if(!input_two_double(input,x,y)) error = true;
    list.push_back({x,y});
}

void SimpleLinearRegression::solve(){
    double sum_x=0,sum_y=0,avg_x=0,avg_y=0;
    double r,a,b;
    int size = list.size();

    if(error||size<2||size>100) {
        cout<<"error\nerror\nerror";
        return;
        }

    for(auto &p:list){
      sum_x += p.x;
      sum_y += p.y;
    }
    avg_x = sum_x/size;
    avg_y = sum_y/size;

    double sum1=0,sum2=0,sum3=0;
    for(auto &p:list){
      double x_det,y_det;
      x_det = p.x- avg_x;
      y_det = p.y- avg_y;
      sum1 += x_det*y_det;
      sum2 += x_det*x_det;
      sum3 += y_det*y_det;
    }
    r = sum1/(sqrt(sum2)*sqrt(sum3));
    if(abs(r)<0.75){
      cout<<toString(r)<<"\nerror\nerror";
      return;
    }else{
      double sum4=0,sum5=0;
      for(auto &p:list){
        sum4 += p.x*p.y;
        sum5 += p.x*p.x;
      }
      a = (sum4-size*avg_x*avg_y)/(sum5-size*avg_x*avg_x);
      b = avg_y - a * avg_x;
      cout<<toString(r)<<endl;
      cout<<"y="<<toString(a)<<(b<0?"*x":"*x+")<<toString(b)<<endl;
      cout<< toString(a*aim_x+b);
    }
}

string SimpleLinearRegression::toString(const double x){
    string s = to_string(x);
    s.erase(s.find('.')+5);
    return s;
}

bool SimpleLinearRegression::input_two_double(const string &str, double &x, double &y) {
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
    if(index == lst) return false;
    if(index != str.size()) return false;
    if(f) y = -y;
    return true;
}

bool SimpleLinearRegression::input_one_double(const string &str, double &x) {
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
    if(index == f) return false;
    if(index != str.size()) return false;
    if(f) x = -x;
    return true;
}