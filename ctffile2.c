#include <stdio.h>

int main(){
	FILE *fp, *fp2;
	int i = 0;
	char str;
	unsigned long pointer = 0;
	char filename[255];
	unsigned long address[]={
			0x00000000,
			0x00001b20,
			0x000025ff,
			0x00006808, 
			0x002A983E,
			0x002AA301,
			0x002AAAB9,
			0x002AEEBB,
			0x00551EF1,
			0x00552861,
			0x00553212,
			0x005577C5,
			0x007FA7FB,
			0x007FB2BF,
			0x007FBEDC};
	 
	fp = fopen("MrFusion.gpjb","rb");
	if (fp == NULL) {
	        printf("file open error.\n");
	        return -1;
	}

	//ファイルの終端(EOF)になるまで続ける
	//ファイルから一文字読込strに格納
	while((str = fgetc(fp)) != EOF){
		if (pointer == address[i]) {
			if (fp2 != NULL) fclose(fp2);
			sprintf(filename, "out%d.bin",i);
			fp2 = fopen(filename,"wb");
			i++;
		}
	    fprintf(fp2,"%c",str);
		pointer++;
	}
    fclose(fp2);
    fclose(fp);
	return 0;
}
