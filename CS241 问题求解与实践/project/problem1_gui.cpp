//coding:utf-8

//参考：fltk源码中测试样例文件Fl_Native_File_Chooser.cxx


#include <stdio.h>
#include <string>
#include <string.h>		/* strstr() */
#include <FL/Fl.H>
#include <FL/fl_ask.H>		/* fl_beep() */
#include <FL/Fl_Window.H>
#include <FL/Fl_Button.H>
#include <FL/Fl_Input.H>
#include <FL/Fl_Multiline_Input.H>
#include <FL/Fl_Box.H>
#include <FL/Fl_Native_File_Chooser.H>
#include <FL/Fl_Help_View.H>

#include <FL/Fl_Double_Window.H>
#include <FL/Fl_Button.H>
#include <FL/Fl_Check_Button.H>
#include <FL/Fl_Return_Button.H>
#include <FL/Fl_Group.H>
#include <FL/Fl_Text_Editor.H>
#include <FL/Fl_Radio_Round_Button.H>

#include "GraphGenerator.h"
using namespace GraphGenterator_NS;

// GLOBALS
Fl_Input *G_filename = NULL;
Fl_Input *G_linenum = NULL;
Fl_Radio_Round_Button* pRndButton,*pRndButton2;
Fl_Button *B_generate = NULL;

void PickFile_CB(Fl_Widget*, void*) {
    // Create native chooser
    Fl_Native_File_Chooser native;
    native.title("选择文件");
    native.type(Fl_Native_File_Chooser::BROWSE_SAVE_FILE);
    native.filter("Text\t*.txt\n");
    native.preset_file(G_filename->value());
    // Show native chooser
    switch ( native.show() ) {
        case -1: fprintf(stderr, "ERROR: %s\n", native.errmsg()); break;	// ERROR
        case  1: fprintf(stderr, "*** CANCEL\n"); fl_beep(); break;		// CANCEL
        default: 								// PICKED FILE
            if ( native.filename() ) {
                fprintf(stderr,"%s",native.filter());
                G_filename->value(native.filename());
            } else {
    G_filename->value("NULL");
            }
            break;
    }
}

void Generate_CB(Fl_Widget*, void*){
    std::string path = G_filename->value();
    int lines_num;
    sscanf(G_linenum->value(),"%d",&lines_num);
    int op = pRndButton ->value();
    printf("%d %d",lines_num,op);
    int max_node_id = 100;
    int max_weight = 1000;
    GraphGenterator gg(path,max_node_id,max_weight);
    
    try{
        if(op==1) gg.create(lines_num);
        else if(op==0) gg.append(lines_num);
        fl_message("操作完成！");
    }catch(runtime_error err){
        fl_alert(err.what());
    }
}

int main(int argc, char **argv) {

#if !defined(WIN32) && !defined(__APPLE__)
    Fl_File_Icon::load_system_icons();
#endif

    int argn = 1;
#ifdef __APPLE__
    // OS X may add the process number as the first argument - ignore
    if (argc>argn && strncmp(argv[1], "-psn_", 5)==0)
        argn++;
#endif
    
    Fl_Window *win = new Fl_Window(600, 200, "图生成器");
    win->size_range(win->w(), win->h(), 0, 0);
    win->begin();
    {
        int x = 80, y = 10;
        G_filename = new Fl_Input(x, y, win->w()-180-10, 25, "文件名");
        G_filename->value(argc <= argn ? "." : argv[argn]);

        Fl_Button *but = new Fl_Button(win->w()-180+x, y, 80, 25, "选择文件");
        but->callback(PickFile_CB);

        y += G_filename->h() + 10;
        G_linenum = new Fl_Input(x, y, 100, 25, "行数");
        G_linenum->value("100");

        Fl_Group* pGroup = new Fl_Group(50, 50, 400, 150);					/* 2. 创建一个分组 */
        pRndButton = new Fl_Radio_Round_Button(150, 80, 150, 30, "新建");
        pRndButton2 = new Fl_Radio_Round_Button(230, 80, 150, 30, "追加");
        pGroup->end();										
        
        B_generate = new Fl_Button(160,120,100,30,"生成");
        B_generate->callback(Generate_CB);

    }
    win->end();
    win->show(argc, argv);
    return(Fl::run());
}
