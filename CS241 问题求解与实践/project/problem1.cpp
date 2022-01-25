//** coding: gbk
#include "GraphGenerator.h"
using namespace GraphGenterator_NS;

int main(int argc, char* argv[]){
    int max_node_id = 200;
    float max_weight = 200;
    srand(int(time(0)));
    int op;         //操作类型和行数，1-新建 2-追加
    int num;
    string arg_file_name;
    if(argc<4){
        printf("number of arguments error"
            "\nUsage:\n\t"
            "%s create|append lines PATH [MaxNodeID MaxWeight]\n",argv[0]);
        return -1;
    }
    string arg_op(argv[1]);
    if(arg_op=="create") op=1;
    else if(arg_op=="append") op=2;
    else{
        printf("argument 1 should be \"create\" or \"append\"");
        return -1;
    }
    sscanf(argv[2],"%d",&num);
    if(to_string(num)!=argv[2]){
        printf("argument 2 should be an integer.");
        return -1;
    }
    arg_file_name = argv[3];
    if(argc==6){
        sscanf(argv[4],"%d",&max_node_id);
        sscanf(argv[5],"%f",&max_weight);
    }
    GraphGenterator gg(arg_file_name,max_node_id,max_weight);
    try{
        if(op==1) gg.create(num);
        else if(op==2) gg.append(num);
    }catch(const runtime_error& err){
        cerr<<err.what();
        return -2;
    }
}