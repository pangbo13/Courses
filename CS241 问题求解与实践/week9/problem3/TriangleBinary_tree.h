#pragma once
#include "Binary_tree.h"

class TriangleBinary_tree : public Binary_tree {
  private:
    void draw_nodes(Point c) const;

  public:
    TriangleBinary_tree(int levels = 0) : Binary_tree(levels) {}

    ~ TriangleBinary_tree() { }
};

