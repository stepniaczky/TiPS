#include <fstream>
#include <string.h>
#include <windows.h>
#include <iostream>

using namespace std;

//PROGRAM ODBIERANIE

char nazwaPliku[255];   //bufor nazwy pliku
ofstream plik;

const char NAK=(char)15; //negative acknowledge
const char SOH=(char)1;  //poczatek naglowka
const char CAN=(char)18; //cancel
const char ACK=(char)6;  //acknowledge
const char EOT=(char)4;  //zakonczenie tarnsmisji

char blokDanych[128];
char znak;
unsigned long rozmiarZnaku= sizeof(znak);
int licznikZnakow=1;      //potrzebne przy czytaniu i pisaniu
bool transmisja=false;
bool poprawnyPakiet;
int numerPaczki;
char dopelnienieDo255;
char sumaKontrolnaCRC[2];      //odebrana suma kontrolna

HANDLE   uchwytPortu;                      	//identyfikator portu
LPCTSTR  nazwaPortu;
DCB      ustawieniaSterowania;              //struktura kontroli portu szeregowego
COMSTAT  zasobyPortu;                        //dodatkowe info o porcie
DWORD    blad;
COMMTIMEOUTS ustawieniaCzasu;
USHORT   tmpCRC;

int PoliczCRC(char *wsk, int count) //suma kontrolna CRC
{
    int sumaKontrolnaCRC = 0;

    while (--count >= 0)
    {
        sumaKontrolnaCRC = sumaKontrolnaCRC ^ (int)*wsk++ << 8; 	//dopisanie 8 zer do znaku
        for (int i = 0; i < 8; ++i)
            if (sumaKontrolnaCRC & 0x8000) {sumaKontrolnaCRC = sumaKontrolnaCRC << 1 ^ 0x1021;} //jezli lewy bit == 1 wykonuj XOR przez 1021
            else {sumaKontrolnaCRC = sumaKontrolnaCRC << 1;} 									  //jezli nie to XOR przez 0000
    }
    return (sumaKontrolnaCRC & 0xFFFF);
}


int czyParzysty(int x, int y) //sprawdzenie parzystosci bitu
{
    if (y == 0) {return 1;}
    if (y == 1) {return x;}
    int wynik=x;
    for (int i = 2; i <= y; i++) {
        wynik = wynik * x;
    }
    return wynik;
}

char PoliczCRC_Znaku(int n, int nrZnaku) //przeliczanie sumy CRC na postac binarna
{
    int x, binarna[16];
    for(int z = 0; z < 16; z++) binarna[z]=0;
    for(int i = 0; i < 16; i++)
    {
        x = n % 2;
        if (x == 1) {n = (n-1) / 2;}
        if (x == 0) {n = n / 2;}
        binarna[15 - i] = x;
    }
    //obliczamy poszczegolne znaki sumaKontrolnaCRC (1-szy lub 2-gi)
    x = 0;
    int k;
    if(nrZnaku == 1) {k = 7;}
    if(nrZnaku == 2) {k = 15;}
    for (int i = 0; i < 8; i++)
        x = x + czyParzysty(2, i) * binarna[k - i];
    return (char)x;//zwraca 1 lub 2 znak (bo 2 znaki to 2 bajty, czyli 16 bitow)
}



int main() {
    int wybor = 0;
    cout<<"Please choose port:\n";
    cout<<"[1]. COM2\n";
    cout<<"[2]. COM3\n";
    cin>>wybor;

    if (wybor == 1) {nazwaPortu = "COM2";}
    else {nazwaPortu = "COM3";}


    uchwytPortu = CreateFile(nazwaPortu, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    if (uchwytPortu != INVALID_HANDLE_VALUE)
    {
        ustawieniaSterowania.DCBlength = sizeof(ustawieniaSterowania);
        GetCommState(uchwytPortu, &ustawieniaSterowania);
        ustawieniaSterowania.BaudRate=CBR_9600;     //predkosc transmisji
        ustawieniaSterowania.Parity = NOPARITY;     //bez bitu parzystosci
        ustawieniaSterowania.StopBits = ONESTOPBIT; //ustawienie bitu stopu (jeden bit)
        ustawieniaSterowania.ByteSize = 8;       //rozmiar bajtu
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
    else {cout<<"Failed to setup port on "<<nazwaPortu<<"!\n";}

    cout<<"Save to file with name: ";
    cin>>nazwaPliku;
    cout << "Start with NAK or C?\n";
    string aa;
    cin >>aa;
    if(aa == "NAK") znak = NAK;
    else znak = 'C';

    for(int i = 0; i < 6; i++) {
        cout<<"\nSending\n";
        //HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED
        WriteFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);
        //czeka na SOH
        cout<<"Waiting for SOH...\n";
        ReadFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);
        if(znak == SOH) {
            cout<<"Connection established\n";
            transmisja = true;
            break;
        }
    }

    if(!transmisja) { //nie bylo SOH
        cout<<"ERROR - connection failed\n";
        exit(1);
    }
    plik.open(nazwaPliku,ios::binary);
    cout<<"Receiving the file, please wait...";
    ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
    numerPaczki = (int)znak;
    ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
    dopelnienieDo255=znak;

    for(int i = 0; i < 128; i++){
        ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
        blokDanych[i] = znak;
    }
    ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
    sumaKontrolnaCRC[0] = znak;
    ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
    sumaKontrolnaCRC[1] = znak;
    poprawnyPakiet = true;
    if ((char)(255 - numerPaczki) != dopelnienieDo255){
        cout<<"ERROR - incorrect package number!\n";
        WriteFile(uchwytPortu, &NAK,licznikZnakow,&rozmiarZnaku, NULL);
        poprawnyPakiet = false;
    }
    else {
        tmpCRC = PoliczCRC(blokDanych,128); // sprawdzanie czy sumy kontrole sa poprawne
        if(PoliczCRC_Znaku(tmpCRC,1) != sumaKontrolnaCRC[0] || PoliczCRC_Znaku(tmpCRC,2) != sumaKontrolnaCRC[1]) {
            cout<<"ERROR - incorrect checksum!\n";
            WriteFile(uchwytPortu, &NAK,licznikZnakow,&rozmiarZnaku, NULL); //NAK
            poprawnyPakiet = false;
        }
    }

    if(poprawnyPakiet) {
        for(int i = 0; i < 128; i++) {
            if(blokDanych[i] != 26) {plik<<blokDanych[i];}
        }
        cout<<"Package sent successfully\n";
        WriteFile(uchwytPortu, &ACK,licznikZnakow,&rozmiarZnaku, NULL);
    }

    while(1) {
        ReadFile(uchwytPortu, &znak,licznikZnakow,&rozmiarZnaku, NULL);
        if(znak == EOT || znak == CAN) break;
        cout<<"Receiving data. ";
        ReadFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);
        numerPaczki = (int)znak;
        ReadFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);
        dopelnienieDo255=znak;
        for(int i = 0; i < 128; i++) {
            ReadFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);
            blokDanych[i] = znak;
            }
        ReadFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);
        sumaKontrolnaCRC[0] = znak;
        ReadFile(uchwytPortu, &znak, licznikZnakow, &rozmiarZnaku, NULL);
        sumaKontrolnaCRC[1] = znak;
        poprawnyPakiet = true;
        if((char)(255 - numerPaczki) != dopelnienieDo255) {
            cout<<"ERROR - incorrect package number!\n";
            WriteFile(uchwytPortu, &NAK,licznikZnakow,&rozmiarZnaku, NULL);
            poprawnyPakiet = false;
        }
        else {
            tmpCRC=PoliczCRC(blokDanych,128);
            if(PoliczCRC_Znaku(tmpCRC,1) != sumaKontrolnaCRC[0] || PoliczCRC_Znaku(tmpCRC,2) != sumaKontrolnaCRC[1]) {
                cout<<"ERROR - incorrect checksum!\n";
                WriteFile(uchwytPortu, &NAK,licznikZnakow,&rozmiarZnaku, NULL);
                poprawnyPakiet = false;
            }
        }
        if(poprawnyPakiet) {
            for(int i = 0; i < 128; i++) {
                if(blokDanych[i] != 26)
                    plik<<blokDanych[i];
            }
            cout<<"Package sent successfully!\n";
            WriteFile(uchwytPortu, &ACK,licznikZnakow,&rozmiarZnaku, NULL);
        }
    }

    WriteFile(uchwytPortu, &ACK,licznikZnakow,&rozmiarZnaku, NULL);
    plik.close();
    CloseHandle(uchwytPortu);
    if(znak == CAN) cout<<"ERROR - connection lost!\n";
    else cout<<"[ File received successfully! ]";
    return 0;
}
