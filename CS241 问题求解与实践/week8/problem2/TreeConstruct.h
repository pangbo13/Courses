#pragma once
#include "std_lib_facilities.h"

bool encode_string_compare(const string& f,const string& s);
int char2int(char c);
class BinaryTree{
    struct node
    {
        bool exsist,has_parent;
        vector<int> child;
        node():exsist(false),has_parent(false){};
    };
    int root,max_level;
    vector<node> tree;
    void add_edge(const char first,const char second);
    string encode_tree(const int root_id);
    public:
    string encode_result;
    BinaryTree();
    void parser(string& input);
    void encode();
    int count_level();
};