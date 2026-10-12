import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Random;
import java.util.Scanner;

// INTERFETE
interface Fighter {
    int getCombatRating();
    String fight(MarvelCharacter target);
}

interface CosmicBeing {
    String useCosmicPower();
    int getCosmicLevel();
}

// CLASA DE BAZA ABSTRACTA
abstract class MarvelCharacter {

    public static final String UNIVERSE = "Marvel Cinematic Universe"; // asociata MarvelCharacter, nu cate una pt fiecare ob
    protected static final Random random = new Random(); // clasele copil pot avea acces la ele
    protected static final Scanner scanner = new Scanner(System.in);

    private static int totalCreated;
    private static final String[] STATUSES = {"hero", "villain", "antihero"};
    private static final String[] NAMES = {"Nick Fury", "Maria Hill", "Wong", "Nebula", "Valkyrie"};

    private String name;
    private double power;
    private int health;
    private int age;
    private String status;

    public MarvelCharacter() {
        totalCreated++;
        randomize();
    }

    public MarvelCharacter(String name, double power, int health, int age, String status) {
        totalCreated++;
        this.name = name;
        setPower(power);
        setHealth(health);
        this.age = age;
        this.status = status;
    }

    protected void randomize() {
        name = NAMES[random.nextInt(NAMES.length)];
        power = Math.round(random.nextDouble() * 1000) / 10.0; 
        health = 50 + random.nextInt(151); 
        age = 18 + random.nextInt(200); 
        status = STATUSES[random.nextInt(STATUSES.length)];
    }

    // metoda abstracta, fiecare copil isi defin propriul signatureMove(), polimorfism
    public abstract String signatureMove();

    // input
    public void inputData() {
        setName(readLine("Name: "));
        
        double p;
        do {
            p = readDouble("Power (0-100): ");
        } while (p < 0 || p > 100);
        setPower(p);

        int h;
        do {
            h = readInt("Health (0-500): ");
        } while (h < 0 || h > 500);
        setHealth(h);

        int a;
        do {
            a = readInt("Age (0-5000): ");
        } while (a < 0 || a > 5000);
        setAge(a);

        String s;
        do {
            s = readLine("Status (hero / villain / antihero): ");
        } while (!s.equals("hero") && !s.equals("villain") && !s.equals("antihero"));
        setStatus(s);
    }

    protected static String readLine(String prompt) {
        System.out.print(prompt);
        return scanner.nextLine().trim();
    }

    protected static int readInt(String prompt) {
        while (true) {
            try {
                return Integer.parseInt(readLine(prompt)); // transforma in int
            } catch (NumberFormatException e) {
                System.out.println("Invalid integer, try again");
            }
        }
    }

    protected static double readDouble(String prompt) {
        while (true) {
            try {
                return Double.parseDouble(readLine(prompt));
            } catch (NumberFormatException e) {
                System.out.println("Invalid number, try again");
            }
        }
    }

    
    public void writeToFile(PrintWriter pw) {
        pw.print(getClass().getName() + ";" + name + ";" + power + ";" + health + ";" + age + ";" + status);
    }

    public void print() {
        System.out.printf("[%s] %s | power=%.1f | health=%d | age=%d | status=%s%n", getClass().getName(), name, power, health, age, status);
    }

    // -metoda finala
    public final String getUniverse() {
        return UNIVERSE;
    }
    // metoda statica
    public static int getTotalCreated() {
        return totalCreated;
    }

    // getters / setters
    public String getName() { return name; }
    public double getPower() { return power; }
    public int getHealth() { return health; }
    public int getAge() { return age; }
    public String getStatus() { return status; }
    
    public void setName(String name) {
        this.name = name;
    }
    public void setPower(double power) {
        this.power = Math.max(0, Math.min(100, power));
    }
    public void setHealth(int health) { // in cazul in care la fight se face dmg mai mare decat helth, si iese cu health in neg, se seteaza health la 0
        this.health = Math.max(0, health);
    }
    public void setAge(int age) {
        this.age = age;
    }
    public void setStatus(String status) {
        this.status = status;
    }
    public boolean isAlive() {
        return health > 0;
    }
}

// AVENGER
class Avenger extends MarvelCharacter implements Fighter {
    private static final String[] AVENGERS = {"Steve Rogers", "Natasha Romanoff", "Thor", "Bruce Banner", "Clint Barton", "Wanda Maximoff"};
    private static final String[] SUITS = {"Mark LXXXV Armor", "Vibranium Shield Suit", "Stealth Suit", "Asgardian Armor", "Quantum Suit"};

    private String suit;
    private int missionsCompleted;

    public Avenger() {
        super(); // apeleaza constr clasei parinte
    }

    public Avenger(String name, double power, int health, int age, String status, String suit, int missionsCompleted) {
        super(name, power, health, age, status);
        this.suit = suit;
        this.missionsCompleted = missionsCompleted;
    }

    @Override // redefinirea unei metode din clasa parinte / interfata
    protected void randomize() {
        super.randomize();
        setName(AVENGERS[random.nextInt(AVENGERS.length)]);
        setStatus("hero");
        suit = SUITS[random.nextInt(SUITS.length)];
        missionsCompleted = random.nextInt(60);
    }

    @Override
    public String signatureMove() {
        return getName() + " shouts: \"Avengers, assemble!\"";
    }

    @Override
    public void inputData() {
        super.inputData();
        suit = readLine("Suit: ");

        int m;
        do {
            m = readInt("Missions completed (0-1000): ");
        } while (m < 0 || m > 1000);
        missionsCompleted = m;
    }

    @Override
    public void writeToFile(PrintWriter pw) {
        super.writeToFile(pw);
        pw.print(";" + suit + ";" + missionsCompleted);
    }

    @Override
    public void print() {
        super.print();
        System.out.printf("    suit=%s | missions=%d%n", suit, missionsCompleted);
    }

    // Fighter
    @Override
    public int getCombatRating() {
        return ((int) getPower()) + missionsCompleted;
    }
    @Override
    public String fight(MarvelCharacter target) {
        if (!isAlive()) {
            return getName() + " is dead and cannot fight.";
        }
        int damage = getCombatRating() / 2;
        target.setHealth(target.getHealth() - damage);
        return getName() + " hits " + target.getName() + " for " + damage + " damage.";
    }

    // metode unice
    public void completeMission() {
        missionsCompleted++;
    }

    public String saveTheDay(int threatLevel) {
        if (!isAlive()) {
            return getName() + " is dead and cannot fight.";
        }
        if (getCombatRating() >= threatLevel) {
            completeMission();
            return getName() + " in the " + suit + " defeats a threat of level " + threatLevel + "!";
        }
        setHealth(getHealth() - threatLevel / 4);
        return getName() + " is overwhelmed by a threat of level " + threatLevel + "...";
    }

    public static String teamMotto() {   // static method
        return "Earth's Mightiest Heroes!";
    }
}

// GUARDIAN
class Guardian extends MarvelCharacter implements Fighter, CosmicBeing {
    private static final String[] GUARDIANS = {"Gamora", "Drax", "Rocket", "Groot", "Mantis"};
    private static final String[] WEAPONS = {"Element Guns", "Godslayer Blade", "Twin Knives", "Quad Blasters", "Vine Whip", "Empathic Touch"};

    private String weapon; 
    private int unitsOwed;

    public Guardian() {
        super();
    }

    public Guardian(String name, double power, int health, int age, String status, String weapon, int unitsOwed) {
        super(name, power, health, age, status);
        this.weapon = weapon;
        this.unitsOwed = unitsOwed;
    }

    @Override
    protected void randomize() {
        super.randomize();
        setName(GUARDIANS[random.nextInt(GUARDIANS.length)]);
        setStatus(random.nextBoolean() ? "hero" : "antihero");
        weapon = WEAPONS[random.nextInt(WEAPONS.length)];
        unitsOwed = random.nextInt(100000);
    }

    @Override
    public String signatureMove() {
        return getName() + " grabs the " + weapon + " and cries: \"We are the Guardians of the Galaxy!\"";
    }

    @Override
    public void inputData() {
        super.inputData();
        weapon = readLine("Weapon: ");
        int u;
        do {
            u = readInt("Units owed (0-100000): ");
        } while (u < 0 || u > 100000);
        unitsOwed = u;
    }

    @Override
    public void writeToFile(PrintWriter pw) {
        super.writeToFile(pw);
        pw.print(";" + weapon + ";" + unitsOwed);
    }

    @Override
    public void print() {
        super.print();
        System.out.printf("    weapon=%s | unitsOwed=%d%n", weapon, unitsOwed);
    }

    // Fighter
    @Override
    public int getCombatRating() {
        return ((int) getPower()) + 10;
    }
    @Override
    public String fight(MarvelCharacter target) {
        if (!isAlive()) {
            return getName() + " is dead and cannot fight.";
        }
        int damage = getCombatRating() / 2;
        target.setHealth(target.getHealth() - damage);
        return getName() + " fires the " + weapon + " at " + target.getName() + " for " + damage + " damage.";
    }

    // CosmicBeing
    @Override
    public String useCosmicPower() {
        return getName() + " channels cosmic energy through the " + weapon + "!";
    }
    @Override
    public int getCosmicLevel() {
        return ((int) getPower()) / 2;
    }

    // unique methods
    public String playMixtape() {
        return getName() + " puts on Awesome Mix and starts dancing.";
    }

    public void payUnits(int amount) {
        unitsOwed = Math.max(0, unitsOwed - amount);
    }
}

// VILLAIN
class Villain extends MarvelCharacter implements Fighter {
    private static final String[] VILLAINS = {"Ultron", "Hela", "Killmonger", "Red Skull", "Ronan", "Ego"};
    private static final String[] PLANS = {"Conquer New York", "Wipe out humanity", "Rule Asgard", "Overthrow Wakanda", "Collect the Tesseract"};

    private int evilLevel;  
    private String masterPlan; 

    public Villain() {
        super();
    }

    public Villain(String name, double power, int health, int age, String status, int evilLevel, String masterPlan) {
        super(name, power, health, age, status);
        this.evilLevel = evilLevel;
        this.masterPlan = masterPlan;
    }

    @Override
    protected void randomize() {
        super.randomize();
        setName(VILLAINS[random.nextInt(VILLAINS.length)]);
        setStatus("villain");
        evilLevel = 10 + random.nextInt(91);
        masterPlan = PLANS[random.nextInt(PLANS.length)];
    }

    @Override
    public String signatureMove() {
        return getName() + " laughs: \"I am burdened with glorious purpose.\"";
    }

    @Override
    public void inputData() {
        super.inputData();
        int e;
        do {
            e = readInt("Evil level (0-100): ");
        } while (e < 0 || e > 100);
        evilLevel = e;
        masterPlan = readLine("Master plan: ");
    }

    @Override
    public void writeToFile(PrintWriter pw) {
        super.writeToFile(pw);
        pw.print(";" + evilLevel + ";" + masterPlan);
    }

    @Override
    public void print() {
        super.print();
        System.out.printf("    evilLevel=%d | masterPlan=%s%n", evilLevel, masterPlan);
    }

    // Fighter
    @Override
    public int getCombatRating() {
        return ((int) getPower()) + evilLevel;
    }
    @Override
    public String fight(MarvelCharacter target) {
        if (!isAlive()) {
            return getName() + " is dead and cannot fight.";
        }
        int damage = getCombatRating() / 2;
        target.setHealth(target.getHealth() - damage);
        return getName() + " strikes " + target.getName() + " for " + damage + " damage.";
    }

    // unique methods
    public String executePlan() {
        return getName() + " executes the plan: " + masterPlan + " (evil level " + evilLevel + ")";
    }
    public void corrupt(MarvelCharacter target) {
        target.setStatus("villain");
    }

    public int getEvilLevel() { return evilLevel; }
    public String getMasterPlan() { return masterPlan; }
}

// THANOS clasa finala
final class Thanos extends Villain implements CosmicBeing {
    private int infinityStones; 
    private boolean gauntletEquipped;

    public Thanos() {
        super();
    }

    public Thanos(String name, double power, int health, int age, String status, int evilLevel, String masterPlan, int infinityStones, boolean gauntletEquipped) {
        super(name, power, health, age, status, evilLevel, masterPlan);
        this.infinityStones = Math.max(0, Math.min(6, infinityStones));
        this.gauntletEquipped = gauntletEquipped;
    }

    @Override
    protected void randomize() {
        super.randomize();
        setName("Thanos");
        setPower(90 + random.nextInt(11));
        setStatus("villain");
        infinityStones = 1 + random.nextInt(6);
        gauntletEquipped = random.nextBoolean();
    }

    @Override
    public String signatureMove() {
        return "Thanos: \"I am inevitable.\"";
    }

    @Override
    public void inputData() {
        super.inputData();
        int i;
        do {
            i = readInt("Infinity Stones (0-6): ");
        } while (i < 0 || i > 6);
        infinityStones = i;
        gauntletEquipped = readLine("Gauntlet equipped (yes/no): ").equalsIgnoreCase("yes");
    }

    @Override
    public void writeToFile(PrintWriter pw) {
        super.writeToFile(pw);
        pw.print(";" + infinityStones + ";" + gauntletEquipped);
    }

    @Override
    public void print() {
        super.print();
        System.out.printf("    infinityStones=%d | gauntlet=%b%n", infinityStones, gauntletEquipped);
    }

    @Override
    public int getCombatRating() {
        return super.getCombatRating() + infinityStones * 50;
    }

    // CosmicBeing
    @Override
    public String useCosmicPower() {
        return "Thanos wields " + infinityStones + " Infinity Stone(s)!";
    }
    @Override
    public int getCosmicLevel() {
        return infinityStones * 15 + (gauntletEquipped ? 10 : 0);
    }

    // unique methods
    public void collectStone() {
        if (infinityStones < 6) {
            infinityStones++;
        }
    }

    public void equipGauntlet() {
        gauntletEquipped = true;
    }

    public int snap(MarvelCharacter[] universe) { // roster
        if (infinityStones < 6 || !gauntletEquipped) {
            System.out.println("Thanos cannot snap yet (needs 6 stones + gauntlet).");
            return 0;
        }
        int dusted = 0;
        for (MarvelCharacter c : universe) {
            if (c != this && c.isAlive() && random.nextBoolean()) {
                c.setHealth(0);
                dusted++;
            }
        }
        return dusted;
    }
}

// MAIN 
public class Main {

    // static method
    static void duel(Fighter a, Fighter b) {
        if (!(a instanceof MarvelCharacter) || !(b instanceof MarvelCharacter)) {
            return;
        }
        MarvelCharacter ca = (MarvelCharacter) a; // conversia tipului obj, deoarece initial e fighter, si noi vrem sa il tratam drept mc
        MarvelCharacter cb = (MarvelCharacter) b;
        if (!ca.isAlive() || !cb.isAlive()) {
            System.out.println("DUEL cancelled: one of the fighters is dead.");
            return;
        }
        System.out.println("DUEL: " + ca.getName() + " vs " + cb.getName());
        System.out.println("  " + a.fight(cb));
        if (cb.isAlive()) {
            System.out.println("  " + b.fight(ca));
        }
        System.out.println("  Result: " + ca.getName() + " HP=" + ca.getHealth() + ", " + cb.getName() + " HP=" + cb.getHealth());
    }

    public static void main(String[] args) {
        System.out.println(MarvelCharacter.UNIVERSE);

        String answer = MarvelCharacter.readLine("Enter data for one Avenger from the keyboard? (y/n): ");
        Avenger second = new Avenger();
        if (answer.equalsIgnoreCase("y")) {
            second.inputData();
        }

        MarvelCharacter[] roster = new MarvelCharacter[7];
        roster[0] = new Avenger("Tony Stark", 85.5, 120, 53, "hero", "Mark LXXXV Armor", 40);
        roster[1] = second;
        roster[2] = new Guardian("Peter Quill", 70.0, 110, 38, "hero", "Element Guns", 12000);
        roster[3] = new Guardian();
        roster[4] = new Villain("Loki", 75.0, 100, 1050, "villain", 60, "Rule Asgard");
        roster[5] = new Villain();
        roster[6] = new Thanos("Thanos", 98.0, 400, 1000, "villain", 100, "Balance the universe", 6, true);

        int fCount = 0, cCount = 0; // arr interfata
        for (MarvelCharacter c : roster) {
            if (c instanceof Fighter) fCount++;
            if (c instanceof CosmicBeing) cCount++;
        }
        Fighter[] fighters = new Fighter[fCount]; // vectori tip interfata
        CosmicBeing[] cosmics = new CosmicBeing[cCount];
        int fi = 0, ci = 0;
        for (MarvelCharacter c : roster) {
            if (c instanceof Fighter) fighters[fi++] = (Fighter) c;
            if (c instanceof CosmicBeing) cosmics[ci++] = (CosmicBeing) c;
        }

        // Print all objects + call unique methods (instanceof + casting)
        System.out.println("\nROSTER");
        for (MarvelCharacter c : roster) {
            System.out.println();
            c.print();
            System.out.println("  Move: " + c.signatureMove());
            System.out.println("  Universe: " + c.getUniverse());

            if (c instanceof Thanos) {
                Thanos t = (Thanos) c;
                t.collectStone();
                System.out.println("  " + t.useCosmicPower());
                System.out.println("  " + t.executePlan());
            } else if (c instanceof Villain) {
                Villain v = (Villain) c;
                System.out.println("  " + v.executePlan());
            } else if (c instanceof Avenger) {
                Avenger a = (Avenger) c;
                System.out.println("  " + a.saveTheDay(60));
            } else if (c instanceof Guardian) {
                Guardian g = (Guardian) c;
                g.payUnits(500);
                System.out.println("  " + g.playMixtape());
            }
        }


        System.out.println("\n--- COSMIC BEINGS ---"); // interf arr
        for (CosmicBeing cb : cosmics) {
            System.out.println(cb.useCosmicPower() + " (cosmic level " + cb.getCosmicLevel() + ")");
        }
        System.out.println("\n--- FIGHTERS ---");
        for (Fighter f : fighters) {
            System.out.println(((MarvelCharacter) f).getName() + " rating: " + f.getCombatRating());
        }

        System.out.println("\n--- DUELS ---");
        duel(fighters[0], fighters[4]);
        duel(fighters[2], fighters[6]);

        System.out.println("\n" + Avenger.teamMotto());

        System.out.println("\n--- UNIQUE METHODS ---");
        ((Villain) roster[4]).corrupt(roster[0]);
        System.out.println(roster[0].getName() + " status: " + roster[0].getStatus());
        ((Avenger) roster[0]).completeMission();
        ((Thanos) roster[6]).equipGauntlet();
        System.out.println("Evil level of Loki: " + ((Villain) roster[4]).getEvilLevel());
        
        // The Snap
        System.out.println("\n--- THE SNAP ---");
        int dusted = ((Thanos) roster[6]).snap(roster);
        System.out.println(dusted + " living characters turned to dust.");
        for (MarvelCharacter c : roster) {
            System.out.println("  " + c.getName() + (c.isAlive() ? " survived." : " ... turned to dust."));
        }

        // Write to file
        try (PrintWriter pw = new PrintWriter(new FileWriter("C:\\Users\\sevce\\OneDrive\\Documents\\University\\Tehnologii de Programare\\characters.txt"))) {
            for (MarvelCharacter c : roster) {
                c.writeToFile(pw);
                pw.println();
            }
            System.out.println("\nSaved to characters.txt");
        } catch (IOException e) {
            System.out.println("File error: " + e.getMessage());
        }

        System.out.println("Total characters created: " + MarvelCharacter.getTotalCreated());
    }
}