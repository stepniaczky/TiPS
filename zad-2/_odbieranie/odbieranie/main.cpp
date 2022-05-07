#include <fstream>
#include <string.h>
#include <windows.h>
#include <iostream>

using namespace std;


char nazwaPliku[255];
ofstream plik;

char blokDanych[128];
char znak;
unsigned long rozmiarZnaku= sizeof(znak);
int licznikZnakow=1;      //potrzebne przy czytaniu i pisaniu
bool transmisja=false;
bool poprawnyPakiet;
int numerPaczki;
char dopelnienieDo255;
char sumaKontrolnaCRC[2];      //odebrane sumaKontrolnaCRC

HANDLE   uchwytPortu;                      	// identyfikator portu
LPCTSTR  nazwaPortu;                    	// przechowuje nazwê portu  L‌ong P‌ointer to a C‌onst T‌CHAR STR‌ing
DCB      ustawieniaSterowania;              // struktura kontroli portu szeregowego
COMSTAT zasobyPortu;                        // dodatkowa informacja o zasobach portu
DWORD   blad;                         	    // reprezentuje typ ewentualnego bledu
COMMTIMEOUTS ustawieniaCzasu;
USHORT tmpCRC;

const char SOH=(char)1;  // Start Of Heading
const char NAK=(char)15; // Negative Acknowledge
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
    return (sumaKontrolnaCRC & 0xFFFF);
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




int main()
{
  cout<<"XModem_Received \nUruchamianie transferu na porcie COM2...\n";

 nazwaPortu="COM2"; // else nazwaPortu="COM2";

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
        cout<<"Nieudane polaczenie (COM2, 9600kb/s, 8-bitowe dane, jeden bit stopu)\n";
  }

  cout<<"Nazwa pliku do ZAPISU: ";
  cin>>nazwaPliku;

    cout << "Wpisz NAK lub C\n";
    string aa;
    cin >>aa;
    if(aa=="NAK") znak = NAK;
    else znak = 'C';

 for(int i=0;i<6;i++)
 {
  cout<<"\nWysylanie\n";
  //HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED
  WriteFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);
  //czeka na SOH
  cout<<"Oczekiwanie na komunikat SOH...\n";
  ReadFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);
  cout<<znak<<endl;
       if(znak==SOH)
  {
   cout<<"Ustanowienie polaczenia powiodlo sie!\n";
   transmisja=true;
   break;
  }
 }

 //nie nadszedl SOH
 if(!transmisja)
 {
  cout<<"ERROR - polaczenie nieudane\n";
  exit(1);
 }
 plik.open(nazwaPliku,ios::binary);
 cout<<"Trwa odbieranie pliku, prosze czekac...";

 ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
 numerPaczki=(int)znak;

 ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
 dopelnienieDo255=znak;

 for(int i=0;i<128;i++)
 {
  ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
  blokDanych[i]=znak;
 }

 ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
 sumaKontrolnaCRC[0]=znak;
 ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
 sumaKontrolnaCRC[1]=znak;
 poprawnyPakiet=true;


      if ((char)(255-numerPaczki)!=dopelnienieDo255)
 {
  cout<<"ERROR - otrzymano niepoprawny numer pakietu!\n";
  WriteFile(uchwytPortu, &NAK,licznikZnakow,&rozmiarZnaku, NULL);
  poprawnyPakiet=false;

 }
 else
 {
  tmpCRC=PoliczCRC(blokDanych,128); // sprawdzanie czy sumy kontrole sa poprawne

  if(PoliczCRC_Znaku(tmpCRC,1)!=sumaKontrolnaCRC[0] || PoliczCRC_Znaku(tmpCRC,2)!=sumaKontrolnaCRC[1])
  {
   cout<<"ERROR - zla suma kontrola!\n";
   WriteFile(uchwytPortu, &NAK,licznikZnakow,&rozmiarZnaku, NULL); //NAK
   poprawnyPakiet=false;
  }
 }

 if(poprawnyPakiet)
 {
  for(int i=0;i<128;i++)
   {
    if(blokDanych[i]!=26)
     plik<<blokDanych[i];
   }
  cout<<"Przeslanie pakietu zakonczone powodzeniem!\n";
  WriteFile(uchwytPortu, &ACK,licznikZnakow,&rozmiarZnaku, NULL);
 }

 while(1)
 {
  ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
  if(znak==EOT || znak==CAN) break;
  cout<<"Trwa odbieranie danych...";

  ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
  numerPaczki=(int)znak;

  ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
  dopelnienieDo255=znak;

  for(int i=0;i<128;i++)
  {
   ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
   blokDanych[i]=znak;
  }


        ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
  sumaKontrolnaCRC[0]=znak;
  ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
  sumaKontrolnaCRC[1]=znak;
        poprawnyPakiet=true;

 if((char)(255-numerPaczki)!=dopelnienieDo255)
  {
   cout<<"ERROR - zly numer pakietu!\n";
   WriteFile(uchwytPortu, &NAK,licznikZnakow,&rozmiarZnaku, NULL);
   poprawnyPakiet=false;
  }
  else
  {
   tmpCRC=PoliczCRC(blokDanych,128);

   if(PoliczCRC_Znaku(tmpCRC,1)!=sumaKontrolnaCRC[0] || PoliczCRC_Znaku(tmpCRC,2)!=sumaKontrolnaCRC[1])
   {
    cout<<"ERROR - zla suma kontrolna!\n";
    WriteFile(uchwytPortu, &NAK,licznikZnakow,&rozmiarZnaku, NULL);
    poprawnyPakiet=false;
   }
  }
  if(poprawnyPakiet)
  {
   for(int i=0;i<128;i++)
   {
    if(blokDanych[i]!=26)
     plik<<blokDanych[i];
   }

   cout<<"Przeslanie pakietu zakonczone powodzeniem!\n";
   WriteFile(uchwytPortu, &ACK,licznikZnakow,&rozmiarZnaku, NULL);
  }
 }
 WriteFile(uchwytPortu, &ACK,licznikZnakow,&rozmiarZnaku, NULL);

 plik.close();
 CloseHandle(uchwytPortu);

 if(znak==CAN) cout<<"ERROR - polaczenie zostalo przerwane! \n";
 else cout<<"Hurra! Plik w calosci odebrany!";
 cin.get();
 cin.get();
 int a;
 cin>>a;

 return 0;
}
