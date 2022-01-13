"""
COMP.CS.100 Ohjelmointi 1 / Programming 1
Eero Hakanen, H291459, eero.v.hakanen@tuni.fi
Gui Project RAVIT-Korttipeli-Juomapeli-KelpoPeli
"""
"""

KÄYTTÖOHJEET
Pelin pelaaminen yleisesti:
Kyseessä siis klassinen juomapeli Ravit. Ohjeet peliin yleisesti ovat
alkuvalmisteluissa pöydälle laitetaan ässät päällekkäin.
kahdeksan korttia asetetaan riviin ja niiden päädyssä on maali.
Loput kortit ovat nosto pakka
Pelin kulku:
1. Pelaajat valitsevat kukin yhden ässän jonka puolesta lyövät vetoa
2. Tämän jälkeen nosto pakasta nostetaan kortteja yksi kerrallaa. Nostetun kortin
maata oleva ässä liikkuu pöydällä eteenpäin kohti maalia.
3. Jos kaikki kortit ohittavat yhden pöydälle riviin asetetuista korteista se käännetään.
Se ässä joka on tämän kortin maata siirtyy askeleen taakse päin.
4. Pelin voittaa se ässä joka ensimmäisenä maalissa.
5. Tämän puolesta vetoa lyöneet saavat jakaa tuplasti oman panoksensa verran hörppyjä

käyttöliittymä:
Sivun ylälaidassa lyhyet ohjeet peliin.
Vasemmalla panostus ohje ja panostaminen:
-Kirjoita ruutuun panosteja, panos ja valittu ässä ja paina Enter
-Tämän jälkeen näytölle tulostuu kirjoitettu teksti ja panostajia voi lisätä
-Panokset saa tyhjennettyä painamalla "Tyhjennä panokset"

Pelin aloittaminen alusta:
Pelin voi keskeyttää ja aloittaa alusta vasemman alalaidan napilla koska tahansa

Kortien nostaminen:
-Käyttöliittymän vasemmassa alalaidassa oleva kortti on nostopakka.
-Klikkaamalla korttia näytölle jaetaan aina uusi kortti ja ässät liikkuvat automaattisesti

Pelin loppu:
-Kun jokin ässä pääsee maaliin tulostuu näytölle ilmoitus voittavasta väristä
-Näytölle tulee myös uusi resetointi nappi
"""

from tkinter import *
from random import choice, randint

# Korttipakan kuvat listattuna maan mukaan
club_files = ['2C.png', '3C.png', '4C.png', '5C.png', '6C.png', '7C.png', '8C.png',
              '9C.png', '10C.png', 'JC.png', 'QC.png', 'KC.png']

spade_files = ['2S.png', '3S.png', '4S.png', '5S.png', '6S.png', '7S.png', '8S.png',
               '9S.png', '10S.png', 'JS.png', 'QS.png', 'KS.png']

heart_files = ['2H.png', '3H.png', '4H.png', '5H.png', '6H.png', '7H.png', '8H.png',
               '9H.png', '10H.png', 'JH.png', 'QH.png', 'KH.png']

diamond_files = ['2D.png', '3D.png', '4D.png', '5D.png', '6D.png', '7D.png', '8D.png',
                 '9D.png', '10D.png', 'JD.png', 'QD.png', 'KD.png']

# Kuvat sanakirjaan maan perusteella
maat = {'RISTI': club_files, 'PATA': spade_files, 'HERTTA': heart_files, 'RUUTU': diamond_files}

# Ässien kuvat sanakirjassa maan mukaan.
ace_files = {'RISTI': 'AC.png', 'PATA': 'AS.png', 'HERTTA': 'AH.png', 'RUUTU': 'AD.png'}


# Käyttöliittymä luokka, koko ohjelma pyörii tämän luokan ympärillä
class Tkinter:
    def __init__(self):
        self.__mainwindow = Tk()
        # Määritellään muuttujat, joita käytetään myöhemmin jo init-funktioon, arvolla "None"
        self.__game_label = None
        self.__confirmation = None
        self.__play_again = None
        self.__panostus_ruutu = None
        self.__panos_label = None
        self.__card_button = None
        self.__empty_button = None
        self.__start_button = None

        # Tulostetaan pelin ohjeet
        self.pelin_ohjeet()

        # Panostus ruutu ja tekstit
        # Listaan tallennetaan käyttäjän syötteet 'self.__panostus_ruutu' muuttujasta
        self.__panostus_tekstit = []
        self.panostus()

        # Maalin tulostus näytölle
        self.goal()

        # Kuvien muokkaus Photoimage muotoon
        # Sanakirjaan tallennetaan kaikki kortit Photoimage muodossa jotta saadaan tehtyä Label osia helposti
        self.__cards = {'RISTI': [], 'PATA': [], 'HERTTA': [], 'RUUTU': []}
        self.card_images()

        # Muuttujilla ace_columns ja columns_passed tarkastetaan ovatko ässät ohittaneet kortin alareunasta
        self.__columns_passed = 1
        self.__ace_columns = []

        # Sanakirjaan tallennetaan ässien Labelit maan perusteella luokiteltuina
        self.__aces = {}
        self.create_aces()
        self.grid_ace()

        # Listan avulla tarkistetaan onko kortti jo jaettu pakasta kun jaetaan random kortti
        self.__cards_used = []

        # Luodaan kortti rivi ala reunaan
        self.__card_back = PhotoImage(file="pictures/blue_back.png")
        self.card_back_grid()

        # Luodaan pelin aloitus nappi ja restart nappi
        self.start_button()
        self.restart_button()

        mainloop()

    def restart_button(self):
        """
        Funtkio luo näytölle napin aloita alusta. Nappi kutsuu funktiota self.confirmation eli
        Nappia painaessa näytölle tulee uusi nappi joka kysyy varmistusta pelin uudelleen aloitukseen
        """
        self.__play_again = Button(text="ALOITA ALUSTA", foreground='red', command=self.confirmation)
        self.__play_again.grid(row=5, column=0, ipady='30')

    def confirmation(self):
        """
        Luo napin joka kysyy varmistusta pelin uudelleen aloitukseen
        Jos nappia klikataan peli resetoituu, kutsutaan self.restart
        """
        self.__confirmation = Button(self.__mainwindow, text='OLETKO VARMA?',
                                     command=self.restart, foreground='white', bg='red')
        self.__confirmation.grid(row=5, column=0, ipady='30', ipadx='0')

    def pelin_ohjeet(self):
        """
        Tulostaa näytölle pelin ohjeet ja panostuksen ohjeet
        """
        pelin_ohje = Label(self.__mainwindow,
                           text='OHJEET:'
                                '\n1. VALITKAA ÄSSÄ'
                                '\n2. ASETTAKAA PANOKSET'
                                '\n3. JUOKAA PUOLET PANOKSESTA'
                                '\n4. LÄHETTÄKÄÄ HEVOSET LIIKKEELLE VASEMMASTA ALAKULMASTA'
                                '\n5. VOITTAJA HEVOSEN VALITSEVAT SAAVAT JAKAA TUPLASTI PANOKSEN VERRAN HÖRPPYJÄ')

        pelin_ohje.grid(row=0, column=2, columnspan=10, sticky='w')
        panostus_ohje = Label(self.__mainwindow, text='KIRJOITA RUUTUUN \n PANOSTAJAN NIMI, VÄRI\n JA PANOS (Enter)')
        panostus_ohje.grid(row=1, column=0)

    def panostus(self):
        """
        Luo panostus ruudun.
        Kun ruutuun kirjoittaessa painaa enter
        kutsutaan funktiota self.panos_teksti,
        parametrina on ruutuun syötetty teksti
        """
        self.__panostus_ruutu = Entry(self.__mainwindow)
        self.__panostus_ruutu.grid(row=1, column=0, sticky='s')
        self.__panostus_ruutu.bind("<Return>", (lambda event: self.panos_teksti(self.__panostus_ruutu.get())))

    def panos_teksti(self, teksti):
        """
        :param teksti: str, panostusruutuun kirjoitettu teksti,
        Jos ruutu on tyhjä funktio ei tee mitään, muutoin
        muokkaa ruudulle uuden panostus tekstin
        """
        if teksti != '':
            self.__panostus_ruutu.delete(0, 'end')
            # Jos ruudulla vanha teksti Label se poistetaan
            if self.__panos_label is not None:
                self.__panos_label.grid_remove()

            # Lisätään ruudun teksti listaan panostus_teksit
            self.__panostus_tekstit.append(teksti)
            # Luodaan uusi self.__panos_label
            self.__panos_label = Label(self.__mainwindow, text="\n".join(self.__panostus_tekstit))
            self.__panos_label.grid(row=2, column=0, rowspan=5, sticky='n')

            # Luodaan panosten tyhjennys nappi, joka kutsuu funktiota empty_panos
            self.__empty_button = Button(self.__mainwindow, text="TYHJENNÄ \nPANANOKSET", foreground='red',
                                         command=self.empty_panos)
            self.__empty_button.grid(row=3, column=0)

    def empty_panos(self):
        """
        Tyhjentää panos_label tekstin näytöltä ja tyhjentää panostus_tekstit- listan
        """
        self.__panostus_tekstit = []
        self.__panos_label.grid_remove()

    def goal(self):
        """
        Tulostaa näytölle maalin, kirjain kerrallaan kirjain eri grid-ruudussa
        """
        row = 1
        for letter in list("MAALI"):
            letter_label = Label(self.__mainwindow, text=letter, font=("Courier", 70), foreground='green')
            letter_label.grid(row=row, column=10)
            row += 1

    def card_images(self):
        """
        Luo jokaisesta kortin kuva tiedostosta
        Photoimagen ja tallentaa sen sanakirjaan maan mukaan
        """
        # maat sanakirjassa kaikien korttien tiedostot maan mukaan
        for maa in maat:
            for picture_file in maat[maa]:
                photoImage = PhotoImage(file=f"pictures/{picture_file}")
                self.__cards[maa].append(photoImage)

    def create_aces(self):
        """
        Luo ässien kuvat niiden aloitus kohdalle vasempaan reunaan
        Tallentaa ässän tiedot sanakirjaan self.__aces
        """
        # Rivi muuttuja ässät riveillä 1-4
        row = 1
        # ace_files sanakirjassa ässien tiedostot maan mukaan
        for maa in ace_files:
            picture_file = ace_files[maa]
            photoImage = PhotoImage(file=f"pictures/{picture_file}")
            ace_label = Label(self.__mainwindow, image=photoImage)
            ace_label.grid(row=row, column=1)
            # Sanakirjaan tallentuu ässän 0.= label objekti, 1. =sen rivi, 2.=sarake ja 3.=photoimage objekti
            self.__aces[maa] = [ace_label, row, 1, photoImage]
            row += 1

    def grid_ace(self):
        """
        Jokaisen ässän paikka gridataan uudestaan
        """
        for ace in self.__aces:
            self.__aces[ace][0].grid_remove()
            self.__aces[ace][0].grid(row=self.__aces[ace][1], column=self.__aces[ace][2])

    def move_ace(self, kortin_maa, amount):
        """
        :param kortin_maa: str, kortin maa joka pakasta tai pöydältä käännetty
        :param amount: int, joko +1 tai -1, tämän mukaan ässä siirtyy eteen tai taakse
        """
        self.__aces[kortin_maa][2] += amount
        # Jos ässä on maalissa, column=10, peli päättyy
        if self.__aces[kortin_maa][2] == 10:
            self.game_over(kortin_maa)

        # Päivitetään missä sarakkeessa ässät ovat nyt

        self.__ace_columns = []
        for maa in self.__aces:
            self.__ace_columns.append(self.__aces[maa][2])

        # Tarkistetaan ovatko kaikki ässät ylittäneet uuden sarakeen
        if all(column > self.__columns_passed for column in self.__ace_columns):
            # Jos ohitettu käännetään pöydällä oleva kortti siitä sarakkeesta
            self.__columns_passed += 1
            self.flip_card()

        # Ässien paikkojen päivitys
        self.grid_ace()

    def random_card(self):
        """
        Valitsee random kortin korttipakasta
        :return random_card: random kortin photoimage objekti
        :return randmon_maa: random kortin maa
        """
        while True:
            # Valitaan random maa self.__cards sanakirjasta, ja sitä vastaava lista kortteja
            random_maa, random_cards = choice(list(self.__cards.items()))
            # Valitaan nyt random maan korttilistasta yksi kortti
            random_card = random_cards[randint(0, 11)]
            # Jos korti pakan kaikkikortit on käytetty tyhjennetään käytettyjen korttien lista
            if len(self.__cards_used) == 4 * 11:
                self.__cards_used = []
            # Jos random kortti käytetyissä korteissa arvotaan uusi kortti
            elif random_card in self.__cards_used:
                continue
            # Muutoin palautetaan random kortin photoimage ja sen maa
            else:
                self.__cards_used.append(random_card)
                return random_card, random_maa

    def card_Labels(self, card, column, row):
        """
        Luo photo imagelle label objektin ja se lisätään näytölle tiettyyn paikkaan
        :param card: photoimage, Kortin josta tehdään label näytölle photoimage objekti
        :param column: int, sarake jonne label tulee
        :param row: int, rivi jonne label tulee
        """
        label = Label(self.__mainwindow, image=card)
        label.grid(row=row, column=column)

    def card_Buttons(self, card):
        """
        Luo vasempaan alakulmaan kortista Button objetkin josta klikkaamalla peli etenee
        kutsuu funktiota self.deal_new
        :param card: photoimage, Kortin josta tehdään label näytölle photoimage objekti
        """
        self.__card_button = Button(self.__mainwindow, image=card, command=self.deal_new)
        self.__card_button.grid(row=5, column=1)

    def card_back_grid(self):
        """
        Luo näytön alareunaan käännetttävien kortien Label-objektit
        """
        for column in range(2, 10):
            card_back_label = Label(self.__mainwindow, image=self.__card_back)
            card_back_label.grid(row=5, column=column)

    def start_button(self):
        """
        Luo pelin alussa korttipakan selkäpuolen napin jota klikkaamalla jaetaan ensimmäinen kortti
        kutsuu funktiota self.deal_new
        """
        self.__start_button = Button(self.__mainwindow, image=self.__card_back, command=self.deal_new)
        self.__start_button.grid(row=5, column=1)

    def deal_new(self):
        """
        Jakaa random kortin vasempaan alareunaan ja siirtää ässiä
        """
        # Kortin määritys
        random_card, random_maa = self.random_card()
        # Ässän sarakkeen päivitys
        self.move_ace(random_maa, 1)
        # Uuden kortin jakaminen
        self.card_Buttons(random_card)

    def flip_card(self):
        """
        Käänttä random kortin alas ja siirtää ässiä
        """
        # Kortin määritys
        random_card, random_maa = self.random_card()
        # Ässän siirto
        self.move_ace(random_maa, -1)
        # Käännetään random kortti alas, self.__columns_passed on sarake
        self.card_Labels(random_card, self.__columns_passed, 5)

    def game_over(self, color):
        """
        Pelin loppu
        :param color: str, maaliin päässeen ässän maa
        """
        # Maaliin päässeen ässän rivi
        row = self.__aces[color][1]
        # Voitto tekstin värin määritys
        if color == 'PATA' or color == 'RISTI':
            text_color = 'black'
        else:
            text_color = 'red'

        # Voitto tekstin label
        self.__game_label = Label(self.__mainwindow, text=f"{color} VOITTAA!",
                                  font=("Courier", 50), foreground=text_color)
        self.__game_label.grid(row=row, column=1, columnspan=8)

        # Aloita alusta nappi
        self.__play_again = Button(text="ALOITA ALUSTA", command=self.restart)
        self.__play_again.grid(row=row, column=8, sticky='w', ipady='30')

    def restart(self):
        """
        Palauttaaa kaiken alkuperäiseen tilanteeseen
        """
        # Objektit joita ei välttämättä ole kun painetaan restart nappia,
        # tarkistetaan ja sitten poistetaan grid-objekti
        if self.__play_again is not None:
            self.__play_again.grid_remove()
        if self.__game_label is not None:
            self.__game_label.grid_remove()
        if self.__confirmation is not None:
            self.__confirmation.grid_remove()
        if self.__panos_label is not None:
            self.__panos_label.grid_remove()


        self.__panostus_tekstit = []
        self.panostus()
        self.goal()

        self.__cards = {'RISTI': [], 'PATA': [], 'HERTTA': [], 'RUUTU': []}
        self.card_images()

        self.__columns_passed = 1
        self.__ace_columns = []
        self.__aces = {}
        self.create_aces()
        self.grid_ace()

        self.__cards_used = []

        self.card_back_grid()
        self.start_button()
        self.restart_button()

if __name__ == '__main__':
    Tkinter()