#include "std_lib_facilities.h"
#include <set>

const set<string> key_words = {"alignas","alignof","and","and_eq","asm",
    "atomic_cancel","atomic_commit","atomic_noexcept","auto","bitand",
    "bitor","bool","break","case","catch","char","char8_t","char16_t",
    "char32_t","class","compl","concept","const","consteval","constexpr",
    "constinit","const_cast","continue","co_await","co_return","co_yield",
    "decltype","default","define","defined","delete","do","double",
    "dynamic_cast","elif","else","error","endif","enum","explicit",
    "export","extern","false","final","float","for","friend","goto",
    "if","ifdef","ifndef","import","include","inline","int","line",
    "long","module","mutable","namespace","new","noexcept","not","not_eq",
    "nullptr","operator","or","or_eq","override","pragma","private",
    "protected","public","reflexpr","register","reinterpret_cast",
    "requires","return","short","signed","sizeof","static","static_assert",
    "static_cast","struct","switch","synchronized","template","this",
    "thread_local","throw","xor_eq","true","try","typedef","typeid",
    "typename","undef","union","unsigned","using","virtual","void",
    "volatile","wchar_t","while","xor",
};
set<string> code_list;

bool in_comment = false;

bool check_chr(char c){
    if((c>='a'&&c<='z')||(c>='A'&&c<='Z')||(c>='0'&&c<='9')||c=='_') return true;
    else return false;
}

void get_input(set<string>& list,string& input){
    int j=0;
    while(input[j]){
        if(check_chr(input[j])){
            string word;
            while(check_chr(input[j])){
                char chr = input[j];
                word += chr;
                j++;
            }
            if(!(word[0]>='0'&&word[0]<='9')){
                if(!in_comment) 
                    if(key_words.find(word)==key_words.end()) list.insert(word);
            }
        }else{
            if(input[j]=='/'&&input[j+1]=='/') break;
            if(input[j]=='/'&&input[j+1]=='*') in_comment = true;
            if(input[j]=='*'&&input[j+1]=='/') in_comment = false;
            if(input[j]=='\\') j++;
            j++;
        }
    }
}

int main(){
    string str;
    while(getline(cin,str)){
        get_input(code_list,str);
    }
    for(auto word:code_list){
        cout<<word<<' ';
    }
}