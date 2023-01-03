#pragma once
#include "std_lib_facilities.h"
#include<unordered_map>
namespace SubGraphMerge_NS{
struct SubGraphInfo{
    int subGraph_id;
    string file_path;
    int node_count;
    float weight_sum;
};

struct edge{
    int start_node_id;
    int end_node_id;
    float weight;
    edge(int s,int e,float w):start_node_id(s),end_node_id(e),weight(w){};
};

struct node{
    int node_id;
    int belongs;
    vector<edge> edges;
    node(int id):node_id(id),belongs(0){};
    node(int id,int b_id):node_id(id),belongs(b_id){};
    node(){};
};

class subGraphMerge{
    vector<SubGraphInfo> SGInfo_List;
    unordered_map<int,node> Graph;
    void read_catalogue(string path);
    void read_SG(SubGraphInfo& sgi);
    public:
    void read(string path);
};

};