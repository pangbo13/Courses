#include "Question_1.h"
int solver1()
{
    vector<int> weight;
    int w,n,input;
    scanf("%d%d",&w,&n);
    weight.resize(n);
    for(int i = 0;i<n;i++){
        scanf("%d",&input);
        weight[i] = input;
    }
    sort(weight.begin(),weight.end());
    if(weight[0]<=0) {
        printf("error");
        return -1;
    }
    if(weight[n-1]>w) {
        printf("out");
        return -1;
    }
    int boat = 0;
    int i = 0,j = n-1;
    while(i<j){
        if(weight[i]+weight[j] > w){
            boat++;
            j--;
        }else
        {
            boat++;
            i++;
            j--;
        }
    }
    if(i==j) boat++;
    printf("%d",boat);
    return 0;
}