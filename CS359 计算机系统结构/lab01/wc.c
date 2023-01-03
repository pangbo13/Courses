#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

void wc(FILE *ofile, FILE *infile, char *inname) {
    char ch;
    int cCount = 0,wCount = 0,lCount = 0;
    int in_word = 0;
	if(!ofile) ofile = stdout;
	if(!infile) infile = stdin;
	if(!inname) inname = "";
    while(!feof(infile)){
        ch = fgetc(infile);
        if(ch!=EOF) cCount++;
        if(ch>=33&&ch<=126){
            if(!in_word){
                in_word = 1;
                wCount++;
            }
        }else in_word = 0;
        if(ch == '\n') lCount++;
    }
    fprintf(ofile,"%8d%8d%8d\t%s\n",lCount,wCount,cCount,inname);
}

int main (int argc, char *argv[]) {

  char* out_file_name = NULL;
	char* inname = NULL;
	if(argc == 1) wc(NULL,NULL,NULL);
	else if(argc == 2){
		inname = argv[1];
		FILE *infile = fopen(inname,"r");
		if(!infile){
			perror("Input file opening failed");
			exit(1);
		}
		wc(NULL,infile,inname);
	}
	else if(argc == 3){
		inname = argv[1];
		FILE *infile = fopen(inname,"r");
		if(!infile){
			perror("Input file opening failed");
			exit(1);
		}
		FILE *out_file = fopen(argv[2],"w");
		if(!out_file){
			perror("Output file opening failed");
			exit(1);
		}
		wc(out_file,infile,inname);
	}
	else{
		printf("arguments error\n");
		exit(1);
	}
	return 0;

}

