//** coding: gbk

#include "GraphSplit.h"
#ifdef _WIN32
    #include <windows.h>
#endif
#define CREATE_FOLDER
using namespace GraphSplit_NS;
int main(int argc, char* argv[]){
    int subGraphMaxNodeNum;
    string arg_file_name;
    if(argc>1){
        if(argc==3){
            arg_file_name = argv[1];
            sscanf(argv[2],"%d",&subGraphMaxNodeNum);
            if(to_string(subGraphMaxNodeNum)!=argv[2]){
                printf("argument 2 should be an integer.");
                return -1;
            }
        }else{
            printf("Usage:\n\t %s GraphFilePath SubGraphMaxNodeNum",argv[0]);
            return -2;
        }
    }else{
        printf("Please input the path of the graph file:");
        char flush[256];
        scanf("%s",flush);
        arg_file_name = flush;
        printf("Please input the max number of nodes in each subgraph :");
        scanf("%d",&subGraphMaxNodeNum);
    }

    GraphSplit gs(arg_file_name);
    double res = gs.split(subGraphMaxNodeNum);
    printf("%.4lf",res);
    #ifdef CREATE_FOLDER
    #ifdef _WIN32
        CreateDirectory("data",NULL);
    #else
        system("mkdir -p \"data\"");
    #endif
    #endif
    gs.write("./data/");
    
}