#pragma once
#include "std_lib_facilities.h"
#include<unordered_map>
#include<queue>
namespace SubGraphProcess_NS{
struct SubGraphInfo{
    int subGraph_id;
    string file_path;
    int node_count;
    float weight_sum;
};

struct edge{
    int start_node_id;
    int end_node_id;
    int end_node_belongs;
    float weight;
    edge(int s,int e,int eb,float w):start_node_id(s),end_node_id(e),end_node_belongs(eb),weight(w){};
};

struct node_path_info{
    int node_id;
    int sg_id;
    float weight;
    int pre_node_id;//上一个节点的id
    node_path_info(int nid,int sgid):node_id(nid),sg_id(sgid){};
    node_path_info(int nid,int sgid,float w):node_id(nid),sg_id(sgid),weight(w){};
    node_path_info(int nid,int sgid,float w,int p):node_id(nid),sg_id(sgid),weight(w),pre_node_id(p){};
};

struct node{
    int node_id;
    int belongs;
    vector<edge> edges;
    float shortest_weight;
    bool visited;
    int pre_node_id;
    node(int id):node_id(id),belongs(0),pre_node_id(-1){};
    node(int id,int b_id):node_id(id),belongs(b_id),shortest_weight(1e20),visited(false),pre_node_id(-1){};
    node(){};
};

struct _SubGraph{
    int sg_id;
    unordered_map<int,node> nodes;
    int node_count;
};

class SubGraphs{
    vector<SubGraphInfo> SGInfo_List;
    vector<_SubGraph> SubGraph_List;
    int SubGraphNum;
    void read_catalogue(string& path);
    void read_SG(SubGraphInfo& sgi);
    node* find_node_in_SubGraph(int sg_id,int node_id);
    pair<int,node*> find_node(int node_id);
    public:
    void read(string& path);
    vector<int> find_accessiable(int node_id);
    float find_shortest_path(int start_node_id,int end_node_id,vector<int>& shortest_path);
};
};