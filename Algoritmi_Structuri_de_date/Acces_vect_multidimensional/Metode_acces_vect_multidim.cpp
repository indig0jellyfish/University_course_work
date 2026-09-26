#include <iostream>
#include <vector>
#include <iomanip>

using namespace std;

class MasivB {
private:
    int r0, r1, c0, c1; 
    int rows, cols;    

    vector<int> direct;
    vector<int> definitorLinii;
    vector<int> definitorColoane;
    int** iliffe;

    bool valid(int i, int j) const {
        return i >= r0 && i <= r1 && j >= c0 && j <= c1;
    }

    int indexDirect(int i, int j) const {
        return (i - r0) * cols + (j - c0);
    }

    int indexPeLinii(int i, int j) const {
        return (i - r0) * cols + (j - c0);
    }

    int indexPeColoane(int i, int j) const {
        return (j - c0) * rows + (i - r0);
    }

public:
    MasivB(int startRow, int endRow, int startCol, int endCol)
        : r0(startRow), r1(endRow), c0(startCol), c1(endCol) {

        rows = r1 - r0 + 1;
        cols = c1 - c0 + 1;

        direct.resize(rows * cols, 0);
        definitorLinii.resize(rows * cols, 0);
        definitorColoane.resize(rows * cols, 0);

        iliffe = new int*[rows];
        for (int i = 0; i < rows; i++) {
            iliffe[i] = new int[cols];
            for (int j = 0; j < cols; j++) {
                iliffe[i][j] = 0;
            }
        }
    }

    ~MasivB() {
        for (int i = 0; i < rows; i++) {
            delete[] iliffe[i];
        }
        delete[] iliffe;
    }

    // SET
    void setDirect(int i, int j, int value) {
        if (valid(i, j))
            direct[indexDirect(i, j)] = value;
    }

    void setDefinitorLinii(int i, int j, int value) {
        if (valid(i, j))
            definitorLinii[indexPeLinii(i, j)] = value;
    }

    void setDefinitorColoane(int i, int j, int value) {
        if (valid(i, j))
            definitorColoane[indexPeColoane(i, j)] = value;
    }

    void setIliffe(int i, int j, int value) {
        if (valid(i, j))
            iliffe[i - r0][j - c0] = value;
    }

    // GET
    int getDirect(int i, int j) const {
        return direct[indexDirect(i, j)];
    }

    int getDefinitorLinii(int i, int j) const {
        return definitorLinii[indexPeLinii(i, j)];
    }

    int getDefinitorColoane(int i, int j) const {
        return definitorColoane[indexPeColoane(i, j)];
    }

    int getIliffe(int i, int j) const {
        return iliffe[i - r0][j - c0];
    }

    // AFISARE MATRICE
    void afisareDirect() const {
        cout << "Acces direct:\n";
        for (int i = r0; i <= r1; i++) {
            for (int j = c0; j <= c1; j++) {
                cout << setw(4) << getDirect(i, j);
            }
            cout << '\n';
        }
        cout << '\n';
    }

    void afisareDefinitorLinii() const {
        cout << "Definitor pe linii:\n";
        for (int i = r0; i <= r1; i++) {
            for (int j = c0; j <= c1; j++) {
                cout << setw(4) << getDefinitorLinii(i, j);
            }
            cout << '\n';
        }
        cout << '\n';
    }

    void afisareDefinitorColoane() const {
        cout << "Definitor pe coloane:\n";
        for (int i = r0; i <= r1; i++) {
            for (int j = c0; j <= c1; j++) {
                cout << setw(4) << getDefinitorColoane(i, j);
            }
            cout << '\n';
        }
        cout << '\n';
    }

    void afisareIliffe() const {
        cout << "Iliffe:\n";
        for (int i = r0; i <= r1; i++) {
            for (int j = c0; j <= c1; j++) {
                cout << setw(4) << getIliffe(i, j);
            }
            cout << '\n';
        }
        cout << '\n';
    }

    void afisareVectoriInterni() const {
        cout << "=== STRUCTURA IN MEMORIE ===\n\n";

        cout << "1) Direct (row-major):\n";
        for (int x : direct) cout << x << " ";
        cout << "\n\n";

        cout << "2) Definitor linii (row-major):\n";
        for (int x : definitorLinii) cout << x << " ";
        cout << "\n\n";

        cout << "3) Definitor coloane (column-major):\n";
        for (int x : definitorColoane) cout << x << " ";
        cout << "\n\n";

        cout << "4) Iliffe (linii separate):\n";
        for (int i = 0; i < rows; i++) {
            cout << "Linia " << i << ": ";
            for (int j = 0; j < cols; j++)
                cout << iliffe[i][j] << " ";
            cout << '\n';
        }
        cout << "\n";
    }

    void afisareIndexare() const {
        cout << "=== INDEXARE ===\n\n";

        for (int i = r0; i <= r1; i++) {
            for (int j = c0; j <= c1; j++) {
                cout << "(" << i << "," << j << ") -> "
                     << "Direct: " << indexDirect(i,j)
                     << ", Coloane: " << indexPeColoane(i,j)
                     << '\n';
            }
        }
        cout << "\n";
    }

    void afisareAdreseIliffe() const {
        cout << "=== ADRESE ILIFEE ===\n";
        for (int i = 0; i < rows; i++) {
            cout << "Linia " << i << " la adresa: " << iliffe[i] << '\n';
        }
        cout << "\n";
    }

    void comparareMemorie() const {
        size_t memDirect = rows * cols * sizeof(int);
        size_t memDef = rows * cols * sizeof(int) + 2 * sizeof(int);
        size_t memIliffe = rows * sizeof(int*) + rows * cols * sizeof(int);

        cout << "=== MEMORIE ===\n";
        cout << "Direct: " << memDirect << " bytes\n";
        cout << "Definitor (linii/coloane): " << memDef << " bytes\n";
        cout << "Iliffe: " << memIliffe << " bytes\n\n";
    }
};

int main() {
    MasivB B(1, 3, 1, 4);

    for (int i = 1; i <= 3; i++) {
        for (int j = 1; j <= 4; j++) {
            int value = i * 10 + j;

            B.setDirect(i, j, value);
            B.setDefinitorLinii(i, j, value);
            B.setDefinitorColoane(i, j, value);
            B.setIliffe(i, j, value);
        }
    }

    B.afisareDirect();
    B.afisareDefinitorLinii();
    B.afisareDefinitorColoane();
    B.afisareIliffe();
    B.afisareVectoriInterni();
    B.afisareIndexare();
    B.afisareAdreseIliffe();
    B.comparareMemorie();

    return 0;
}