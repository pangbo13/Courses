//** coding: gbk

#include "GraphGenerator.h"
using namespace GraphGenterator_NS;

int GraphGenterator::randint(int a,int b){
    return rand()%(b-a+1)+a;
}
float GraphGenterator::randfloat(float a,float b){
    return rand()/double(RAND_MAX)*(b-a);
}
bool GraphGenterator::randbool(float probability){
    return randfloat(0,1)<probability;
}
void GraphGenterator::write_node(int num,FILE* f){
    for(int i=0;i<num;i++){
        if(randbool(0.8))
            fprintf(f,"<%d %d %f>\n",randint(1,max_node_id),randint(1,max_node_id),randfloat(1,max_weight));
        else fprintf(f,"<%d>\n",randint(1,max_node_id));
    }
}
void GraphGenterator::create(int num){
    auto f = fopen(file_name.c_str(),"w");
    if(!f) throw runtime_error(string("FILE ERROR:Cannot create the file: ")+file_name);
    write_node(num,f);
    fclose(f);
}
void GraphGenterator::append(int num){
    auto f = fopen(file_name.c_str(),"a");
    if(!f) throw runtime_error(string("FILE ERROR:Cannot open the file: ")+file_name);
    write_node(num,f);
    fclose(f);
}
