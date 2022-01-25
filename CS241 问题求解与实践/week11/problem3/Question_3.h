#pragma once
#include "std_lib_facilities.h"
class palindrome{
    vector<vector<int>> length,direction;
    string input;
    int get_length(int start,int end);
    string get_str(int start,int end);
    public:
        palindrome(){};
        void get_input();
        void calc();
};