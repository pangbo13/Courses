#include <stdio.h>

/* Only change any of these 4 values */
#define V0 3
#define V1 3
#define V2 1
#define V3 3

int main(void) {
	int a;
	char *s;

	printf("  SJTU labstarter:\n====================\n");

	/* for loop */
	for(a=0; a<V0; a++) {
		printf("Happy ");
	}
	printf("\n");

	/* switch statement */
	switch(V1) {
		case 0:		printf("RNG\n");
		case 1: 	printf("IG\n");	break;
		case 2: 	printf("4AM\n");
		case 3: 	printf("FPX\n");		break;
		case 4:		printf("eStarpro\n");	break;
		case 5:		printf("AG\n");
		default:	printf("I don't know these people!\n");
	}

	/* ternary operator */
	s = (V3==3) ? "Go" : "Guo";

	/* if statement */
	if(V2) {
		printf("\n%s Li!\n",s);
	} else  {
		printf("\n%s Jia !\n",s);
	}

	return 0;
}
