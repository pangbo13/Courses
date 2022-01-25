# include "BarChart.h"

string BarChart :: double_2_str(double x){
	string res = to_string((int)(x*10));
	res.insert(res.length() - 1, 1, '.');
	return res;
}

void BarChart :: load_data(){
	char junk[20];
	int y, m, d;
	double tempture;
	vector <int> count_days;
	vector <double> newYork_tempSum, austin_tempSum;
	newYork_tempSum.resize(13);
	austin_tempSum.resize(13);
	count_days.resize(13);

	auto fp_ny = fopen("NewYork.csv", "r");
	for (int i = 1; i <= 12; ++ i) newYork_avg[i] = 0, count_days[i] = 0;
	fscanf(fp_ny, "%s,%s,\n", junk, junk);
	while(fscanf(fp_ny, "%d/%d/%d,%lf ,", &y, &m, &d, &tempture)!=EOF) {
		newYork_tempSum[m] += tempture;
		count_days[m] ++;
	}
	fclose(fp_ny);
	for (int i = 1; i <= 12; ++ i) 
		if(count_days[i]!=0) 
			newYork_avg[i] =newYork_tempSum[i] / count_days[i];

	auto fp_au = fopen("Austin.csv", "r");
	for (int i = 1; i <= 12; ++ i) austin_avg[i] = 0, count_days[i] = 0;
	fscanf(fp_au, "%s,%s,\n", junk, junk);
	while(fscanf(fp_au, "%d/%d/%d,%lf ,", &y, &m, &d, &tempture)!=EOF){
		austin_tempSum[m] += tempture;
		count_days[m] ++;
	}
	fclose(fp_au);
	for (int i = 1; i <= 12; ++ i) 
		if(count_days[i]!=0) 
			austin_avg[i] = austin_tempSum[i] / count_days[i];
}


void BarChart :: draw_lines() const {
	//表头
	Text title(Point(300, 60), "Temperature in New York and Austin(2016)");
	title.set_color(Color :: black);
	title.set_font(Font(FL_TIMES_BOLD));
	title.set_font_size(20);
	title.draw();

	//X轴
	Axis AX(Axis :: x, Point(100, 500), 840, 12, "Month");
	AX.set_color(Color :: black);
	AX.label.move(650,20);
	AX.draw();

	//Y轴
	Axis AY(Axis :: y, Point(100, 500), 400, 8, "Temperature");
	AY.set_color(Color :: black);
	AY.draw();

	//温度坐标数字
	for (int i = 0, y = 500; i <= 40; i += 5, y -= Ysize_per_deg * 5) {
		Text t(Point(75, y + 5), to_string(i));
		t.draw();
	}

	int cur_x = 100, cur_y = 500;
	for (int i = 1; i <= 12; ++ i) {
		cur_x += 10;

		int austin_length = austin_avg[i] * Ysize_per_deg;
		Graph_lib :: Rectangle au_block(Point(cur_x, cur_y - austin_length), 25, austin_length);
		au_block.set_color(Color::dark_green);
		au_block.set_fill_color(austin_color);
		au_block.draw();


		Text t_austin(Point(cur_x - 3, cur_y - austin_length - 8), double_2_str(austin_avg[i]));
		t_austin.set_color(austin_color);
		t_austin.draw();

		cur_x += 30;

		int newyork_length = newYork_avg[i] * 10;
		Graph_lib :: Rectangle ny_block(Point(cur_x, cur_y- newyork_length), 25, newyork_length);
		ny_block.set_color(Color::dark_blue);
		ny_block.set_fill_color(newYork_color);
		ny_block.draw();

		Text t_newyork(Point(cur_x, cur_y - newyork_length - 8), double_2_str(newYork_avg[i]));
		t_newyork.set_color(newYork_color);
		t_newyork.draw();

		Text t_axis(Point(cur_x - 10, cur_y + 20), to_string(i));
		t_axis.draw();

		cur_x += 30;
	}

	Graph_lib :: Rectangle rblank(Point(750, 80), 200, 100);
	rblank.set_color(Color :: red);
	rblank.set_fill_color(Color :: white);
	rblank.draw();

	Graph_lib :: Rectangle raustin(Point(770, 100), 80, 20);
	raustin.set_color(austin_color);
	raustin.set_fill_color(austin_color);
	raustin.draw();

	Graph_lib :: Rectangle rnewyork(Point(770, 140), 80, 20);
	rnewyork.set_color(newYork_color);
	rnewyork.set_fill_color(newYork_color);
	rnewyork.draw();

	Text taustin(Point(860, 115), "Austin");
	taustin.set_color(Color :: black);
	taustin.set_font(Font(FL_TIMES_BOLD_ITALIC));
	taustin.draw();

	Text tnewyork(Point(860, 155), "New York");
	tnewyork.set_color(Color :: black);
	tnewyork.set_font(Font(FL_TIMES_BOLD_ITALIC));
	tnewyork.draw();
}


