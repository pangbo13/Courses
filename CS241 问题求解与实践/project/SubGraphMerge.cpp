//** coding: gbk

#include "SubGraphMerge.h"
using namespace SubGraphMerge_NS;
void subGraphMerge::read_catalogue(string path){
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
void subGraphMerge::read_SG(SubGraphInfo& sgi){
    ifstream fin;
    fin.open(sgi.file_path.c_str(),ios::in);
    if(!fin) throw runtime_error(string("FILE ERROR:Cannot load the file:")+sgi.file_path);
    string input_line;
    while(getline(fin,input_line)){
        int args_num,num1,num2,num3;
        float num4;
        if(input_line.find('@')!=string::npos){
            args_num = sscanf(input_line.c_str(),"<%d %d@%d %f>",&num1,&num2,&num3,&num4);
            if(Graph.find(num1) == Graph.end()){
                Graph[num1] = node(num1,sgi.subGraph_id);
            }
            if(Graph.find(num2) == Graph.end()){
                Graph[num2] = node(num2,num3);
            }
            Graph[num1].edges.push_back(edge(num1,num2,num4));
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
                Graph[num1].edges.push_back(edge(num1,num2,num4));
            }
        }
    }
}
void subGraphMerge::read(string path){
    read_catalogue(path);
    for(auto& sgi:SGInfo_List){
        read_SG(sgi);
    }
}

