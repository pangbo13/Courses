#include<iostream>
#include<string>
#include<vector>
#include<algorithm>

using namespace std;

bool check_chr(char c){
    if((c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9')||c=='_'||c=='-') return true;
    else return false;
}

void get_input(vector<string>& list,string& input,bool to_lower=true){
    int j=0;
    while(input[j]){
        if(check_chr(input[j])){
            string word;
            while(check_chr(input[j])){
                char chr = input[j];
                if(chr=='_'||chr=='-'){
                    if(!check_chr(input[j+1])){
                        j++;
                        break;
                    }
                }
                else if(chr>='A'&&chr<='Z'){ 
                    if(to_lower) chr-=('A'-'a');
                }
                word += chr;
                j++;
            }
            list.push_back(word);
        }else{
            while(input[j]&&!check_chr(input[j])) j++;
        }
    }
}

int main(){
    vector<string> list,count_list;
    string input;
    getline(cin,input);
    get_input(list,input);
    getline(cin,input);
    get_input(count_list,input,false);
    for(auto count_word:count_list){
        int count = 0;
        string lower_count_word;
        lower_count_word.resize(count_word.size());
        transform(count_word.begin(), count_word.end(), lower_count_word.begin(), ::tolower);
        for(auto word:list){
            if(word==lower_count_word) count++;
        }
        // cout<<count<<' ';
        printf("(%s,%d) ",count_word.c_str(),count);
    }
    
}