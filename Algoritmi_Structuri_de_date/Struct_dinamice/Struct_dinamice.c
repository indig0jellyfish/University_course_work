#include <stdio.h>
#include <stdlib.h>

#define MAX 200

int citireFisier(int v[]) {
    FILE *f = fopen("Lista_neordonata.txt", "r");
    if (!f) {
        printf("Eroare fisier!\n");
        return 0;
    }

    int n = 0;
    char linie[300];

    while (fgets(linie, sizeof(linie), f) && n < MAX) {
        sscanf(linie, "%d.", &v[n]);  // extrage DOAR ID-ul
        n++;
    }

    fclose(f);
    return n;
}

// LISTA SIMPLA
typedef struct Nod {
    int val;
    struct Nod *next;
} Nod;

Nod* insLS(Nod *h, int x) {
    Nod *n = (Nod*)malloc(sizeof(Nod));
    n->val = x;
    n->next = NULL;

    if (!h) return n;

    Nod *p = h;
    while (p->next) p = p->next;
    p->next = n;
    return h;
}

void afisLS(Nod *h) {
    while (h) {
        printf("%d ", h->val);
        h = h->next;
    }
    printf("\n");
}

Nod* cautLS(Nod *h, int x) {
    while (h) {
        if (h->val == x) return h;
        h = h->next;
    }
    return NULL;
}

Nod* stergLS(Nod *h, int x) {
    Nod *p = h, *prev = NULL;
    while (p) {
        if (p->val == x) {
            if (prev) prev->next = p->next;
            else h = p->next;
            free(p);
            return h;
        }
        prev = p;
        p = p->next;
    }
    return h;
}

// LISTA DUBLA
typedef struct NodD {
    int val;
    struct NodD *next, *prev;
} NodD;

NodD* insLD(NodD *h, int x) {
    NodD *n = (NodD*)malloc(sizeof(NodD));
    n->val = x;
    n->next = NULL;
    n->prev = NULL;

    if (!h) return n;

    NodD *p = h;
    while (p->next) p = p->next;
    p->next = n;
    n->prev = p;
    return h;
}

void afisLD(NodD *h) {
    while (h) {
        printf("%d ", h->val);
        h = h->next;
    }
    printf("\n");
}

NodD* cautLD(NodD *h, int x) {
    while (h) {
        if (h->val == x) return h;
        h = h->next;
    }
    return NULL;
}

NodD* stergLD(NodD *h, int x) {
    NodD *p = h;
    while (p && p->val != x) p = p->next;
    if (!p) return h;

    if (p->prev) p->prev->next = p->next;
    else h = p->next;

    if (p->next) p->next->prev = p->prev;

    free(p);
    return h;
}

// LISTA CIRCULARA
typedef struct NodC {
    int val;
    struct NodC *next;
} NodC;

NodC* insLC(NodC *h, int x) {
    NodC *n = (NodC*)malloc(sizeof(NodC));
    n->val = x;

    if (!h) {
        n->next = n;
        return n;
    }

    NodC *p = h;
    while (p->next != h) p = p->next;
    p->next = n;
    n->next = h;
    return h;
}

void afisLC(NodC *h) {
    if (!h) {
        printf("\n");
        return;
    }

    NodC *p = h;
    do {
        printf("%d ", p->val);
        p = p->next;
    } while (p != h);
    printf("\n");
}

NodC* cautLC(NodC *h, int x) {
    if (!h) return NULL;

    NodC *p = h;
    do {
        if (p->val == x) return p;
        p = p->next;
    } while (p != h);

    return NULL;
}

NodC* stergLC(NodC *h, int x) {
    if (!h) return NULL;

    NodC *p = h, *prev = NULL;

    do {
        if (p->val == x) {
            if (p->next == p) {
                free(p);
                return NULL;
            }

            if (p == h) {
                NodC *tail = h;
                while (tail->next != h) tail = tail->next;
                h = h->next;
                tail->next = h;
            } else {
                prev->next = p->next;
            }

            free(p);
            return h;
        }

        prev = p;
        p = p->next;
    } while (p != h);

    return h;
}

// STIVA
typedef struct {
    int a[MAX];
    int top;
} Stiva;

void initS(Stiva *s) {
    s->top = -1;
}

void push(Stiva *s, int x) {
    if (s->top < MAX - 1) s->a[++s->top] = x;
}

void pop(Stiva *s) {
    if (s->top >= 0) s->top--;
}

void afisS(Stiva s) {
    for (int i = s.top; i >= 0; i--)
        printf("%d ", s.a[i]);
    printf("\n");
}

// COADA
typedef struct {
    int a[MAX];
    int front, rear;
} Coada;

void initQ(Coada *q) {
    q->front = 0;
    q->rear = -1;
}

void enqueue(Coada *q, int x) {
    if (q->rear < MAX - 1) q->a[++q->rear] = x;
}

void dequeue(Coada *q) {
    if (q->front <= q->rear) q->front++;
}

void afisQ(Coada q) {
    for (int i = q.front; i <= q.rear; i++)
        printf("%d ", q.a[i]);
    printf("\n");
}

// ARBORE BINAR DE CAUTARE
typedef struct NodA {
    int val;
    struct NodA *st, *dr;
} NodA;

NodA* insA(NodA *r, int x) {
    if (!r) {
        NodA *n = (NodA*)malloc(sizeof(NodA));
        n->val = x;
        n->st = n->dr = NULL;
        return n;
    }

    if (x < r->val) r->st = insA(r->st, x);
    else r->dr = insA(r->dr, x);

    return r;
}

NodA* cautA(NodA *r, int x) {
    if (!r || r->val == x) return r;
    if (x < r->val) return cautA(r->st, x);
    return cautA(r->dr, x);
}

NodA* minim(NodA *r) {
    while (r && r->st) r = r->st;
    return r;
}

NodA* stergA(NodA *r, int x) {
    if (!r) return NULL;

    if (x < r->val) r->st = stergA(r->st, x);
    else if (x > r->val) r->dr = stergA(r->dr, x);
    else {
        if (!r->st) {
            NodA *t = r->dr;
            free(r);
            return t;
        }
        if (!r->dr) {
            NodA *t = r->st;
            free(r);
            return t;
        }

        NodA *t = minim(r->dr);
        r->val = t->val;
        r->dr = stergA(r->dr, t->val);
    }

    return r;
}

void inordine(NodA *r) {
    if (r) {
        inordine(r->st);
        printf("%d ", r->val);
        inordine(r->dr);
    }
}

void preordine(NodA *r) {
    if (r) {
        printf("%d ", r->val);
        preordine(r->st);
        preordine(r->dr);
    }
}

void postordine(NodA *r) {
    if (r) {
        postordine(r->st);
        postordine(r->dr);
        printf("%d ", r->val);
    }
}

// MENIURI
void meniuLS(Nod **h) {
    int op, x;
    do {
        printf("\nLista simpla: 1-afis 2-ins 3-caut 4-sterg 0-inapoi\n");
        scanf("%d", &op);
        if (op == 1) afisLS(*h);
        else if (op == 2) { scanf("%d", &x); *h = insLS(*h, x); }
        else if (op == 3) { scanf("%d", &x); printf(cautLS(*h, x) ? "Gasit\n" : "Nu exista\n"); }
        else if (op == 4) { scanf("%d", &x); *h = stergLS(*h, x); }
    } while (op != 0);
}

void meniuLD(NodD **h) {
    int op, x;
    do {
        printf("\nLista dubla: 1-afis 2-ins 3-caut 4-sterg 0-inapoi\n");
        scanf("%d", &op);
        if (op == 1) afisLD(*h);
        else if (op == 2) { scanf("%d", &x); *h = insLD(*h, x); }
        else if (op == 3) { scanf("%d", &x); printf(cautLD(*h, x) ? "Gasit\n" : "Nu exista\n"); }
        else if (op == 4) { scanf("%d", &x); *h = stergLD(*h, x); }
    } while (op != 0);
}

void meniuLC(NodC **h) {
    int op, x;
    do {
        printf("\nLista circulara: 1-afis 2-ins 3-caut 4-sterg 0-inapoi\n");
        scanf("%d", &op);
        if (op == 1) afisLC(*h);
        else if (op == 2) { scanf("%d", &x); *h = insLC(*h, x); }
        else if (op == 3) { scanf("%d", &x); printf(cautLC(*h, x) ? "Gasit\n" : "Nu exista\n"); }
        else if (op == 4) { scanf("%d", &x); *h = stergLC(*h, x); }
    } while (op != 0);
}

void meniuStiva(Stiva *s) {
    int op, x;
    do {
        printf("\nStiva: 1-afis 2-push 3-pop 0-inapoi\n");
        scanf("%d", &op);
        if (op == 1) afisS(*s);
        else if (op == 2) { scanf("%d", &x); push(s, x); }
        else if (op == 3) pop(s);
    } while (op != 0);
}

void meniuCoada(Coada *q) {
    int op, x;
    do {
        printf("\nCoada: 1-afis 2-enqueue 3-dequeue 0-inapoi\n");
        scanf("%d", &op);
        if (op == 1) afisQ(*q);
        else if (op == 2) { scanf("%d", &x); enqueue(q, x); }
        else if (op == 3) dequeue(q);
    } while (op != 0);
}

void meniuArb(NodA **r) {
    int op, x;
    do {
        printf("\nArbore: 1-inordine 2-preordine 3-postordine 4-ins 5-caut 6-sterg 0-inapoi\n");
        scanf("%d", &op);
        if (op == 1) { inordine(*r); printf("\n"); }
        else if (op == 2) { preordine(*r); printf("\n"); }
        else if (op == 3) { postordine(*r); printf("\n"); }
        else if (op == 4) { scanf("%d", &x); *r = insA(*r, x); }
        else if (op == 5) { scanf("%d", &x); printf(cautA(*r, x) ? "Gasit\n" : "Nu exista\n"); }
        else if (op == 6) { scanf("%d", &x); *r = stergA(*r, x); }
    } while (op != 0);
}

// MAIN
int main() {
    Nod *ls = NULL;
    NodD *ld = NULL;
    NodC *lc = NULL;
    Stiva s;
    Coada q;
    NodA *arb = NULL;

    initS(&s);
    initQ(&q);

    int valori[MAX];
    int n = citireFisier(valori);

    for (int i = 0; i < n; i++) {
        ls = insLS(ls, valori[i]);
        ld = insLD(ld, valori[i]);
        lc = insLC(lc, valori[i]);
        push(&s, valori[i]);
        enqueue(&q, valori[i]);
        arb = insA(arb, valori[i]);
    }

    int op;
    do {
        printf("\n MENIU PRINCIPAL \n");
        printf("1. Lista simpla\n");
        printf("2. Lista dubla\n");
        printf("3. Lista circulara\n");
        printf("4. Stiva\n");
        printf("5. Coada\n");
        printf("6. Arbore\n");
        printf("0. Iesire\n");
        scanf("%d", &op);

        if (op == 1) meniuLS(&ls);
        else if (op == 2) meniuLD(&ld);
        else if (op == 3) meniuLC(&lc);
        else if (op == 4) meniuStiva(&s);
        else if (op == 5) meniuCoada(&q);
        else if (op == 6) meniuArb(&arb);

    } while (op != 0);

    return 0;
}