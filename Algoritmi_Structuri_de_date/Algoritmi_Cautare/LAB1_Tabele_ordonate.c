#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 200

typedef struct {
    int nr;
    char titlu[200];
    int pagini;
} Carte;

// Eliminare spatii 
void trim(char *s) {
    while (*s == ' ' || *s == '\n' || *s == '\r' || *s == '\t')
        memmove(s, s + 1, strlen(s));
    int len = strlen(s);
    while (len > 0 &&
          (s[len-1] == ' ' || s[len-1] == '\n' ||
           s[len-1] == '\r' || s[len-1] == '\t')) {
        s[len-1] = '\0';
        len--;
    }
}

// Citire fisier 
int citireCarti(const char *fisier, Carte v[]) {
    FILE *f = fopen(fisier, "r");
    if (!f) {
        printf("Eroare la deschiderea fisierului %s\n", fisier);
        return 0;
    }
    char line[512];
    int n = 0;

    while (fgets(line, sizeof(line), f)) {
        char title[200], autor[100], anul[10], gen[100], pret[20], limba[50];
        int num, pagini;
        if (sscanf(line,
            " %d. %199[^,], %99[^,], %9[^,], %99[^,], %19[^,], %49[^,], %d",
            &num, title, autor, anul, gen, pret, limba, &pagini) == 8) {
            trim(title);
            v[n].nr = num;
            strcpy(v[n].titlu, title);
            v[n].pagini = pagini;
            n++;
        }
        if (n >= MAX) break;
    }
    fclose(f);
    return n;
}

// SECVENTIALA 
int cautareSecventiala(Carte v[], int n, char *x, int *iteratii) {
    *iteratii = 0;
    for (int i = 0; i < n; i++) {
        (*iteratii)++;
        if (strcmp(v[i].titlu, x) == 0)
            return i;
    }
    return -1;
}

// BINARA 
int cautareBinara(Carte v[], int n, char *x, int *iteratii) {
    int st = 0, dr = n - 1;
    *iteratii = 0;
    while (st <= dr) {
        (*iteratii)++;
        int m = (st + dr) / 2;
        int cmp = strcmp(x, v[m].titlu);
        if (cmp == 0)
            return m;
        if (cmp < 0)
            dr = m - 1;
        else
            st = m + 1;
    }
    return -1;
}

// INTERPOLARA 
int cautareInterpolara(Carte v[], int n, int x, int *iteratii) {
    int st = 0, dr = n - 1;
    *iteratii = 0;
    while (st <= dr &&
           x >= v[st].pagini &&
           x <= v[dr].pagini) {
        (*iteratii)++;
        if (v[dr].pagini == v[st].pagini)
            break;
        int pos = st + (double)(dr - st) *
                 (x - v[st].pagini) /
                 (v[dr].pagini - v[st].pagini);
        if (v[pos].pagini == x)
            return pos;
        if (v[pos].pagini < x)
            st = pos + 1;
        else
            dr = pos - 1;
    }
    if (st < n && v[st].pagini == x)
        return st;
    return -1;
}

// FIBONACCI 
int cautareFibonacci(Carte v[], int n, char *x, int *iteratii) {
    int fibMm2 = 0;
    int fibMm1 = 1;
    int fibM = fibMm1 + fibMm2;
    *iteratii = 0;
    while (fibM < n) {
        fibMm2 = fibMm1;
        fibMm1 = fibM;
        fibM = fibMm1 + fibMm2;
    }
    int offset = -1;
    while (fibM > 1) {
        (*iteratii)++;
        int i = (offset + fibMm2 < n - 1) ?
                offset + fibMm2 : n - 1;

        int cmp = strcmp(v[i].titlu, x);
        if (cmp < 0) {
            fibM = fibMm1;
            fibMm1 = fibMm2;
            fibMm2 = fibM - fibMm1;
            offset = i;
        }
        else if (cmp > 0) {
            fibM = fibMm2;
            fibMm1 = fibMm1 - fibMm2;
            fibMm2 = fibM - fibMm1;
        }
        else
            return i;
    }

    if (fibMm1 && offset + 1 < n &&
        strcmp(v[offset + 1].titlu, x) == 0)
        return offset + 1;
    return -1;
}

// MENIU 
int main() {
    int opt;
    do {
        printf("\nTabele Ordonate\n");
        printf("1. Cautare binara (pe titlu)\n");
        printf("2. Cautare interpolara (pe nr pagini)\n");
        printf("3. Cautare secventiala (pe titlu)\n");
        printf("4. Cautare Fibonacci (pe titlu)\n");
        printf("0. Iesire\n");
        printf("Optiune: ");
        scanf("%d", &opt);
        getchar();

        if (opt == 1 || opt == 3 || opt == 4) {
            Carte v[MAX];
            int n = citireCarti("Lista_ordonata.txt", v);
            if (n == 0) continue;
            char x[200];
            printf("\nIntrodu titlul cautat: ");
            fgets(x, sizeof(x), stdin);
            x[strcspn(x, "\n")] = 0;
            trim(x);
            int poz = -1;
            int iteratii = 0;
            if (opt == 1) {
                poz = cautareBinara(v, n, x, &iteratii);
                printf("\nCautarea binara\n");
            }
            if (opt == 3) {
                poz = cautareSecventiala(v, n, x, &iteratii);
                printf("\nCautare secventiala\n");
            }
            if (opt == 4) {
                poz = cautareFibonacci(v, n, x, &iteratii);
                printf("\nCautare Fibonacci\n");
            }
            printf("Iteratii: %d\n", iteratii);
            if (poz != -1)
                printf("Gasit la pozitia %d: %s\n",
                       poz+1, v[poz].titlu);
            else
                printf("Titlul nu a fost gasit\n");
        }

        if (opt == 2) {
            Carte v[MAX];
            int n = citireCarti("Lista_ordonata_pagini.txt", v);
            if (n == 0) continue;
            int pag;
            printf("\nNumar pagini cautat: ");
            scanf("%d", &pag);
            int iteratii = 0;
            int poz = cautareInterpolara(v, n, pag, &iteratii);
            printf("\nCautare interpolara\n");
            printf("Iteratii: %d\n", iteratii);
            if (poz != -1)
                printf("Gasit la pozitia %d: %s\n",
                       poz+1, v[poz].titlu);
            else
                printf("Titlul nu a fost gasit\n");
        }
    } while (opt != 0);
    return 0;
}