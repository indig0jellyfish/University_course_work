#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX 100

//STRUCTURI 
typedef struct {
    char titlu[100];
} Carte;
typedef struct {
    Carte c;
    int st, dr;
} Nod;

//CITIRE DIN FISIER 
int citireCarti(Carte v[]) {
    FILE *f = fopen("Lista_neordonata.txt", "r");
    if (!f) {
        printf("Nu pot deschide fisierul!\n");
        return 0;
    }

    int n = 0, num;
    char line[512];
    while (fgets(line, sizeof(line), f)) {
        if (sscanf(line, " %d. %99[^,]", &num, v[n].titlu) == 2) {
            n++;
            if (n >= MAX) break;
        }
    }
    fclose(f);
    return n;
}

//CAUTARE SECVENȚIALĂ 

void cautareSecventiala() {
    Carte v[MAX];
    int n = citireCarti(v);
    if (n == 0) return;
    char cautat[100];
    int iteratii = 0;
    int gasit = -1;

    printf("Introdu titlul cautat: ");
    getchar();
    fgets(cautat, sizeof(cautat), stdin);
    cautat[strcspn(cautat, "\n")] = 0;
    for (int i = 0; i < n; i++) {
        iteratii++;
        if (strcmp(v[i].titlu, cautat) == 0) {
            gasit = i;
            break;
        }
    }

    printf("\nCautare secventiala\n");
    printf("Iteratii: %d\n", iteratii);
    if (gasit != -1)
        printf("Gasit la pozitia %d: %s\n", gasit + 1, v[gasit].titlu);
    else
        printf("Titlul nu a fost gasit\n");
}

//INSERARE IN ARBORE 

int inserare(Nod arb[], int *n, int rad, Carte c) {
    if (rad == -1) {
        arb[*n].c = c;
        arb[*n].st = -1;
        arb[*n].dr = -1;
        (*n)++;
        return (*n) - 1;
    }
    if (strcmp(c.titlu, arb[rad].c.titlu) < 0)
        arb[rad].st = inserare(arb, n, arb[rad].st, c);
    else
        arb[rad].dr = inserare(arb, n, arb[rad].dr, c);
    return rad;
}

//CONSTRUIRE ARBORE 
int construireArbore(Nod arb[]) {
    Carte v[MAX];
    int nCarti = citireCarti(v);
    int n = 0;
    int rad = -1;
    for (int i = 0; i < nCarti; i++)
        rad = inserare(arb, &n, rad, v[i]);
    return n;
}

void afisareArbore(Nod arb[], int n) {
    printf("\nArbore Binar:\n\n");
    for (int i = 0; i < n; i++) {
        printf("%d. %s [",
               i + 1,
               arb[i].c.titlu);
        if (arb[i].st != -1)
            printf("%d", arb[i].st + 1);
        else
            printf("-");
        printf(", ");
        if (arb[i].dr != -1)
            printf("%d", arb[i].dr + 1);
        else
            printf("-");
        printf("]\n");
    }
}

//CAUTARE IN ARBORE 
void cautareArbore() {
    Nod arb[MAX];
    int n = construireArbore(arb);
    if (n == 0) return;
    afisareArbore(arb, n);   // <<< AICI AFIȘĂM STRUCTURA
    char cautat[100];
    int iteratii = 0;
    int curent = 0;

    printf("\nIntrodu titlul cautat: ");
    getchar();
    fgets(cautat, sizeof(cautat), stdin);
    cautat[strcspn(cautat, "\n")] = 0;
    while (curent != -1) {
        iteratii++;
        int cmp = strcmp(cautat, arb[curent].c.titlu);
        if (cmp == 0)
            break;
        else if (cmp < 0)
            curent = arb[curent].st;
        else
            curent = arb[curent].dr;
    }

    printf("\nCautare in arbore binar\n");
    printf("Iteratii: %d\n", iteratii);

    if (curent != -1)
        printf("Gasit la index intern %d: %s\n",
               curent,
               arb[curent].c.titlu);
    else
        printf("Titlul nu a fost gasit\n");
}

//MENIU 
int main() {
    int opt;
    do {
        printf("\nTabele Neordonate\n");
        printf("1. Arborele Binar\n");
        printf("2. Cautarea secventiala\n");
        printf("0. Iesire\n");
        printf("Optiune: ");
        scanf("%d", &opt);
        switch (opt) {
            case 1:
                cautareArbore();
                break;
            case 2:
                cautareSecventiala();
                break;
            case 0:
                break;
            default:
                printf("Optiune invalida!\n");
        }
    } while (opt != 0);
    return 0;
}