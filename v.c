#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>

/*

Vigenere 100 points

k: ????????????
p: SECCON{???????????????????????????????????}
c: LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ

k=key, p=plain, c=cipher, md5(p)=f528a6ab914c1ecf856a1d93103948fe

key: VIGENERxxxxx


 |ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
-+----------------------------
A|ABCDEFGHIJKLMNOPQRSTUVWXYZ{}
B|BCDEFGHIJKLMNOPQRSTUVWXYZ{}A
C|CDEFGHIJKLMNOPQRSTUVWXYZ{}AB
D|DEFGHIJKLMNOPQRSTUVWXYZ{}ABC
E|EFGHIJKLMNOPQRSTUVWXYZ{}ABCD
F|FGHIJKLMNOPQRSTUVWXYZ{}ABCDE
G|GHIJKLMNOPQRSTUVWXYZ{}ABCDEF
H|HIJKLMNOPQRSTUVWXYZ{}ABCDEFG
I|IJKLMNOPQRSTUVWXYZ{}ABCDEFGH
J|JKLMNOPQRSTUVWXYZ{}ABCDEFGHI
K|KLMNOPQRSTUVWXYZ{}ABCDEFGHIJ
L|LMNOPQRSTUVWXYZ{}ABCDEFGHIJK
M|MNOPQRSTUVWXYZ{}ABCDEFGHIJKL
N|NOPQRSTUVWXYZ{}ABCDEFGHIJKLM
O|OPQRSTUVWXYZ{}ABCDEFGHIJKLMN
P|PQRSTUVWXYZ{}ABCDEFGHIJKLMNO
Q|QRSTUVWXYZ{}ABCDEFGHIJKLMNOP
R|RSTUVWXYZ{}ABCDEFGHIJKLMNOPQ
S|STUVWXYZ{}ABCDEFGHIJKLMNOPQR
T|TUVWXYZ{}ABCDEFGHIJKLMNOPQRS
U|UVWXYZ{}ABCDEFGHIJKLMNOPQRST
V|VWXYZ{}ABCDEFGHIJKLMNOPQRSTU
W|WXYZ{}ABCDEFGHIJKLMNOPQRSTUV
X|XYZ{}ABCDEFGHIJKLMNOPQRSTUVW
Y|YZ{}ABCDEFGHIJKLMNOPQRSTUVWX
Z|Z{}ABCDEFGHIJKLMNOPQRSTUVWXY
{|{}ABCDEFGHIJKLMNOPQRSTUVWXYZ
}|}ABCDEFGHIJKLMNOPQRSTUVWXYZ{


*/

void md5_check(char *data)
{

    char *anshash = "f528a6ab914c1ecf856a1d93103948fe";

    MD5_CTX c;
    unsigned char md[MD5_DIGEST_LENGTH];
    char mdString[33];
    int r, i;
    
    r = MD5_Init(&c);
    if(r != 1) {
        perror("init");
        exit(1);
    }
    
    r = MD5_Update(&c, data, strlen(data));
    if(r != 1) {
        perror("update");
        exit(1);
    }
    
    r = MD5_Final(md, &c);
    if(r != 1) {
        perror("final");
        exit(1);
    }
 
    for(i = 0; i < 16; i++)
         sprintf(&mdString[i * 2], "%02x", (unsigned int)md[i]);
 
    printf("md5 digest: %s\n", mdString);

    if (strcmp(mdString, anshash) == 0) {
	printf("DONE! plain:%s md5:%s\n",data,mdString);
	exit(1);
    }
}

int decrypt(char *key)
{
  char codecode[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}ABCDEFGHIJKLMNOPQRSTUVWXYZ{}";
  char clpher[] = "LMIG}RPEDOEEWKJIQIWKJWMNDTSR}TFVUFWYOCBAJBQ";
  char plain[100];

  printf("key: %s\n",key);
  int kp = 0; // key pointer
  int pp = 0; // plain text pointer
  char cnum;
  char knum;
  for (int i = 0; i < strlen(clpher); i++){
     char c = clpher[i];
     if ( c == '{' ) {
	 cnum = 26;
     } else {
         if ( c == '}' ) {
              cnum = 27;
         } else {
           cnum = c - 'A';
         }
     }

     if (key[kp] == '{') {
         knum = 26;
     } else {
     	if (key[kp] == '}') {
         knum = 27;
  	} else {
         knum = key[kp] - 'A';
	}
     }
     //printf("knum: %d cnum:%d\n",knum,cnum);

     plain[pp] = codecode[(28 - knum) + cnum];
     pp++;
     kp++;
     if (kp > 11) { kp = 0; };
  }  
  plain[pp] = 0;
  printf("plain: %s\n",plain);
  md5_check(plain);
}

int main()
{
  char code[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ{}";
  char key[5];
  char keytmp[12];

  for(int i=0; i<28; i++){
        key[0]=code[i];
	for(int j=0; j<28; j++){
	  key[1]=code[j];
          for(int k=0; k<28; k++){
            key[2]=code[k];
            for(int l=0; l<28; l++){
              key[3]=code[l];
              for(int m=0; m<28; m++){
                  key[4]=code[m];
                  key[5]=0;
		  //VIGENERxxxxx
                  sprintf(keytmp, "VIGENER%s\n",key);
	  	  decrypt(keytmp);
              }
            }
       }
    }
  }

}
