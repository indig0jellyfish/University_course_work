import java.io.*;
import java.util.Random;

class Meeting {
    int participants; // acces doar codului din acelasi pachet cu clasa, dacă o clasa din alt pachet o mosteneste pe, ea nu va avea acces la acele campuri
    int participantsInfo[];
    static int nrMeeting; 

    Meeting() {
        participants = 5;
        participantsInfo = new int[participants];

        for (int i = 0; i < participants; i++) {
            participantsInfo[i] = 1; // meeting unde toti particip sunt activisti
        }

        nrMeeting++;
    }

    Meeting(int participants, int info[]) {
        this.participants = participants;
        participantsInfo = new int[participants]; // vect cu nr elem primit in constr

        for (int i = 0; i < participants; i++) {
            participantsInfo[i] = info[i];
        }

        nrMeeting++;
    }

    Meeting(Meeting other) {
        this.participants = other.participants;
        this.participantsInfo = new int[participants];

        for (int i = 0; i < participants; i++) {
            this.participantsInfo[i] = other.participantsInfo[i];
        }

        nrMeeting++;
    }

    Meeting(String filename) { // creeaza un obj citind info din txtfile
        try {
            BufferedReader file = new BufferedReader(new FileReader(filename));

            participants = Integer.parseInt(file.readLine()); // transf primii linii in int
            participantsInfo = new int[participants];

            for (int i = 0; i < participants; i++) {
                participantsInfo[i] = Integer.parseInt(file.readLine()); // citim fiecare linie, transf txt in int
            }

            file.close();
            nrMeeting++;

        } catch (IOException e) {
            System.out.println("Error reading file");
        }
    }

    void saveToFile(String filename) { // salveaza info obj in txt file
        try {
            PrintWriter file = new PrintWriter(new FileWriter(filename)); // deschidem fisierul pt scriere

            file.println(participants);

            for (int i = 0; i < participants; i++) {
                file.println(participantsInfo[i]);
            }

            file.close();

        } catch (IOException e) {
            System.out.println("Error writing file");
        }
    }

    void printInfo() { // metoda ce afiseaza la ecran toată informaţia despre meeting
        System.out.println("\nMeeting participants: " + participants);
        System.out.print("Participants information: ");
        
        for (int i = 0; i < participants; i++) {
            System.out.print(" " + participantsInfo[i]);
        }
    }

    public int getParticipants() {
        return participants;
    }

    public void setParticipants(int newParticipants) {
        if (newParticipants > 0 && newParticipants != participants) {
            int tmp[] = new int[participants];

            for (int i = 0; i < participants; i++) {
                tmp[i] = participantsInfo[i];
            }

            participantsInfo = new int[newParticipants];

            int min = (participants < newParticipants) ? participants : newParticipants;

            for (int i = 0; i < min; i++) {
                participantsInfo[i] = tmp[i];
            }

            participants = newParticipants;
        }
    }

    public int getParticipant(int id) {
        if (id >= 0 && id < participants) {
            return participantsInfo[id];
        }

        return -1;
    }

    public void setParticipant(int id, int newParticipant) {
        if (id >= 0 && id < participants && newParticipant >= 0 && newParticipant <= 2) {
            participantsInfo[id] = newParticipant;
        }
    }

    void inputInfo() {
        do {
            System.out.print("Nr of participants: ");
            participants = inInt();
        } while (participants <= 0);

        participantsInfo = new int[participants];

        for (int i = 0; i < participants; i++) {
            do {
                System.out.print("Enter participant " + i + " (0-journalist, 1-activist, 2-policeman): ");
                participantsInfo[i] = inInt();
            } while (participantsInfo[i] < 0 || participantsInfo[i] > 2);
        }
    }

    void randomInfo() {
        Random random = new Random(); // ob ce genereaza valori aleatoare
        participants = random.nextInt(10) + 1;
        participantsInfo = new int[participants];

        for (int i = 0; i < participants; i++) {
            participantsInfo[i] = random.nextInt(3);
        }
    }

    static void compareActivists(Meeting meeting1, Meeting meeting2) { // static pt ca comp 2 ob simultan, nu e o actiune a unui ingur ob
        int activists1 = 0;
        int activists2 = 0;

        for (int i = 0; i < meeting1.participants; i++) {
            if (meeting1.participantsInfo[i] == 1) {
                activists1++;
            }
        }

        for (int i = 0; i < meeting2.participants; i++) {
            if (meeting2.participantsInfo[i] == 1) {
                activists2++;
            }
        }

        if (activists1 > activists2) {
            System.out.println("1st meeting has more activists");
        } else if (activists2 > activists1) {
            System.out.println("2nd meeting has more activists");
        } else {
            System.out.println("Both meetings have the same nr of activists");
        }
    }

    void concatenate(Meeting other) {
        int oldParticipants = participants;
        participants = participants + other.participants;

        int tmp[] = new int[oldParticipants];

        for (int i = 0; i < oldParticipants; i++) {
            tmp[i] = participantsInfo[i];
        }

        participantsInfo = new int[participants];

        for (int i = 0; i < oldParticipants; i++) {
            participantsInfo[i] = tmp[i];
        }

        for (int i = 0; i < other.participants; i++) {
            participantsInfo[oldParticipants + i] = other.participantsInfo[i];
        }

        other.participantsInfo = null;
        other.participants=0;
    }

    static String inString() {
        String str = "";
        BufferedReader box = new BufferedReader(new InputStreamReader(System.in)); // System.in - intrarea de la tast   InputStreamReader - transf datele de intrare intr-un flux de caract   BufferedReader - permite citirea unei linii întregi

        try {
            str = box.readLine(); // citirea per se
        } catch (IOException e) { }

        return str;
    }

    static int inInt() {
        return (Integer.valueOf(inString())).intValue();
    }

    public static void main(String[] args) {
        System.out.println("\nInitial Meetings");
        Meeting A = new Meeting();
        Meeting B = new Meeting(4, new int[]{1, 0, 2, 1});
        Meeting C = new Meeting(B);

        A.printInfo();
        B.printInfo();
        C.printInfo();

        System.out.println("\n\nMeeting D read from the input:");
        Meeting D = new Meeting();
        D.inputInfo();
        D.printInfo();

        System.out.println("\n\nMeeting E with random values:");
        Meeting E = new Meeting();
        E.randomInfo();
        E.printInfo();

        System.out.println("\n\nComparing the nr of activists:");
        Meeting.compareActivists(A, B);

        System.out.println("\nBefore concatenation:");
        A.printInfo();
        B.printInfo();

        A.concatenate(B);

        System.out.println("\nAfter concatenation:");
        A.printInfo();

        Meeting grupa[] = new Meeting[6]; // vect de 6 ref catre obj meeting
        grupa[0] = new Meeting(); // implicit 
        grupa[1] = new Meeting(3, new int[]{1, 0, 2}); // cu parametri
        grupa[2] = new Meeting(grupa[1]); // de copiere
        grupa[3] = new Meeting();
        grupa[4] = new Meeting(5, new int[]{1, 1, 0, 2, 1});
        grupa[5] = new Meeting(grupa[4]);

        for (int i = 0; i < grupa.length; i++) {
            System.out.println();
            grupa[i].printInfo();
        }

        System.out.println("\nCompaing the nr of activists: ");
        Meeting.compareActivists(grupa[1], grupa[4]);

        System.out.println("\nNr of objects created: " + nrMeeting);

        System.out.println("URRRRRRAAAAAA !!!");

        A.saveToFile("C:\\Users\\sevce\\OneDrive\\Documents\\University\\Tehnologii de Programare\\A.txt");
        B.saveToFile("C:\\Users\\sevce\\OneDrive\\Documents\\University\\Tehnologii de Programare\\B.txt");
        C.saveToFile("C:\\Users\\sevce\\OneDrive\\Documents\\University\\Tehnologii de Programare\\C.txt");
        D.saveToFile("C:\\Users\\sevce\\OneDrive\\Documents\\University\\Tehnologii de Programare\\D.txt");
        E.saveToFile("C:\\Users\\sevce\\OneDrive\\Documents\\University\\Tehnologii de Programare\\E.txt");

        for (int i = 0; i < grupa.length; i++) {
            grupa[i].saveToFile(
                "C:\\Users\\sevce\\OneDrive\\Documents\\University\\Tehnologii de Programare\\grupa" + i + ".txt"
            );
        }
    }
}