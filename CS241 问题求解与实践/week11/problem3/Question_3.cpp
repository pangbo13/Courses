#include "Question_3.h"

void palindrome::get_input(){
    getline(cin,input);
    int len = input.length();
    length.resize(len);
    direction.resize(len);
    for(int i=0;i<len;i++){
        length[i].resize(len,-1);
        direction[i].resize(len,-1);
    }
}
int palindrome::get_length(int start,int end){
    if(start>=end) return 0;
    if(length[start][end]!=-1) return length[start][end];
    int ans = 0;
    if(input[start]==input[end]){
        direction[start][end] = 0;
        ans = 1+get_length(start+1,end-1);
        length[start][end] = ans;
        return ans;
    }
    int len_l,len_r;
    len_l = get_length(start+1,end);
    len_r = get_length(start,end-1);
    if(len_l>=len_r){
        ans = len_l;
        direction[start][end] = 1;
        length[start][end] = ans;
        return ans;
    }else{
        ans = len_r;
        direction[start][end] = 2;
        length[start][end] = ans;
        return ans;
    }
}

string palindrome::get_str(int start,int end){
    if(start>=end) return "";
    else switch(direction[start][end]){
        case 0:
            return input[start] + get_str(start+1,end-1) + input[end];
            break;
        case 1:
            return get_str(start+1,end);
            break;
        case 2:
            return get_str(start,end-1);
            break;
        default:
            return "";
    }
}

void palindrome::calc(){
    int len = input.length();
    get_length(0,len-1);
    cout<<get_str(0,len-1);
}