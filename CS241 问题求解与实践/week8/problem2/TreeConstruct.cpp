#include "TreeConstruct.h"

bool encode_string_compare(const string& f,const string& s){
    return f.length()>s.length()||f>s;
}
int char2int(char c){
    if(c>='a'&&c<='z') return c - 'a';
    else if(c>='A'&&c<='Z') return c - 'A' + 26;
    else return -1;
}

void BinaryTree::add_edge(const char first,const char second){
    int node_id = char2int(first);
    int parent_id = char2int(second);
    bool if_has_parent = second != 0;
    tree[node_id].exsist = true;
    if(if_has_parent){
        tree[node_id].has_parent = true;
        tree[parent_id].exsist = true;
        tree[parent_id].child.push_back(node_id);
    }
}
string BinaryTree::encode_tree(const int root_id){
    string left_encode,right_encode,res;
    auto& n = tree[root_id];
    vector<string> child_encode;
    child_encode.resize(n.child.size());
    for(int j = 0;j < n.child.size();j++){
        child_encode[j] = encode_tree(n.child[j]);
    }
    sort(child_encode.begin(),child_encode.end(),encode_string_compare);
    res = '1';
    for(auto& s:child_encode){
        res += s;
    }
    res += '0';
    return res;
}
BinaryTree::BinaryTree():root(-1),max_level(0){
    tree.resize(53);
}
void BinaryTree::parser(string& input){
    int j = 0;
    while(input[j]){
        if(input[j]=='<'){
            char first = 0,second = 0;
            j++;
            first = input[j];
            j++;
            if(input[j]=='>') add_edge(first,second);
            else{
                j++;
                second = input[j];
                j++;
                add_edge(first,second);
            }
        }
        j++;
    }
    for(int i = 0; i<52 ;i++){
        auto& n = tree[i];
        if(n.exsist){
            if(!n.has_parent){
                root = i;
                break;
            }
        }
    }
}
void BinaryTree::encode(){
    encode_result = encode_tree(root);
}
int BinaryTree::count_level(){
    int level = 0;
    int j = 0;
    while(encode_result[j]){
        char c = encode_result[j];
        if(c=='1') level++;
        else{
            if(level>max_level) max_level = level;
            level --;
        }
        j++;
    }
    return max_level;
}