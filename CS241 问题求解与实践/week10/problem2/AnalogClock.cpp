#include "AnalogClock.h"

void AnalogClock :: draw_lines() const {}
void AnalogClock :: update() {
    static int last_update = 0;
    time_t timer;
    time(&timer);
    if(last_update==timer) return;
    struct tm *cur_time = localtime(&timer);
    int year = cur_time -> tm_year + 1900;
    int month = cur_time -> tm_mon + 1;
    int day = cur_time -> tm_mday;
    int hour = cur_time -> tm_hour;
    int minute = cur_time -> tm_min;
    int second = cur_time -> tm_sec;
    last_update = second;

    //覆盖原图像
    Graph_lib::Rectangle background(Point(0, 0),600,500);
    background.set_fill_color(Color::white);
    background.draw();

    string time_str;
    if(hour < 10) time_str += "0";
    time_str += to_string(hour) + ":";
    if(minute < 10) time_str += "0";
    time_str += to_string(minute) + ":";
    if(second < 10) time_str += "0";
    time_str += to_string(second);
    Text time_text(Point(center.x-45, center.y+130), time_str);
    time_text.set_font(Font(FL_SYMBOL));
    time_text.set_font_size(25);
    time_text.draw();

    string date_str;
    date_str += to_string(year) + "/";
    if(month < 10) date_str += "0";
    date_str += to_string(month) + "/";
    date_str += to_string(day);
    Text date_text(Point(center.x-60, center.y+100), date_str);
    date_text.set_font(Font(FL_SYMBOL));
    date_text.set_font_size(25);
    date_text.draw();

    Circle clock_circle(Point(center.x, center.y), 200);
    clock_circle.set_style(Line_style(Line_style::solid,3));
    clock_circle.draw();

    for (int deg = 0; deg < 360; deg +=30) {
        double angle = deg / 180.0 * PI;//角度转弧度
        //画刻度
        Line clock_line(Point(center.x + 190 * cos(angle), center.y + 190 * sin(angle)), Point(center.x + 200 * cos(angle), center.y + 200 * sin(angle)));
        clock_line.set_color(Color :: black);
        clock_line.set_style(Line_style(Line_style::solid,3));
        clock_line.draw();

        //画数字
        int num = (deg / 30+3 ) % 12;
        if(num == 0) num = 12;
        Text num_text(Point(center.x + 180 * cos(angle) - 6, center.y + 180 * sin(angle) + 6), to_string(num));
        num_text.set_color( Color::black);
        num_text.set_font(Font(Font(FL_TIMES_BOLD)));
        num_text.set_font_size(20);
        num_text.draw();
    }

    Circle c_dot(Point(center.x, center.y), 2);
    c_dot.set_style( Line_style( Line_style :: solid, 5));
    c_dot.draw();

    //计算指针角度
    double hour_angle = (hour % 12) / 6.0 * PI, minute_angle = (minute % 60) / 30.0 * PI, second_angle = (second % 60) / 30.0 * PI;
    minute_angle += second_angle / 60;
    hour_angle += minute_angle / 12;

    Line l_hour(Point(center.x, center.y), 
            Point(center.x + hour_length * sin(hour_angle), 
            center.y - hour_length * cos(hour_angle)));
    l_hour.set_color(fl_rgb_color(128,128,255));
    l_hour.set_style(Line_style(Line_style::solid, 5));
    l_hour.draw();

    Line l_minute(Point(center.x, center.y),
            Point(center.x + minute_length * sin(minute_angle),
            center.y - minute_length * cos(minute_angle)));
    l_minute.set_color(fl_rgb_color(255,0,0));
    l_minute.set_style(Line_style(Line_style::solid,3));
    l_minute.draw();

    Line l_second(Point(center.x, center.y), 
            Point(center.x + second_length * sin(second_angle), 
            center.y - second_length * cos(second_angle)));
    l_second.set_color(Color::black);
    l_second.set_style(Line_style(Line_style::solid,1));
    l_second.draw();
}
