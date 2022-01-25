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
        // enum graph_type{Node=0,BinaryTree,Tree,Graph} type;
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
    void add_edge(const int first,const int second){
        int node_id = first;
        int parent_id = second;
        bool if_has_parent = second != -1;
        if(node_id>Graph.size()-5){
            Graph.resize(node_id+10);
            GraphR.resize(node_id+10);
        }
        Graph[node_id].exsist = true;
        GraphR[node_id].exsist = true;
        if(if_has_parent){
            if(parent_id>Graph.size()-5){
                Graph.resize(parent_id+10);
                GraphR.resize(parent_id+10);
            }
            Graph[node_id].has_parent = true;
            Graph[parent_id].exsist = true;
            Graph[parent_id].child.push_back(node_id);
            GraphR[parent_id].exsist = true;
            GraphR[parent_id].has_parent = true;
            GraphR[node_id].child.push_back(parent_id);
        }
    };
    public:
    NodeRecognition():graph_count(0){
        Graph.resize(110);
        GraphR.resize(110);
    }
    void parser(string& input){
        int j = 0;
        while(input[j]){
            if(input[j]=='<'){
                int first = -1,second =-1;
                j++;
                if(input[j]=='>'){
                    j++;
                    continue;
                };
                first = 0;
                while(input[j]>='0'&&input[j]<='9'){
                    first = first*10 + (input[j]-'0');
                    j++;
                }
                if(input[j]=='>') add_edge(first,second);
                else{
                    j++;
                    second = 0;
                    while(input[j]>='0'&&input[j]<='9'){
                        second = second*10 + (input[j]-'0');
                        j++;
                    }
                    add_edge(first,second);
                }
            }
            j++;
        }
        for(int i = 0; i<Graph.size() ;i++){
            auto& n = Graph[i];
            if(n.exsist){
                if(!n.has_parent){
                    root.push_back(i);
                }
            }
        }
    }
    void process(){
        vector<bool> visted;
        visted.resize(Graph.size());
        for(int j = 0;j<visted.size();j++) visted[j]= false;
        
        for(auto r:root){
            if(visted[r]) continue;
            //发现了未被访问的根节点
            int size = 0,value = 0;
            bool tree = true,binary_tree = true;
            graph_count++;
            //判断是不是单独节点
            if(!GraphR[r].has_parent){
                visted[r] = true;
                size = 1;
                value = r;
                GraphPartList.push_back(GraphPart(0,size,value));
            }else{
                //开始DFS搜索
                stack<int> dfs_stack;
                dfs_stack.push(r);
                while(!dfs_stack.empty()){
                    int node_id = dfs_stack.top();
                    dfs_stack.pop();
                    if(visted[node_id]) continue;
                    visted[node_id] = true;
                    size++;
                    value += node_id;
                    //判断是不是树,原图有不超过一个父亲，反图不超过一个儿子
                    if(GraphR[node_id].child.size()>1){
                        tree = false;
                        //如果不只一个父节点，全部放入栈中
                        for(auto n:GraphR[node_id].child) dfs_stack.push(n);
                    }
                    //判断是不是二叉树
                    if(!tree||Graph[node_id].child.size()>2) binary_tree = false;
                    //所有儿子节点入栈
                    for(auto n:Graph[node_id].child) dfs_stack.push(n);
                }
                if(binary_tree) GraphPartList.push_back(GraphPart(1,size,value));
                else if(tree) GraphPartList.push_back(GraphPart(2,size,value));
                else GraphPartList.push_back(GraphPart(3,size,value));
            }
            }
        //对剩下结点扫描一遍
        for(int j = 0;j < Graph.size();j++){
            if(!Graph[j].exsist||visted[j]) continue;
            int size = 0,value = 0;
            graph_count++;
            //开始DFS搜索
            stack<int> dfs_stack;
            dfs_stack.push(j);
            while(!dfs_stack.empty()){
                int node_id = dfs_stack.top();
                dfs_stack.pop();
                if(visted[node_id]) continue;
                visted[node_id] = true;
                size++;
                value += node_id;
                for(auto n:GraphR[node_id].child) dfs_stack.push(n);
                for(auto n:Graph[node_id].child) dfs_stack.push(n);
                }
            GraphPartList.push_back(GraphPart(3,size,value));
            }
            sort(GraphPartList.begin(),GraphPartList.end());
        }
    void output(){
        
        cout<<"We have recognized "<<graph_count<<" graph"<<(graph_count>1?"s.":".")<<endl;
        for(auto& g:GraphPartList){
            cout<<"--";
            switch(g.type){
                case 0:
                    cout<<"Node";
                    break;
                case 1:
                    cout<<"Binary tree";
                    break;
                case 2:
                    cout<<"Tree";
                    break;
                case 3:
                    cout<<"Graph";
                    break;
            }
            cout<<". Weight: "<<g.value<<". Size: "<<g.size<<"."<<endl;

        }
    }
};

int main(){
    string line,input;
    NodeRecognition G;
    getline(cin,line);
    G.parser(line);
    G.process();
    G.output();
}