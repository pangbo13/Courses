#include "Binary_tree.h"
#define NODE_INTERVAL 15
Binary_tree :: Binary_tree(int levels) : levels(levels) {
    nodes.resize(1<<levels);
    int nowlevel = 1;
    int levels_node_num = 1;
    int node_id = 1;
    for(;nowlevel<=levels;++nowlevel){
        for(int i = 0;i < (1<<(nowlevel-1));i++){
            nodes[node_id] = Point(NODE_INTERVAL*((1<<(levels-nowlevel))*(1+2*i)),30*nowlevel);
            add(nodes[node_id]);
            node_id++;
        }
    }
}

void Binary_tree :: draw_lines() const {
    for (int i = 1; i < nodes.size()/2; i ++){
        fl_line(nodes[i].x, nodes[i].y, nodes[2*i].x, nodes[2*i].y);
        fl_line(nodes[i].x, nodes[i].y, nodes[2*i+1].x, nodes[2*i+1].y);
    }
    for(int i = 1; i < nodes.size(); i ++) draw_nodes(nodes[i]);
}
void Binary_tree :: draw_nodes(Point c) const {
    fl_arc(c.x - 8, c.y - 8, 16, 16, 0, 360);
}
