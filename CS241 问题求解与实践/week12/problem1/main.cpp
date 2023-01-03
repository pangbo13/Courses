#include "std_lib_facilities.h"
#include<queue>
using namespace std;

struct task{
    int pid;
    int priority;
    int start_time;
    bool started;
    queue<int> time_split;
    task(string& input){
        started = false;
        int i = 0;
        bool get_starttime = false;
        while(input[i]){
            if(input[i]=='['||input[i]==']'){
                i++;
                continue;
            }else if(input[i]=='P'){
                i++;
                int num = 0;
                while(isdigit(input[i])){
                    num = num*10 + (input[i]-'0');
                    i++;
                }
                pid = num;
                while(input[i]==' ') i++;
                num = 0;
                while(isdigit(input[i])){
                    num = num*10 + (input[i]-'0');
                    i++;
                }
                priority = num;
                while(input[i]==' ') i++;
                num = 0;
                while(isdigit(input[i])){
                    num = num*10 + (input[i]-'0');
                    i++;
                }
                start_time = num;
            }else if(input[i]==' '){
                while(input[i]==' ') i++;
            }else if(isdigit(input[i])){
                int num = 0;
                while(input[i]&&isdigit(input[i])){
                    num = num*10 + (input[i]-'0');
                    i++;
                }
                time_split.push(num);
            }
             
        }
    }
};
struct sort_by_starttime{
    bool operator()(task& a,task& b){
        return a.start_time>b.start_time;
    }
};

struct sort_by_priority{
    bool operator()(task& a,task& b){
        return a.priority<a.priority;
    }
};

priority_queue<task,vector<task>,sort_by_starttime> task_queue;
vector<task> task_wait;
vector<int> finish;
int main(){
    string str;
    int ltask_id = -1;          
    while(getline(cin,str)){
        task t(str);
        task_queue.push(t);
    }
    int ctime = 0,next_time = 0;
    while(true){
        while((!task_queue.empty())&&task_queue.top().start_time<=ctime){
            task_wait.push_back(task_queue.top());
            task_queue.pop();
        }
        if(task_wait.empty()){
           if(!task_queue.empty()){
                    ctime = task_queue.top().start_time;
                    continue;
                }else break;
        }else{
            int max_priority = -100000;
            int ctask_id = -1;
            for(int i = 0;i<task_wait.size();i++){
                if((!task_wait[i].time_split.empty())&&(task_wait[i].priority+task_wait[i].started)>=max_priority){
                    if((task_wait[i].priority+task_wait[i].started)==max_priority){
                        if(ctask_id>=0){
                            if(task_wait[i].start_time>task_wait[ctask_id].start_time) ctask_id = i;
                        }else ctask_id = i;
                    }else{
                        ctask_id = i;
                        max_priority = (task_wait[i].priority+task_wait[i].started);
                    }
                }
            }
            if(ctask_id == -1) {
                if(!task_queue.empty()){
                    ctime = task_queue.top().start_time;
                    continue;
                }else break;
            }
            if(ctask_id!=ltask_id){
                // if(ltask_id==-1) ltask_id = ctask_id;
                // if(task_wait[ctask_id].priority-task_wait[ltask_id].priority>=2) ltask_id = ctask_id;
                ltask_id = ctask_id;
            }
            ctime += task_wait[ltask_id].time_split.front();
            task_wait[ltask_id].time_split.pop();
            task_wait[ltask_id].started = true;
            while((!task_queue.empty())&&task_queue.top().start_time<ctime){
                task_wait.push_back(task_queue.top());
                task_queue.pop();
            }   
            if(task_wait[ltask_id].time_split.empty()) {
                finish.push_back(task_wait[ltask_id].pid);
                ltask_id = -1;
                }
            for(int i = 0;i<task_wait.size();i++){
                if(i==ltask_id) {
                    task_wait[i].priority--;
                    if(task_wait[i].priority<1) task_wait[i].priority = 1;
                }
                else {
                    task_wait[i].priority++;
                    if(task_wait[i].priority>10) task_wait[i].priority = 10;
                    }
            }

        }
    }
    for(auto i:finish){
        cout<<'P'<<i<<' ';
    }
}