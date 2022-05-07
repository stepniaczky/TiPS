#include <fstream>
#include <string.h>
#include <windows.h>
#include "iostream"

using namespace std;

ifstream plik;
char nazwaPliku[255];                   // bufor na nazwe pliku

char znak;                              // bufor na przesylany znak
int licznikZnakow=1;
unsigned long rozmiarZnaku= sizeof(znak);
int kod;

bool transmisja=false;
bool czyPoprawnyPakiet;
int nrPakietu=1;
char paczka[128];

HANDLE   uchwytPortu;                      	// identyfikator portu
LPCTSTR  nazwaPortu;                    	// przechowuje nazwê portu
DCB      ustawieniaSterowania;              // struktura kontroli portu szeregowego
COMSTAT zasobyPortu;                        // dodatkowa informacja o zasobach portu
DWORD   blad;                         	    // reprezentuje typ ewentualnego b³êdu
COMMTIMEOUTS ustawieniaCzasu;
USHORT tmpCRC;

const char SOH=(char)1;  // Start Of Heading
const char NAK=(char)15; // Negative Acknowledge (21?)
const char CAN=(char)18; // Flaga do przerwania połączenia (24?) cancel
const char ACK=(char)6;  // Zgoda na rzesylanie danych           acknowledge
const char EOT=(char)4;  // End Of Transmission

int PoliczCRC(char *wsk, int count)
{
    int sumaKontrolnaCRC = 0;

    while (--count >= 0)
    {
        sumaKontrolnaCRC = sumaKontrolnaCRC ^ (int)*wsk++ << 8; 								 // wez znak i dopisz osiem zer
        for (int i = 0; i < 8; ++i)
            if (sumaKontrolnaCRC & 0x8000) sumaKontrolnaCRC = sumaKontrolnaCRC << 1 ^ 0x1021; // jezli lewy bit == 1 wykonuj XOR generatorm 1021
            else sumaKontrolnaCRC = sumaKontrolnaCRC << 1; 									 // jezli nie to XOR przez 0000, czyli przez to samo
    }
    return (sumaKontrolnaCRC & 0xFFFF); //1111 1111 1111 1111
}


int czyParzysty(int x, int y)
{
    if (y==0) return 1;
    if (y==1) return x;

    int wynik=x;

    for (int i=2; i<=y; i++)
        wynik=wynik*x;

    return wynik;
}


char PoliczCRC_Znaku(int n, int nrZnaku) //przeliczanie CRC na postac binarna
{
    int x, binarna[16];

    for(int z=0; z<16; z++) binarna[z]=0;

    for(int i=0; i<16; i++)
    {
        x=n%2;
        if (x==1) n=(n-1)/2;
        if (x==0) n=n/2;
        binarna[15-i]=x;
    }

    //obliczamy poszczegolne znaki sumaKontrolnaCRC (1-szy lub 2-gi)
    x=0;
    int k;

    if(nrZnaku==1) k=7;
    if(nrZnaku==2) k=15;

    for (int i=0; i<8; i++)
        x=x+czyParzysty(2,i)*binarna[k-i];

    return (char)x;//zwraca 1 lub 2 znak (bo 2 znaki to 2 bajty, czyli 16 bitów)
}



int main ()
{

 cout<<"XModem_Send \nUruchamianie transferu na porcie COM3...\n";

 nazwaPortu="COM2";

 //ustawiamy parametry portu i go otwieramy
 uchwytPortu = CreateFile(nazwaPortu, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
        if (uchwytPortu != INVALID_HANDLE_VALUE)
        {
               ustawieniaSterowania.DCBlength = sizeof(ustawieniaSterowania);
                GetCommState(uchwytPortu, &ustawieniaSterowania);
                ustawieniaSterowania.BaudRate=CBR_9600;     // predkosc transmisji
                ustawieniaSterowania.Parity = NOPARITY;       // bez bitu parzystosci
                ustawieniaSterowania.StopBits = ONESTOPBIT;    // ustawienie bitu stopu (jeden bit)
                ustawieniaSterowania.ByteSize = 8;       // liczba wysylanych bitów

                ustawieniaSterowania.fParity = TRUE;
                ustawieniaSterowania.fDtrControl = DTR_CONTROL_DISABLE; //Kontrola linii DTR: DTR_CONTROL_DISABLE (sygnal nieaktywny)
                ustawieniaSterowania.fRtsControl = RTS_CONTROL_DISABLE; //Kontrola linii RTR: DTR_CONTROL_DISABLE (sygnal nieaktywny)
                ustawieniaSterowania.fOutxCtsFlow = FALSE;
                ustawieniaSterowania.fOutxDsrFlow = FALSE;
                ustawieniaSterowania.fDsrSensitivity = FALSE;
                ustawieniaSterowania.fAbortOnError = FALSE;
                ustawieniaSterowania.fOutX = FALSE;
                ustawieniaSterowania.fInX = FALSE;
                ustawieniaSterowania.fErrorChar = FALSE;
                ustawieniaSterowania.fNull = FALSE;

                ustawieniaCzasu.ReadIntervalTimeout = 10000;
                ustawieniaCzasu.ReadTotalTimeoutMultiplier = 10000;
                ustawieniaCzasu.ReadTotalTimeoutConstant = 10000;
                ustawieniaCzasu.WriteTotalTimeoutMultiplier = 100;
                ustawieniaCzasu.WriteTotalTimeoutConstant = 100;

                SetCommState(uchwytPortu, &ustawieniaSterowania);
                SetCommTimeouts(uchwytPortu, &ustawieniaCzasu);
                ClearCommError(uchwytPortu, &blad ,&zasobyPortu);
 }
 else {
        cout<<"Nieudane polaczenie (COM3, 9600kb/s, 8-bitowe dane, jeden bit stopu)\n";
  }

  cout<<"Nazwa pliku do WYSLANIA: ";
  cin>>nazwaPliku;

 cout<<"\nOczekiwanie na rozpoczecie transmisji...\n";
 for(int i=0;i<6;i++) {
    //HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED
    ReadFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);

    if(znak=='C'){
       cout<<" | otrzymano znak\n......"<<znak<<endl;;
       kod=1;
       transmisja=true;
       break;
    }
    else if(znak==NAK){
         cout<<" | otrzymano NAK\n";
         kod=2;
         transmisja=true;
        break;
    }
 }


 if(!transmisja) exit(1);

 plik.open(nazwaPliku,ios::binary);
 while(!plik.eof())
 {
  //tablica do czyszczenia
  for(int i=0;i<128;i++)
   paczka[i]=(char)26;

  int w=0;


  while(w<128 && !plik.eof())
  {
   paczka[w]=plik.get();
   if(plik.eof()) paczka[w]=(char)26;
   w++;
  }
  czyPoprawnyPakiet=false;

  while(!czyPoprawnyPakiet)
  {
   cout<<"Trwa wysylanie pakietu. Prosze czekac...\n";
   WriteFile(uchwytPortu, &SOH,licznikZnakow,&rozmiarZnaku, NULL);  // wysylanie SOH
   znak=(char)nrPakietu;
   WriteFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);  // wyslanie numeru paczki
   znak=(char)255-nrPakietu;
   WriteFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);   // wyslanie dopelnienia


   for(int i=0;i<128;i++)
    WriteFile(uchwytPortu, &paczka[i],licznikZnakow,&rozmiarZnaku, NULL);
            if (kod==2) //suma kontrolna
              {
         char suma_kontrolna=(char)26;
            for(int i=0;i<128;i++)
               suma_kontrolna+=paczka[i]%256;
               WriteFile(uchwytPortu, &suma_kontrolna,licznikZnakow,&rozmiarZnaku, NULL);
               cout<<" Suma kontrolna = " <<suma_kontrolna<<endl;
               }
            else if(kod==1) //obliczanie CRC i transfer
               {
      tmpCRC=PoliczCRC(paczka,128);
      znak=PoliczCRC_Znaku(tmpCRC,1);
      WriteFile(uchwytPortu,&znak,licznikZnakow,&rozmiarZnaku, NULL);
      znak=PoliczCRC_Znaku(tmpCRC,2);
      WriteFile(uchwytPortu,&znak,licznikZnakow,&rozmiarZnaku, NULL);
      }


            while(1)
   {
    znak=' ';
    ReadFile(uchwytPortu,&znak,licznikZnakow,&rozmiarZnaku, NULL);

    if(znak==ACK)
    {
     czyPoprawnyPakiet=true;
     cout<<"Przeslano poprawnie pakiet danych!";
     break;
    }
    if(znak==NAK)
    {
     cout<<"ERROR - otrzymano NAK!\n";
     break;
    }
    if(znak==CAN)
    {
     cout<<"ERROR - polaczenie zostalo przerwane!\n";
     return 1;
    }
   }
  }
  //zwiekszamy numer pakietu
  if(nrPakietu==255) nrPakietu=1;
  else nrPakietu++;

 }
 plik.close();

 while(1)
 {
  znak=EOT;
  WriteFile(uchwytPortu,&znak,licznikZnakow,&rozmiarZnaku, NULL);
  ReadFile(uchwytPortu,&znak,licznikZnakow,&rozmiarZnaku, NULL);
  if(znak==ACK) break;
 }

 CloseHandle(uchwytPortu);
 cout<<"Koniec! Udalo sie wyslac plik!";
    return 0;


}
