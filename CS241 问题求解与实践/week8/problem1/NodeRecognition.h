#include<iostream>
#include<stack>
#include "std_lib_facilities.h"
using namespace std;
class NodeRecognition{
    struct node
    {
        bool exsist,has_parent;
        vector<int> child;
        node():exsist(false),has_parent(false){};
    };
    struct GraphPart{
        int type,size,value;
        //type: 0-Node 1-BinaryTree 2-Tree 3-Graph
        GraphPart(int t,int s,int v):type(t),size(s),value(v){};
        bool operator<(const GraphPart& other){
            if(type==other.type){
                if(value==other.value) return size<other.size;
                else return value<other.value;
            }else return type<other.type;
        }
    };
    int graph_count;
    vector<node> Graph,GraphR;
    vector<int> root;
    vector<GraphPart> GraphPartList;
    void add_edge(const int first,const int second);
    public:
    NodeRecognition():graph_count(0){
        Graph.resize(110);
        GraphR.resize(110);
    }
    void parser(string& input);
    void process();
    void output();
};