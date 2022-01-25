#pragma once
#include "std_lib_facilities.h"

class subsequence{
    vector<int> data;
    bool error_flag;
    int n,count,input;
    public:
        subsequence();
        void get_input();
        void calc();
};
