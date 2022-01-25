#include<iostream>
#include "std_lib_facilities.h"
using namespace std;
int char2int(char c){
    if(c>='a'&&c<='z') return c - 'a';
    else if(c>='A'&&c<='Z') return c - 'A' + 26;
    else return -1;
}
class BinaryTree{
    struct node
    {
        bool exsist,has_parent;
        int left,right;
        node():exsist(false),has_parent(false),left(-1),right(-1){};
    };
    int root,max_level;
    vector<node> tree;
    void add_edge(const char first,const char second){
        int node_id = char2int(first);
        int parent_id = char2int(second);
        bool if_has_parent = second != 0;
        tree[node_id].exsist = true;
        if(if_has_parent){
            tree[node_id].has_parent = true;
            tree[parent_id].exsist = true;
            if(tree[parent_id].left == -1) tree[parent_id].left = node_id;
            else tree[parent_id].right = node_id;
        }
    };
    string encode_tree(const int root_id){
        string left_encode,right_encode,res;
        auto& n = tree[root_id];
        if(n.left!=-1) left_encode = encode_tree(n.left);
        if(n.right!=-1) right_encode = encode_tree(n.right);
        if(left_encode.length()>right_encode.length()||left_encode>right_encode){
            res = '1' + left_encode + right_encode + '0';
        }else{
            res = '1' + right_encode + left_encode + '0';
        }
        return res;
    }
    public:
    string encode_result;
    BinaryTree():root(-1),max_level(0){
        tree.resize(53);
    }
    void parser(string& input){
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
    void encode(){
        encode_result = encode_tree(root);
    }
    int count_level(){
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
};

int main(){
    // char c = 'a';
    // tree.resize(53);
    string line,input;
    BinaryTree tree1,tree2;
    getline(cin,line);
    tree1.parser(line);
    getline(cin,line);
    tree2.parser(line);
    tree1.encode();
    tree2.encode();
    cout<<tree1.count_level()<<' '<<tree2.count_level()<<endl;
    cout<<tree1.encode_result<<' '<<tree2.encode_result<<endl;
    if(tree1.encode_result==tree2.encode_result) cout<<"Yes";
    else cout<<"No";
    // int j = 0;
    // while(line[j]){
    //     if(line[j]=='<'){
    //         char first = 0,second = 0;
    //         j++;
    //         first = line[j];
    //         j++;
    //         if(line[j]=='>') add_edge(first,second);
    //         else{
    //             j++;
    //             second = line[j];
    //             j++;
    //             add_edge(first,second);
    //         }
    //     }
    //     j++;
    // }
    // int root = -1;
    // for(int i = 0; i<52 ;i++){
    //     auto& n = tree[i];
    //     if(n.exsist){
    //         if(!n.has_parent){
    //             root = i;
    //             break;
    //         }
    //     }
    // }
    // cout<<root<<endl;
    // string encode_result = encode_tree(root);
    // int level = 0,max_level = 0;
    // j = 0;
    // while(encode_result[j]){
    //     char c = encode_result[j];
    //     if(c=='1') level++;
    //     else{
    //         if(level>max_level) max_level = level;
    //         level --;
    //     }
    //     j++;
    // }
    // cout<<encode_result<<endl<<max_level;
}