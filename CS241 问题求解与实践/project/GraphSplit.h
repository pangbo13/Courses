#pragma once
#include "std_lib_facilities.h"
#include<unordered_map>
#include<set>
#include<map>

#define FILE_DEBUG_INFO
namespace GraphSplit_NS{
//��
struct edge{
    int start_node_id;
    int end_node_id;
    double weight;
    edge(int s,int e,double w):start_node_id(s),end_node_id(e),weight(w){};
};
//�ڵ�
struct node{
    int node_id;
    int belongs;
    double weight_sum;
    vector<edge> edges;
    node(int id):node_id(id),belongs(0),weight_sum(-1){};
    node(){};
};
//��ѡ�ڵ�
struct candidate_node
{
    int node_id;
    double subsplit_cost;
    candidate_node(int id):node_id(id),subsplit_cost(0){};
};
//��ͼ
struct SubGraph{
    set<int> nodes;
    int subGraph_id;
    double weight_sum;
    int node_count;
    SubGraph(int id):subGraph_id(id),weight_sum(0),node_count(0){}; 
};

class GraphSplit{
    unordered_map<int,node> Graph,GraphR;
    public:
    double edge_weight_sum;//ͼ�б�Ȩֵ�ͣ������Ի���
    double subgraph_weight_sum;//��ͼ�б�Ȩֵ�ܺ�
    private:
    vector<SubGraph*> sg_list; 
    vector<SubGraph*> saved_sg_list; 
    class splitor{
        //splitor�����ڹ����и����ͼ�����е���ʱ����
        SubGraph* sg;
        int DEMARCATION;
        int maxN;
        int current_node_id;//���ڱ��浱ǰ���ڴ���Ľڵ�id
        unordered_map<int,node>&Graph,&GraphR;
        map<int,candidate_node> cnodes;
        public:
            splitor(SubGraph* sg_p,int max_N,int demarcation,unordered_map<int,node>&G,unordered_map<int,node>&GR)
                :sg(sg_p),DEMARCATION(demarcation),maxN(max_N),Graph(G),GraphR(GR){}
            void update_cost();
            int find_first_node();
            int find_node();
            void add_node(int node_id);
    };
    void read_file(string& path);
    void init();
    void clear_cache();
    void clear_saved();
    double split(int maxN,int demarcation);
    void load_saved_before_write();
    public:
    GraphSplit(string path);
    ~GraphSplit();
    double split(int maxN);
    void write(string path);
};

};