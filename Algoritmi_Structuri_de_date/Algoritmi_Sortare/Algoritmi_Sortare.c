#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX 200
#define TITLU_LEN 200

typedef struct {
    int id;
    char titlu[TITLU_LEN];
} Carte;

// CITIRE 
int citireCarti(Carte v[]) {
    FILE *f = fopen("Lista_neordonata.txt", "r");
    if (!f) {
        printf("Nu pot deschide fisierul!\n");
        return 0;
    }

    int n = 0, num;
    char line[512];

    while (fgets(line, sizeof(line), f)) {
        if (sscanf(line, " %d. %199[^,]", &num, v[n].titlu) == 2) {
            v[n].id = num;
            n++;
            if (n >= MAX) break;
        }
    }

    fclose(f);
    return n;
}

// AFISARE 
void afisare(Carte v[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d. %s\n", v[i].id, v[i].titlu);
}

// COPIE 
void copiaza(Carte d[], Carte s[], int n) {
    for (int i = 0; i < n; i++)
        d[i] = s[i];
}

//  BUBBLE  
void bubbleSort(Carte v[], int n, unsigned long long *c, unsigned long long *m) {
    *c = *m = 0;
    for (int i = 0; i < n-1; i++) {
        for (int j = 0; j < n-1-i; j++) {
            (*c)++;
            if (v[j].id > v[j+1].id) {
                Carte t = v[j];
                v[j] = v[j+1];
                v[j+1] = t;
                (*m)++;
            }
        }
    }
}

//  INSERTION  
void insertionSort(Carte v[], int n, unsigned long long *c, unsigned long long *m) {
    *c = *m = 0;
    for (int i = 1; i < n; i++) {
        Carte key = v[i];
        int j = i - 1;
        while (j >= 0) {
            (*c)++;
            if (v[j].id > key.id) {
                v[j+1] = v[j];
                (*m)++;
                j--;
            } else break;
        }
        v[j+1] = key;
        (*m)++;
    }
}

//  SELECTION  
void selectionSort(Carte v[], int n, unsigned long long *c, unsigned long long *m) {
    *c = *m = 0;
    for (int i = 0; i < n-1; i++) {
        int min = i;
        for (int j = i+1; j < n; j++) {
            (*c)++;
            if (v[j].id < v[min].id)
                min = j;
        }
        if (min != i) {
            Carte t = v[i];
            v[i] = v[min];
            v[min] = t;
            (*m)++;
        }
    }
}

//  QUICK  
int partition(Carte v[], int st, int dr, unsigned long long *c, unsigned long long *m) {
    int pivot = v[dr].id;
    int i = st - 1;

    for (int j = st; j < dr; j++) {
        (*c)++;
        if (v[j].id <= pivot) {
            i++;
            Carte t = v[i];
            v[i] = v[j];
            v[j] = t;
            (*m)++;
        }
    }

    Carte t = v[i+1];
    v[i+1] = v[dr];
    v[dr] = t;
    (*m)++;

    return i+1;
}

void quickSortRec(Carte v[], int st, int dr, unsigned long long *c, unsigned long long *m) {
    if (st < dr) {
        int p = partition(v, st, dr, c, m);
        quickSortRec(v, st, p-1, c, m);
        quickSortRec(v, p+1, dr, c, m);
    }
}

void quickSort(Carte v[], int n, unsigned long long *c, unsigned long long *m) {
    *c = *m = 0;
    quickSortRec(v, 0, n-1, c, m);
}

//  SHELL  
void shellSort(Carte v[], int n, unsigned long long *c, unsigned long long *m) {
    *c = *m = 0;
    for (int gap = n/2; gap > 0; gap /= 2) {
        for (int i = gap; i < n; i++) {
            Carte temp = v[i];
            int j = i;
            while (j >= gap) {
                (*c)++;
                if (v[j-gap].id > temp.id) {
                    v[j] = v[j-gap];
                    (*m)++;
                    j -= gap;
                } else break;
            }
            v[j] = temp;
            (*m)++;
        }
    }
}

//  HEAP  
void heapify(Carte v[], int n, int i, unsigned long long *c, unsigned long long *m) {
    int max = i;
    int st = 2*i + 1;
    int dr = 2*i + 2;

    if (st < n) {
        (*c)++;
        if (v[st].id > v[max].id)
            max = st;
    }

    if (dr < n) {
        (*c)++;
        if (v[dr].id > v[max].id)
            max = dr;
    }

    if (max != i) {
        Carte t = v[i];
        v[i] = v[max];
        v[max] = t;
        (*m)++;
        heapify(v, n, max, c, m);
    }
}

void heapSort(Carte v[], int n, unsigned long long *c, unsigned long long *m) {
    *c = *m = 0;

    for (int i = n/2 - 1; i >= 0; i--)
        heapify(v, n, i, c, m);

    for (int i = n-1; i > 0; i--) {
        Carte t = v[0];
        v[0] = v[i];
        v[i] = t;
        (*m)++;
        heapify(v, i, 0, c, m);
    }
}

//  MAIN  
int main() {

    Carte original[MAX];
    int n = citireCarti(original);
    if (n == 0) return 0;

    int opt;
    do {
            printf("\nOptiuni:\n");
        printf("1. Bubble Sort (dupa id)\n");
        printf("2. Insertion Sort (dupa id)\n");
        printf("3. Selection Sort (dupa id)\n");
        printf("4. Quick Sort (dupa id)\n");
        printf("5. Shell Sort (dupa id)\n");
        printf("6. Heap Sort (dupa id)\n");
        printf("7. Afisare fisier original\n");
        printf("0. Iesire\n");
        printf("Optiune: ");
        scanf("%d", &opt);

        Carte v[MAX];
        copiaza(v, original, n);

        unsigned long long c = 0, m = 0;

        switch (opt) {
            case 1: bubbleSort(v,n,&c,&m); break;
            case 2: insertionSort(v,n,&c,&m); break;
            case 3: selectionSort(v,n,&c,&m); break;
            case 4: quickSort(v,n,&c,&m); break;
            case 5: shellSort(v,n,&c,&m); break;
            case 6: heapSort(v,n,&c,&m); break;
            case 7: afisare(original,n); continue;
            case 0: break;
            default: printf("Optiune invalida!\n"); continue;
        }

        if (opt >=1 && opt <=6) {
            printf("\nRezultat sortare:\n");
            afisare(v,n);
            printf("\nComparatii: %llu\n", c);
            printf("Mutari/Permutari: %llu\n", m);
        }

    } while (opt != 0);

    return 0;
}