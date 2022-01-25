//** coding: gbk

#include "SubGraphProcess.h"
using namespace SubGraphProcess_NS;
int main(){
    string path = "./data";
    SubGraphs sgs;
    try{sgs.read(path);}
    catch(const runtime_error& err){
        cerr<<err.what();
        return -1;
    }
    
    int op;
    int first_node_id,second_node_id;
    
    printf("Please choose your operation:\n");
    printf("1.Input one node and ouput all nodes that accessible.\n");
    printf("2.Input two nodes and ouput "
            "the length of the shortest path between these nodes.\n");
    scanf("%d",&op);

    if(op==1){
        printf("Please input ID of the node:");
        scanf("%d",&first_node_id);
        auto node_list = sgs.find_accessiable(first_node_id);
        if(node_list.size()>0){
            printf("Nodes can access:\n");
            for(auto i:node_list) printf("%d ",i);
        }else{
            printf("Cannot find the node.");
        }
    }else if(op==2){
        printf("Please input ID of the two nodes:");
        scanf("%d %d",&first_node_id,&second_node_id);
        vector<int> shortest_path;
        float res = sgs.find_shortest_path(first_node_id,second_node_id,shortest_path);
        if(res == -1) printf("Cannot find the first node.");
        else if(res == -2) printf("Cannot find the second node.");
        else if(res == -3) printf("There is no path between two nodes.");
        else {
            printf("The length of the shortest path is %.2f\n",res);
            printf("The path is:\n");
            for(auto n:shortest_path) printf("%d ",n);
        }
    }else printf("Invalid choice.");
}