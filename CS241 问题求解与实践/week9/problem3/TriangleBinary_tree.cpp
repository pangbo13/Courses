# include "TriangleBinary_tree.h"

void TriangleBinary_tree :: draw_nodes(Point c) const {
    fl_line(c.x, c.y - 8 , c.x - 8, c.y + 8);
    fl_line(c.x - 8, c.y + 8 , c.x + 8, c.y + 8);
    fl_line(c.x + 8, c.y + 8, c.x, c.y - 8 );
}

