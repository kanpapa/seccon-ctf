#include <stdio.h>
#include <limits.h>

int main()
{
  long data_size[]={
			0x00000000,
			0x00001b1f,
			0x000025ff,
			0x00006808, 
			0x002A983E,
			0x002AA300,
			0x002AAAB9,
			0x002AEEBB,
			0x00551EF1,
			0x00552860,
			0x00553212,
			0x005577C5,
			0x007FA7FB,
			0x007FB2BE,
			0x007FBEDC,
			0x007FFF21};
	 
  FILE *fpr;
  FILE *fpw;
  char *fname_r = "MrFusion.gpjb";
  char fname_w[256];
  fpos_t pos;
  /* 
  unsigned char buf[8488386];
  */
  unsigned char buf[3000000];

  int i;
  size_t size;

  printf("TYPE\t\tMIN\t\t\tMAX\n");
  printf("char\t\t%d\t\t\t%d\n", CHAR_MIN, CHAR_MAX);
  printf("short\t\t%d\t\t\t%d\n", SHRT_MIN, SHRT_MAX);
  printf("int\t\t%d\t\t%d\n", INT_MIN, INT_MAX);
  printf("long\t\t%ld\t\t%ld\n", LONG_MIN, LONG_MAX);
  printf("long long\t%lld\t%lld\n", LLONG_MIN, LLONG_MAX);

  printf("data file open.\n");

  fpr = fopen( fname_r, "rb" );
  if( fpr == NULL ){
    printf( "読込用 %sファイルが開けません\n", fname_r );
    return -1;
  }

  for (i = 0; i < 15; i++){
      size = fread( buf, sizeof( unsigned char ), data_size[i + 1] - data_size[i] , fpr );
      printf("data1:%08lx - data2:%08lx size:%08lx ",data_size[i], data_size[i + 1], size);

      sprintf(fname_w, "out%d.bin",i);

      fpw = fopen( fname_w, "wb" );
      if( fpw == NULL ){
           printf( "書込用 %sファイルが開けません\n", fname_w );
           return -1;
      }
      fwrite( buf, sizeof( unsigned char ), size, fpw );
      fclose( fpw );

      printf( "%sファイルのコピーが終わりました\n", fname_w );

      /* printf("seek: %d\n", fseek(fpr, size, SEEK_CUR)); */
      printf("seek: %d\n", fseek(fpr, data_size[i + 1], SEEK_SET));
  }
  fclose( fpr );

  return 0;
}
