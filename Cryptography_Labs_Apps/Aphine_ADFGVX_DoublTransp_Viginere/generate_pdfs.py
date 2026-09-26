import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

BASE=os.path.dirname(os.path.abspath(__file__))
DOC=os.path.join(BASE,'docs')

def register_font():
    candidates=[
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf']
    for p in candidates:
        if os.path.exists(p):
            pdfmetrics.registerFont(TTFont('DV',p)); return 'DV'
    return 'Helvetica'

FONT=register_font()

def make_pdf(filename,title,intro,algorithm,steps,attack,example):
    os.makedirs(DOC,exist_ok=True)
    path=os.path.join(DOC,filename)
    styles=getSampleStyleSheet()
    title_s=ParagraphStyle('title',parent=styles['Title'],fontName=FONT,fontSize=18,leading=22)
    h=ParagraphStyle('h',parent=styles['Heading2'],fontName=FONT,fontSize=13,leading=16,spaceBefore=10)
    body=ParagraphStyle('body',parent=styles['BodyText'],fontName=FONT,fontSize=10.5,leading=15)
    code=ParagraphStyle('code',parent=styles['Code'],fontName=FONT,fontSize=8.5,leading=11)
    doc=SimpleDocTemplate(path,pagesize=A4,rightMargin=40,leftMargin=40,topMargin=40,bottomMargin=40)
    story=[Paragraph(title,title_s),Spacer(1,10),Paragraph('<b>Descriere generala</b>',h),Paragraph(intro,body),Paragraph('<b>Algoritmul de criptare/decriptare</b>',h),Paragraph(algorithm,body),Preformatted(steps,code),Paragraph('<b>Testarea rezistentei criptografice</b>',h),Paragraph(attack,body),Paragraph('<b>Exemplu de lucru</b>',h),Preformatted(example,code)]
    doc.build(story)
    return path

def generate_all(out_dir=None):
    global DOC
    if out_dir: DOC=out_dir
    make_pdf('cifrul_afin.pdf','Cifrul Afin (Caesar - caz particular)',
        'Cifrul afin este un cifru cu substitutie monoalfabetica. Fiecare litera a alfabetului este asociata unei valori 0..m-1.',
        'Pentru cheia (a,b), criptarea este E(x)=(a*x+b) mod m, iar decriptarea este D(y)=a^-1*(y-b) mod m. Conditia este gcd(a,m)=1. Caesar este cazul a=1.',
        'CRIPTOGRARE:\n1. Normalizeaza textul.\n2. Converteste fiecare caracter in indice x.\n3. Calculeaza y=(a*x+b) mod m.\n4. Converteste y in caracter.\n\nDECRIPTOGRARE:\n1. Calculeaza inversul modular a^-1.\n2. Pentru fiecare y: x=a^-1*(y-b) mod m.\n3. Converteste x in caracter.',
        'Brute force: pentru toate valorile a relativ prime cu m si toate valorile b, se decripteaza textul. Un scor chi-patrat bazat pe frecventa literelor permite ordonarea candidatilor.',
        'alfabet=abcdefghijklmnopqrstuvwxyz\ntext=attackatdawn\na=5, b=8\nrezultat=izziyqizniae\n\nPentru Caesar: a=1, iar b este deplasarea.' )
    make_pdf('cifrul_vigenere.pdf','Cifrul Vigenere',
        'Vigenere este un cifru cu substitutie polialfabetica. Cheia este repetata pana la lungimea mesajului.',
        'Criptarea: C_i=(P_i+K_i) mod m. Decriptarea: P_i=(C_i-K_i) mod m.',
        'CRIPTOGRARE:\n1. Normalizeaza textul si cheia.\n2. Repeta cheia pe lungimea mesajului.\n3. Pentru fiecare pozitie combina indicii P_i si K_i modulo m.\n4. Converteste rezultatul in litera.\n\nDECRIPTOGRARE:\nSe scade indicele cheii din indicele criptat modulo m.',
        'Atacul statistic poate folosi indicele de coincidenta pentru estimarea lungimii cheii. Pentru fiecare coloana de caractere se aplica analiza chi-patrat pentru a aproxima deplasarea Caesar si a reconstrui cheia.',
        'text=attackatdawn\ncheie=lemon\nC_i=(P_i+K_i) mod 26\nPentru fiecare pozitie se foloseste caracterul corespunzator din LEMONLEMONLE...')
    make_pdf('transpozitie_dubla.pdf','Cifru cu transpozitie dubla pe verticala',
        'Cifrul aplica de doua ori o transpozitie pe coloane. Textul este aranjat in randuri, iar coloanele sunt citite in ordinea alfabetica a cheii.',
        'La criptare se aplica transformarea columnara cu cheia 1, apoi cu cheia 2. La decriptare ordinea este inversata: mai intai se anuleaza cheia 2, apoi cheia 1.',
        'CRIPTOGRARE:\n1. Elimina spatiile si caracterele nepermise.\n2. Umple matricea pe randuri.\n3. Determina ordinea coloanelor dupa cheie.\n4. Citeste coloanele in acea ordine.\n5. Repeta pasii cu a doua cheie.\n\nDECRIPTOGRARE:\nReconstruieste coloanele conform lungimilor lor si citeste matricea pe randuri, mai intai pentru cheia 2 si apoi pentru cheia 1.',
        'Rezistenta poate fi testata prin incercarea mai multor lungimi de chei si permutari pentru mesaje scurte. Frecventa caracterelor nu se schimba, deoarece cifrul doar reordoneaza caracterele; de aceea analiza de n-grame este mai utila.',
        'text=WEAREDISCOVEREDFLEEATONCE\ncheie1=CARGO\ncheie2=LAB\nPas 1: columnar_encrypt(text,CARGO)\nPas 2: columnar_encrypt(rezultat,LAB)')
    make_pdf('cifrul_adfgvx.pdf','Cifrul mixt ADFGVX',
        'ADFGVX combina substitutia printr-un patrat 6x6 cu o transpozitie pe coloane. Alfabetul implementat include a-z si cifrele 0-9.',
        'Se construieste un alfabet cheiat de 36 caractere si se asociaza fiecare caracter unei perechi din A,D,F,G,V,X. Dupa substitutie, sirul de simboluri este transpus pe coloane cu o a doua cheie.',
        'CRIPTOGRARE:\n1. Construieste alfabetul cheiat.\n2. Pentru fiecare caracter gaseste pozitia sa in patratul 6x6.\n3. Inlocuieste pozitia cu doua simboluri ADFGVX.\n4. Scrie sirul rezultat in tabelul transpozitiei si citeste coloanele dupa cheie.\n\nDECRIPTOGRARE:\n1. Reconstruieste matricea de transpozitie.\n2. Recupereaza sirul ADFGVX.\n3. Grupeaza simbolurile cate doua.\n4. Foloseste patratul invers pentru a obtine caracterele originale.',
        'Rezistenta este mai buna decat la o substitutie simpla deoarece frecventele sunt mascate de substitutie si ordinea lor este amestecata de transpozitie. Pentru atac se pot combina cautarea cheilor si analiza de n-grame.',
        'simboluri= A D F G V X\npatrat=6x6 (a-z + 0-9, alfabet cheiat)\ntext=attackatdawn\n1) substitutie -> sir ADFGVX\n2) transpozitie -> text criptat final')

if __name__=='__main__':
    print(generate_all(DOC))
