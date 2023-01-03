//** coding: gbk

#include "GraphSplit.h"
using namespace GraphSplit_NS;
void GraphSplit::splitor::update_cost(){
    for(auto& e:Graph[current_node_id].edges){
        if(e.end_node_id==e.start_node_id) continue;//跳过自环
        auto& endnode = Graph[e.end_node_id];
        if(endnode.belongs){ 
            if(endnode.belongs== sg->subGraph_id){
                sg->weight_sum+=e.weight;}//如果另一个节点在同一个子图内，就把边权值加入子图的边权值和
            continue;//另一个节点已经分配子图，但是不是同一个子图，直接忽略
            }
        //另一个节点还未分配子图
        endnode.weight_sum -= e.weight;//从全局图中减去这条边的权值
        auto cnode_p = cnodes.find(e.end_node_id);
        if(cnode_p == cnodes.end()){ //待选列表中没有
            cnodes.insert({e.end_node_id,candidate_node(e.end_node_id)});//加入待选列表
            cnode_p = cnodes.find(e.end_node_id);
        }
        cnode_p->second.subsplit_cost += e.weight;//更新待选节点的子图切割代价
    }
    //在反图中重复一遍操作
    for(auto& e:GraphR[current_node_id].edges){
        if(e.end_node_id==e.start_node_id) continue;
        auto& endnode = GraphR[e.end_node_id];//边的结束节点的引用
        if(endnode.belongs){ 
            if(endnode.belongs== sg->subGraph_id){
                sg->weight_sum+=e.weight;}//如果结束节点在子图内，就把边权值加入子图和
            continue;//结束节点已经分配子图，但是不是同一个子图，直接忽略
            }
        //另一个节点还未分配子图
        endnode.weight_sum -= e.weight;
        auto cnode_p = cnodes.find(e.end_node_id);
        if(cnode_p == cnodes.end()){ //待选列表中没有则添加到列表
            cnodes.insert({e.end_node_id,candidate_node(e.end_node_id)});
            cnode_p = cnodes.find(e.end_node_id);
        }
        cnode_p->second.subsplit_cost += e.weight;//更新待选节点的子图切割代价
    }
}
int GraphSplit::splitor::find_first_node(){
    int max_weight_id = -1;//找不到节点则返回-1
    double max_weight = -1e20f;
    for(auto& pair_p:Graph){
        auto& node_p = pair_p.second;//节点对象的引用
        int node_id = pair_p.first;
        if(node_p.belongs) continue;
        double weight = node_p.weight_sum+GraphR[node_id].weight_sum;
        if(max_weight<weight){
            max_weight = weight;
            max_weight_id = node_id;
        }
    }
    current_node_id = max_weight_id;
    return current_node_id;
}
int GraphSplit::splitor::find_node(){
    int max_weight_id = -1;//找不到节点则返回-1
    double max_weight = -1e20f;
    for(auto& pair_p:cnodes){
        auto& node_p = pair_p.second;
        double weight;
        if((sg->node_count)>DEMARCATION)//特别处理最后几个节点
            //计算每个节点的权重：与子图相连的边权值-其余边权值
            weight = node_p.subsplit_cost - (Graph[node_p.node_id].weight_sum+GraphR[node_p.node_id].weight_sum);
        else
            weight = node_p.subsplit_cost;
        if(max_weight<weight){
            max_weight = weight;
            max_weight_id = node_p.node_id;
        }
    }
    current_node_id = max_weight_id;
    return current_node_id;
}
void GraphSplit::splitor::add_node(int node_id){
    sg->nodes.insert(node_id);
    cnodes.erase(node_id);
    Graph[node_id].belongs = sg->subGraph_id;
    GraphR[node_id].belongs = sg->subGraph_id;
    sg->node_count++;
}

void GraphSplit::read_file(string& path){
    ifstream fin;
    fin.open(path.c_str(),ios::in);
    if(!fin){
        throw runtime_error(string("FILE ERROR: Cannot read file: ")+path);
    }
    string input_line;
    while(getline(fin,input_line)){
        int args_num,num1,num2;
        double num3;
        args_num = sscanf(input_line.c_str(),"<%d %d %lf>",&num1,&num2,&num3);
        if(args_num == 1){
            auto node_p = Graph.find(num1);
            if(node_p == Graph.end()){
                Graph[num1] = node(num1);
            }
            auto node_pR = GraphR.find(num1);
            if(node_pR == GraphR.end()){
                GraphR[num1] = node(num1);
            }
        }else{
            if(Graph.find(num1) == Graph.end()){
                Graph[num1] = node(num1);
            }
            if(Graph.find(num2) == Graph.end()){
                Graph[num2] = node(num2);
            }
            Graph[num1].edges.push_back(edge(num1,num2,num3));
            if(GraphR.find(num1) == GraphR.end()){
                GraphR[num1] = node(num1);
            }
            if(GraphR.find(num2) == GraphR.end()){
                GraphR[num2] = node(num2);
            }
            GraphR[num2].edges.push_back(edge(num2,num1,num3));

            if(num2!=num1) edge_weight_sum += num3;
        }
    }
}

void GraphSplit::init(){
    subgraph_weight_sum = 0;
    //初始化,计算每个节点的边权值和
    for(auto& n:Graph){
        auto& node_p = n.second;
        node_p.belongs = 0;
        node_p.weight_sum = 0;
        for(auto e:node_p.edges){
            if(e.end_node_id!=e.start_node_id) node_p.weight_sum += e.weight;
        }
    }
    for(auto& n:GraphR){
        auto& node_p = n.second;
        node_p.belongs = 0;
        node_p.weight_sum = 0;
        for(auto e:node_p.edges){
            if(e.end_node_id!=e.start_node_id) node_p.weight_sum += e.weight;
        }
    }
}
void GraphSplit::clear_cache(){
    for(auto p:sg_list)delete p;
    sg_list.clear();
}
void GraphSplit::clear_saved(){
    for(auto p:saved_sg_list)delete p;
    saved_sg_list.clear();
}
GraphSplit::GraphSplit(string path){
    edge_weight_sum = 0;
    subgraph_weight_sum = 0;
    read_file(path);
}
GraphSplit::~GraphSplit(){
    clear_cache();
    clear_saved();
}
double GraphSplit::split(int maxN,int demarcation){
    clear_cache();
    init();
    int cnode_id;
    int subGraph_id = 1;
    while(true){
        SubGraph* sg = new SubGraph(subGraph_id);
        splitor sp(sg,maxN,demarcation,Graph,GraphR);
        cnode_id = sp.find_first_node();//找到第一个节点
        if(cnode_id==-1) {//没有可选的第一个节点，结束
            delete sg;
            break;
        }else{
            sg_list.push_back(sg);
        }
        sp.add_node(cnode_id);//把节点加入子图
        sp.update_cost();//更新图权值
        while((sg->node_count<maxN)&& ((cnode_id = sp.find_node())!=-1)){
            sp.add_node(cnode_id);
            sp.update_cost();
        }
        subGraph_id ++;
        subgraph_weight_sum += sg->weight_sum;
    }
    return edge_weight_sum-subgraph_weight_sum;//返回子图切割的代价
}
double GraphSplit::split(int maxN){
    double min_cost = 1e20;
    float step = maxN<100?1:(maxN/100.0);//设置尝试步长
    for(float demarcation=0;demarcation<=maxN;){
        double cost = split(maxN,demarcation);
        if(cost<min_cost){
            min_cost = cost;
            clear_saved();//清空保存的分割方法
            saved_sg_list = sg_list;
            sg_list.clear();//清空当前临时的子图列表，避免子图对象被delete
            if(fabs(min_cost)<1e-6){
                min_cost = 0;
                break;//发现代价为0的方法后，直接结束
            }
        }
        demarcation+=step;
    }
    return min_cost;
}

void GraphSplit::load_saved_before_write(){
    for(auto sg:saved_sg_list){
        for(auto node_id:sg->nodes){
            Graph[node_id].belongs = sg->subGraph_id;
        }
    }
}


void GraphSplit::write(string path){
    load_saved_before_write();
    for(auto sg:saved_sg_list){
        string file_name = path +"/SG-"+ to_string(sg->subGraph_id) + ".txt";
        FILE* f = fopen(file_name.c_str(),"w");
        if(!f) throw runtime_error(string("FILE ERROR:Cannot create the file:")+file_name);
        for(auto n_id:sg->nodes){
            auto& start_node = Graph[n_id];
            if(start_node.edges.empty()){
                fprintf(f,"<%d>\n",start_node.node_id);
            }else{
                for(auto e:start_node.edges){
                    auto& end_node = Graph[e.end_node_id];
                    if(end_node.belongs==sg->subGraph_id){
                        fprintf(f,"<%d %d %.4lf>\n",e.start_node_id,e.end_node_id,e.weight);
                    }else{
                        fprintf(f,"<%d %d@%d %.4lf>\n",e.start_node_id,e.end_node_id,end_node.belongs,e.weight);
                    }
                }
            }
        }
        fclose(f);
    }
    FILE* f = fopen((path+"/catalogue.txt").c_str(),"w");
    if(!f) throw runtime_error(string("FILE ERROR:Cannot create the file: ")+path+"/catalogue.txt");
    for(auto sg:saved_sg_list){
        fprintf(f,"%d %s %d %f\n",sg->subGraph_id,("SG-"+ to_string(sg->subGraph_id) + ".txt").c_str(),
            sg->node_count,sg->weight_sum);
    }
    #ifdef FILE_DEBUG_INFO
        fprintf(f,"#total weight=%lf\n",edge_weight_sum);
        fprintf(f,"#subgraph total weight=%lf\n",subgraph_weight_sum);
    #endif
    fclose(f);
}
