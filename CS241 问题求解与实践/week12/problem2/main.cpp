#include "std_lib_facilities.h"
#include<queue>
using namespace std;

struct task{
    int pid;
    int priority;
    int start_time;
    int finish_time;
    queue<int> time_split;
    task(string& input){
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
    bool operator<(task& oth){
        if(priority>oth.priority) return true;
        else if(start_time<oth.priority) return true;
        else return false; 
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
    while(getline(cin,str)){
        task t(str);
        task_queue.push(t);
    }
    int ctime = 0,next_time = 0;
    int atime1 = 0,atime2 = 0;
    int core1_task_id = -1,core2_task_id = -1;
    while(true){
        ctime = next_time;
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
            sort(task_wait.begin(),task_wait.end());
            bool has_task = false;
            }
            if(atime1>ctime&&atime2>ctime){
                ctime = min(atime1,atime2);
            }else{
                if(ctime>=atime1){
                    
                }
            }
            ctime += task_wait[ctask_id].time_split.front();
            task_wait[ctask_id].time_split.pop();
            if(task_wait[ctask_id].time_split.empty()) finish.push_back(task_wait[ctask_id].pid);
            for(int i = 0;i<task_wait.size();i++){
                if(i==ctask_id) task_wait[i].priority--;
                else task_wait[i].priority++;
            }

        }
    }
    for(auto i:finish){
        cout<<'P'<<i<<' ';
    }
}