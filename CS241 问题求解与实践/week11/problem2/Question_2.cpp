#include "Question_2.h"

subsequence::subsequence():error_flag(false),count(0){}
void subsequence::get_input(){
    scanf("%d",&n);
    data.resize(n);
    while(scanf("%d",&input)==1){ 
        count ++;
        if(input > 1000||input < -1000) error_flag = true;
        if(count<=n) data[count-1] = input; 
    }
}
void subsequence::calc(){
    if(count!=n||n>100000||error_flag){
        printf("error");
        return;
    }
    int max = -10000,current = 0,p_max_begin = 1,max_begin = -1,max_end = -1;
    for(int i = 0;i < n;i++){
        current += data[i];
        if(current > max){
            max = current;
            max_begin = p_max_begin;
            max_end = i+1;
        }
        if(current < 0){
            current = 0;
            p_max_begin = i + 2;
        }
    }
    printf("%d %d %d",max,max_begin,max_end);
}