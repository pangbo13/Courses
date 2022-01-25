#include<iostream>
#include "std_lib_facilities.h"
#include<vector>
#include<queue>
using namespace std;

vector<int> counter;
priority_queue<int,vector<int>,greater<int>> que;


int main(){
    counter.resize(256);
    for(auto &c:counter) c = 0;
    string line,input;
    while(getline(cin,line)){
        if(input!="") input += '\n';
        input += line;
    }
    for(auto c:input){
        counter[c]++;
    }
    for(auto c:counter){
        if(c!=0) que.push(c);
    }
    int wpl = 0;
    while(!que.empty()){
        int sum = 0;
        sum += que.top();
        que.pop();
        if(que.empty()) break;
        sum += que.top();
        que.pop();
        que.push(sum);
        wpl += sum;
    }
    cout<<wpl;

}