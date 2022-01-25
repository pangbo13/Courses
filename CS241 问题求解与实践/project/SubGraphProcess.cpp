//** coding: gbk

#include "SubGraphProcess.h"
using namespace SubGraphProcess_NS;
void SubGraphs::read_catalogue(string& path){
    ifstream fin;
    char temp_flush[200];
    fin.open((path+"/catalogue.txt").c_str(),ios::in);
    if(!fin) throw runtime_error(string("FILE ERROR:Cannot load the file:")+path+"/catalogue.txt");
    string input_line;
    while(getline(fin,input_line)){
        SubGraphInfo sgi;
        sscanf(input_line.c_str(),"%d %s %d %f",&sgi.subGraph_id,temp_flush,&sgi.node_count,&sgi.weight_sum);
        sgi.file_path = path +'/'+ temp_flush;
        SGInfo_List.push_back(sgi);
    }
    fin.close();
}
void SubGraphs::read_SG(SubGraphInfo& sgi){
    ifstream fin;
    fin.open(sgi.file_path.c_str(),ios::in);
    string input_line;
    SubGraph_List[sgi.subGraph_id].sg_id = sgi.subGraph_id;
    auto& Graph = SubGraph_List[sgi.subGraph_id].nodes;
    while(getline(fin,input_line)){
        if(input_line[0]=='#') continue;//忽略以#开始的行，便于添加注释
        int args_num,num1,num2,num3;
        float num4;
        if(input_line.find('@')!=string::npos){
            args_num = sscanf(input_line.c_str(),"<%d %d@%d %f>",&num1,&num2,&num3,&num4);
            if(Graph.find(num1) == Graph.end()){
                Graph[num1] = node(num1,sgi.subGraph_id);
            }
            Graph[num1].edges.push_back(edge(num1,num2,num3,num4));
        }else{
            args_num = sscanf(input_line.c_str(),"<%d %d %f>",&num1,&num2,&num4);
            if(args_num == 1){
                auto node_p = Graph.find(num1);
                if(node_p == Graph.end()){
                    Graph[num1] = node(num1,sgi.subGraph_id);
                }
            }else{
                if(Graph.find(num1) == Graph.end()){
                    Graph[num1] = node(num1,sgi.subGraph_id);
                }
                if(Graph.find(num2) == Graph.end()){
                    Graph[num2] = node(num2,sgi.subGraph_id);
                }
                Graph[num1].edges.push_back(edge(num1,num2,sgi.subGraph_id,num4));
            }
        }
    }
    SubGraph_List[sgi.subGraph_id].node_count = Graph.size();
}
node* SubGraphs::find_node_in_SubGraph(int sg_id,int node_id){
    auto& Graph = SubGraph_List[sg_id].nodes;
    auto find_result = Graph.find(node_id);
    if(find_result==Graph.end()) return nullptr;
    else return &(*find_result).second;
}
void SubGraphs::read(string& path){
    read_catalogue(path);
    SubGraphNum = SGInfo_List.size();
    SubGraph_List.resize(SubGraphNum+1);
    for(auto& sgi:SGInfo_List){
        read_SG(sgi);
    }
}
pair<int,node*> SubGraphs::find_node(int node_id){
    int sg_id;
    node* target_node = nullptr;
    for(int i=1;i<=SubGraphNum;i++){
        target_node = find_node_in_SubGraph(i,node_id);
        if(target_node)break;
    }
    if(target_node){
        sg_id = target_node->belongs;
        return {sg_id,target_node};
    }else return {-1,target_node};
}
vector<int> SubGraphs::find_accessiable(int node_id){
    queue<node_path_info> que;
    vector<int> visted_node;
    int sg_id = find_node(node_id).first;
    if(sg_id!=-1){
        que.push({node_id,sg_id});
    }else return {};
    while(!que.empty()){
        auto cur_node_info = que.front();
        que.pop();
        auto& cur_node = SubGraph_List[cur_node_info.sg_id].nodes[cur_node_info.node_id];
        if(cur_node.visited) continue;
        cur_node.visited = true;
        for(auto& e:cur_node.edges){
            que.push({e.end_node_id,e.end_node_belongs});
        }
        visted_node.push_back(cur_node_info.node_id);
    }
    sort(visted_node.begin(),visted_node.end());
    return visted_node;
}
float SubGraphs::find_shortest_path(int start_node_id,int end_node_id,vector<int>& shortest_path){
        queue<node_path_info> que;
        auto first_node = find_node(start_node_id);
        int sg_id = first_node.first;
        if(sg_id!=-1){
            que.push({start_node_id,sg_id,0,-1});
        }else return -1;//找不到开始节点
        first_node.second->shortest_weight = 0;
        while(!que.empty()){
            auto cur_node_info = que.front();
            que.pop();
            auto& cur_node = SubGraph_List[cur_node_info.sg_id].nodes[cur_node_info.node_id];
            if(cur_node.visited&&cur_node.shortest_weight<cur_node_info.weight) continue;
            cur_node.visited = true;
            cur_node.shortest_weight = cur_node_info.weight;
            cur_node.pre_node_id = cur_node_info.pre_node_id;
            for(auto& e:cur_node.edges){
                que.push({e.end_node_id,e.end_node_belongs,e.weight+cur_node.shortest_weight,cur_node.node_id});
            }
        }
        auto end_node = find_node(end_node_id);
        if(end_node.first==-1) return -2; //找不到结束节点
        if(!end_node.second->visited) return -3; //两节点之间不存在道路
        shortest_path.clear();
        int cur_node_id = end_node_id;
        while(cur_node_id!=-1){
            shortest_path.push_back(cur_node_id);
            cur_node_id = find_node(cur_node_id).second->pre_node_id;
        }
        reverse(shortest_path.begin(),shortest_path.end());
        return end_node.second->shortest_weight;
}



