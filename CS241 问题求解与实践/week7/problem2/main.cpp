#include<iostream>
#include "std_lib_facilities.h"
#include<vector>
#include<queue>
#include<map>
using namespace std;

// vector<int> counter;
priority_queue<int,vector<int>,greater<int>> que;
map<string,int> counter;

bool check_chr(char c){
    if((c>='a'&&c<='z')||(c>='A'&&c<='Z')) return true;
    else return false;
}


int main(){
    // counter.resize(256);
    // for(auto &c:counter) c = 0;
    string line,input;
    while(getline(cin,line)){
        if(input!="") input += '\n';
        input += line;
    }
    // for(auto c:input){
    //     counter[c]++;
    // }

    int j=0;
    int unencodeable = 0;
    while(input[j]){
        if(check_chr(input[j])){
            string word;
            while(check_chr(input[j])){
                char chr = input[j];
                word += chr;
                j++;
            }
            auto word_counter = counter.find(word);
            if(word_counter==counter.end()) counter.insert(pair<string,int>(word,1));
            else{
                (*word_counter).second += 1;
            }
            // if(!(word[0]>='0'&&word[0]<='9')){
            //     // if(!in_comment) 
            //         // if(key_words.find(word)==key_words.end()) list.insert(word);
            //     auto word_counter = counter.find(word)
            //     if
            // }
        }else{
            unencodeable ++;
            j++;
        }
    }

    for(auto& c:counter){
        que.push(c.second);
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
    cout<<wpl+8*unencodeable;

}