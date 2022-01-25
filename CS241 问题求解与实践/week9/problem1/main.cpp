#include "Simple_window.h"
#include "Graph.h"
#include "hyperelliptic.h"
#include "std_lib_facilities.h"
#include <iostream>

#define WINDOW_WIDTH 600
#define WINDOW_HEIGT 400

int main() {
    double a, b, m, n;
    int N;
    cout << "Please input a b m n N (N is a non-negative even integer): ";
    cin >> a >> b >> m >> n >> N;

    Hyperelliptic hyp(a, b, m, n, N , Point(WINDOW_WIDTH/2,WINDOW_HEIGT/2));

    hyp.set_color(0x99ffee);//乱选了一个颜色，内置的太难看了

    Simple_window win(Point(200,200), WINDOW_WIDTH, WINDOW_HEIGT, "Hyperelliptic");

    win.attach (hyp);

    win.wait_for_button();
    return 0;
}
