#pragma once
#include "std_lib_facilities.h"
#include "Graph.h"

using namespace Graph_lib;
using namespace std;

class Binary_tree : public Shape {
  protected:
    int levels;
    vector <Point> nodes;

    virtual void draw_nodes(Point c) const;
    void draw_lines() const;

  public:
    Binary_tree(int levels = 0);
    ~Binary_tree() = default;
};


