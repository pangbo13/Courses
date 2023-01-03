#pragma once
#include "std_lib_facilities.h"
namespace GraphGenterator_NS{
class GraphGenterator{
    static int randint(int a,int b);
    static float randfloat(float a,float b);
    static bool randbool(float probability);
    string file_name;
    int max_node_id;
    float max_weight;
    void write_node(int num,FILE* f);
     public:
    GraphGenterator(string path,int MaxNodeID = 200,float MaxWeight = 200):
                                    file_name(path),max_node_id(MaxNodeID),max_weight(MaxWeight){};
    void create(int num);
    void append(int num);
};

};