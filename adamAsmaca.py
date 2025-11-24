import os, json, random, time
from colorama import init, Fore, Back, Style

# colorama'yı başlat (Windows'ta renklerin çalışması için gerekli)
init(autoreset=True)

# --- RENK STİLLERİ ---
COLOR_HEADER = Fore.CYAN + Style.BRIGHT  # Başlıklar için
COLOR_SUCCESS = Fore.GREEN + Style.BRIGHT  # Başarılı işlemler için
COLOR_ERROR = Fore.RED + Style.BRIGHT  # Hata ve yanlış tahminler için
COLOR_WARNING = Fore.YELLOW  # Uyarılar için
COLOR_BONUS = Fore.MAGENTA + Style.BRIGHT  # Bonuslar için

# Bir exception tanımladık
class CountError(Exception):
    def __init__(self, message=COLOR_WARNING + "Invalid Count"):
        self.message = message
        super().__init__(message)

class Hangman:
    def __init__(self):
        self.__checkFile()

        self.__categories = {
            "hayvanlar": ("köpek", "kedi", "at", "kuş", "fil","aslan","kaplan","balık","tilki","zürafa","kelebek","karga","leylek","kartal"),
            "meyveler": ("elma", "armut", "kiraz", "üzüm", "şeftali","nar","mandalina","kivi","portakal","limon","muz","erik","vişne","kayısı"),
            "teknolojiler": ("telefon","bilgisayar","tablet","kamera","internet","bluetooth","modem","klavye","fare","kulaklık")
        }
            
    #gerekli değişkenleri tanımladım
        self.__errorCount = 6  # yapılan hata sayısı. max hata değişkenini kaldırıp hata sayısını 6 olarak güncelledim
        self.__score = 0   # oyun skorumuz
        self.__bonus = 0   # işlemler sonucu kazanacağımız bonus
        self.__gamerName = "" # oyuncu adı
        self.__hintTaken = False # ipucu alınmış mı. Yeni değişken ekledim

        self.__wrongGuessedLetters = set() # yanlış tahmin edilen harfleri tutmak için 
        self.__correctGuessedLetters = set() # doğru tahmin edilen harfleri tutmak için
        self.__selectedWord = ""     # seçilen kelime (random modülü ile yapacağız)
        self.__selectedCategory = "" # seçilen kategori (random modülü ile yapacağız)
        self.__displayWord = []  # kelimeyi görüntüleme

        #adam asmaca oyununun görselleri
        self.__hangmanImages = [
            """
             +---+
             O   |
            /|\\  |
            / \\  |
                ===
            """,
            """
             +---+
             O   |
            /|\\  |
            /    |
                ===
            """,
            """
             +---+
             O   |
            /|\\  |
                 |
                ===
            """,
            """
             +---+
             O   |
            /|   |
                 |
                ===
            """, 
            """
             +---+
             O   |
             |   |
                 |
                ===
            """,
            """
             +---+
             O   |
                 |
                 |
                ===
            """,                                
            """
             +---+
                 |
                 |
                 |
                ===
            """
        ]

    # Rastgele kategori ve rastgele kelime seçilecek. seçilen kelime ve seçilen kategori değişkenine atanacak.
    def selectedRandomWord(self) -> None:
        categoryName = random.choice(list(self.__categories.keys()))
        self.__selectedCategory = categoryName

        wordList = self.__categories[categoryName]
        selectedWord = random.choice(wordList).lower() 
        self.__selectedWord = selectedWord

        self.__displayWord = ["_"] * len(selectedWord) # seçilen kelimenin harf sayısı kadar "_" çiz
        #Yeni oyun öncesi sıfırlama
        self.__hintTaken = False
        self.__errorCount = 6
        self.__wrongGuessedLetters = set()
        self.__correctGuessedLetters = set()
        self.__bonus = 0
        self.__score = 0
    
    # Dışarıdan bir harf alacak. Kelimenin içinde var mı diye kontrol edecek. Kelimenin içinde varsa harfi yerine veya yerlerine koyacak.
    def letterGuessing(self, letter:str) -> None:
        # eğer değişken str değilse hata fırlatır
        if(letter.isdigit()):
            raise ValueError(COLOR_WARNING + "Invalid value!")
        # eğer değişkenin uzunluğu 1'den farklı ise hata fırlatır
        elif(len(letter) != 1):
            raise CountError()

        # girilen harf önceden tahmin edilmişse bu blok çalışır
        if(letter in self.__correctGuessedLetters or letter in self.__wrongGuessedLetters):
            os.system("cls")
            print(f"'{letter}' bu harf önceden tahmin ettiğiniz harfler arasında bulunuyor!")
            return
        # girilen harf kelimede bulunuyorsa bu blok çalışır
        if((letter in self.__selectedWord)):
            self.__score += 10
            self.__correctGuessedLetters.add(letter)

            indexes = [i for i, char in enumerate(self.__selectedWord) if char == letter]   
            for i in indexes:
                self.__displayWord[i] = self.__selectedWord[i]
            os.system("cls")
            print(COLOR_SUCCESS + "Tebrikler 🎊")
            print(f"'{letter}' harfi kelimenin içinde bulunuyor!")
            return
        # girilen harf kelimenin içinde yoksa bu blok çalışır
        else:
            self.__errorCount -= 1
            self.__score -= 5
            self.__wrongGuessedLetters.add(letter)
            os.system("cls")
            print(f"Yanlış harf '{letter}' | Kalan hata hakkı: {self.__errorCount}")
            return
            
    # Kelime tahmin etme
    def wordGuessing(self, word:str) -> None:
        if(word.isdigit()):
            raise ValueError(COLOR_WARNING + "Invalid value!")
        if(len(word) != len(self.__selectedWord)):
            raise CountError(COLOR_WARNING + f"Kelime {len(self.__selectedWord)} harfli olmalıdır!")

        if(word == self.__selectedWord):
            self.__displayWord.clear()
            self.__displayWord = self.__selectedWord.split()
            letters = set(word)
            for letter in letters:
                if (letter not in self.__correctGuessedLetters):
                    self.__score += 10
                    self.__correctGuessedLetters.add(letter)

        else:
            self.__score -= 5
            os.system("cls")
            print(COLOR_ERROR + "Yanlış tahmin!")
            print(f"Kelime:", end=" ")
            print(COLOR_ERROR + word, end=" ")
            print("değil!")

    # doğru tahmin sonrası rastgele bir harfi kelimede aç
    def openRandomLetter(self) -> str:
        closedIndexes = [i for i, char in enumerate(self.__displayWord) if char == "_"]

        if not closedIndexes: # kapalı indeks kalmadıysa işlem yapma
            return None
        #bir harf açılana kadar döngü sürsün
        while True:
            randomIndex = random.choice(range(len(self.__selectedWord)))
            if self.__displayWord[randomIndex] == "_":
                openLetter = self.__selectedWord[randomIndex]
                #harf doğruysa o harfin kelimede bulunduğu tüm indekslerde o harf gösterilir
                for i , char in enumerate(self.__selectedWord):
                    if char == openLetter:
                        self.__displayWord[i] = char
                        # açılmış harfi tahmin edilen harfler listesine ekle
                        self.__correctGuessedLetters.add(char)

                return openLetter

            # eğer "_" kalmadıysa yani tüm harfler bilindiyse döngüyü sonlandır
            if "_" not in self.__displayWord:
                break

    # ---------- Hesap Makinesi ---------- #
    # Hesap makinesi için sayı alma fonksiyonu
    def __getNumbers(self, text:str="Sayıyı giriniz: ") -> float:
        while(True):
            try:
                number = float(input(text))
                return number
            except ValueError:
                print(COLOR_WARNING + "Lütfen geçerli bir değer giriniz!\n")

    # İşlemleri kontrol eden fonksiyon
    def __checkTheOperation(self, correctAnswer:float, answer:float) -> None:
        if(abs((correctAnswer) - answer) <= 1e-6):
            randomLetter = self.openRandomLetter()
            self.__bonus += 1
            self.__score += 15
            print(COLOR_SUCCESS + "Doğru! 🎉")
            print(f"🎁 Bonus: '{randomLetter}' harfi açıldı!")
            print(f"Bonus puanın: {self.__bonus}")
        else:
            self.__score -= 10
            print(COLOR_ERROR + "Yanlış! ⛔")
            print(f"Doğru cevap = {correctAnswer}")
            self.__errorCount -= 1

    # İşlemleri yapan metot
    def __calculate(self, arithmeticOperator:str) -> tuple[float, float] | None:
        text = ". sayı (iptal için 'iptal'): "
        number1, number2 = self.__getNumbers(f"1{text}"), self.__getNumbers(f"2{text}")

        match (arithmeticOperator):
            case "+": correctAnswer = number1 + number2
            case "-": correctAnswer = number1 - number2
            case "*": correctAnswer = number1 * number2
            case "/":
                if(number2 == 0):
                    self.__errorCount -= 1
                    self.__score -= 10
                    print(COLOR_ERROR + "Payda '0' olamaz!\n")
                    return
                else: correctAnswer = number1 / number2

        print(f"{number1} - {number2} = ?")
        answer = self.__getNumbers("Cevabınız: ")
        return correctAnswer, answer

    # Hesap makinesi metodu
    def calculator(self) -> None:
        
        # Matematiksel işlemi kontrol edip doğruluk değerine göre bazı işlemler yapar.
        while(True):
                operation = input("İşlem türü (toplama/çıkarma/çarpma/bölme) ya da 'iptal': ").strip().lower()
                match(operation):
                    case "toplama":
                        correctAnswer, answer = self.__calculate("+")
                        self.__checkTheOperation(correctAnswer, answer)
                        return
                    
                    case "çıkarma":
                        correctAnswer, answer = self.__calculate("-")
                        self.__checkTheOperation(correctAnswer, answer)
                        return
                    
                    case "çarpma":
                        correctAnswer, answer = self.__calculate("*")
                        self.__checkTheOperation(correctAnswer, answer)
                        return
                    
                    case "bölme":
                        correctAnswer, answer = self.__calculate("/")
                        self.__checkTheOperation(correctAnswer, answer)
                        return

                    case "iptal":
                        return
                    # "case _:" c++ switch-case yapısında ki default gibidir
                    case _:
                        os.system("cls")
                        print(COLOR_WARNING + "Lütfen geçerli bir seçim yapınız!\n")
                        time.sleep(1)
                        os.system("cls")
    # ----------------------------------------------------------------------- #
    
    def isWinOrLose(self) -> bool:
        if(self.__errorCount == 0):
            print(COLOR_ERROR + "Kaybettiniz! 💀")
            print(f"Skorunuz: {self.__score}")
            self.writeToFile()
            return True
        
        if(self.__selectedWord == "".join(self.__displayWord)):
            print(COLOR_SUCCESS + "Kazandınız! 🎊🎉🎊🎉")
            print("Kelime:", end="")
            print(Fore.CYAN + self.__selectedWord)
            print(f"Skornunuz: {self.__score}")
            self.writeToFile()
            return True
        return False
    # ----------------------------------------------------------------------- #

    #  ----------  Dosya İşlemleri  ----------  #
    # Bir oyun bitince skorları dosyaya yazdıracak.
    def __checkFile(self) -> None:
        if(not os.path.exists("scores.json")):
            with open("scores.json", "w", encoding="utf-8") as file:
                json.dump({}, file, ensure_ascii=False, indent=4)
            return
        
        try:
            with open("scores.json", "r", encoding="utf-8") as file:
                scores = json.load(file)
                # tip yanlış olursa
                if not isinstance(scores, dict):
                    scores = {}
        except json.JSONDecodeError:
            scores = {}
        
        for gamerName, score in list(scores.items()):
            if not isinstance(score, (int, float)):
                del scores[gamerName]

        with open("scores.json", "w", encoding="utf-8") as file:
                json.dump(scores, file, ensure_ascii=False, indent=4)
            # Eğer score int veya float değilse siliyoruz

    # Skorları dosyaya yazacak
    def writeToFile(self) -> None:
        with open("scores.json", "r", encoding="utf-8") as file:           
            scores = json.load(file)

        # oyuncu yoksa ekler, varsa ve yeni skor büyükse günceller.
        scores[self.__gamerName] = max(self.__score, scores.get(self.__gamerName, 0))

        sortedScores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        
        with open("scores.json", "w", encoding="utf-8") as file:
            json.dump(sortedScores, file, ensure_ascii=False, indent=4)

    # İlk 5 skoru dosyadan alıp ekrana yazdıracak.
    def writeScores(self) -> None:
        with open("scores.json", "r", encoding="utf-8") as file:
            scores = json.load(file)           

        if(not scores):
            print(COLOR_WARNING + "Her hangi bir skor bulunmamaktadır.")
            return
        else:
            sortedScores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
            with open("scores.json", "w", encoding="utf-8") as file:
                    json.dump(sortedScores, file, ensure_ascii=False, indent=4)
            rank = 1
            print(COLOR_HEADER + "OYUNCULAR                SKORLAR")
            for gamerName, score in sortedScores.items():
                print(f"{rank}. {gamerName:<20} | {score:<5}")
                rank += 1   
                if (rank == 6):
                    break
    # ----------------------------------------------------------------------- #

    # ---------- Setter Method ---------- #
    def setGamerName(self, gamerName:str) -> None:
        if(len(gamerName) <= 20 and len(gamerName) > 2):
            self.__gamerName = gamerName.strip()
        else:
            raise CountError(COLOR_WARNING + "İsim [3, 20] aralığında olmalıdır!")

    #  ---------- Getter Methods ----------  #
    # İpucu alma fonksiyonu
    def getHint(self) -> None:
        if(self.__bonus == 0):
            os.system("cls")
            print(COLOR_WARNING + "Bonus puanınız '0'!")
            time.sleep(1)
            os.system("cls")
        elif(not self.__hintTaken):
            self.__bonus -= 1
            self.__hintTaken = True
            print("Kategori:", end=" ")
            print(COLOR_BONUS + self.__selectedCategory)
        else:
            print(f"Kategori: {self.__selectedCategory}")

    # Her hatada adam asılmaya yaklaşacak şekilde model güncellenecek.
    def getHangmanFigure(self) -> str:
        return self.__hangmanImages[self.__errorCount]
        
    # Önceden tahmin edlien harfleri döndürür
    def getGuessedLetters(self) -> str:
        if(not self.__correctGuessedLetters and not self.__wrongGuessedLetters):
            return "-"
        else:
            correctGuessedLetters = set(list(map(lambda x: Fore.GREEN + x + Style.RESET_ALL,self.__correctGuessedLetters)))
            wrongGuessedLetters = set(list(map(lambda x: Fore.RED + x + Style.RESET_ALL,self.__wrongGuessedLetters)))
            letters = wrongGuessedLetters.union(correctGuessedLetters)
            return ", ".join(letters)

    # Bonus puanı döndürür
    def getBonus(self) -> int:
        return self.__bonus
    
    def getScore(self) -> int:
        return self.__score
    
    # sifreli kelimeyi görüntüler
    def getDisplayWord(self) -> str:
        return " ".join(self.__displayWord)
    
# Girilen değerlerin uzunluğu doğru mu veya tip hatası veriyor mu kontrol. obj sınıftan alınan bir metot
def memberValidation(obj, member:str) -> bool:
    try:
        os.system("cls")
        obj(member)
        return True
    except (CountError, ValueError) as e:
        os.system("cls")
        print(e)
        time.sleep(1)
        os.system("cls")
        return False

# Burada oyun oluşturulacak. Bu da sınıf yapıldıktan sonra hazırlanacak.
def main():
    # Nesne oluşturduk
    hangman = Hangman()

    isContinue = True
    isSelectRandomWord = False
    gamerName = ""

    while(True):
        gamerName = input("Oyuncu ismini giriniz: ").strip()
        if(memberValidation(hangman.setGamerName, gamerName)):
            break

    os.system("cls")
    print(COLOR_HEADER + "\n=== Calc & Hang: İşlem Yap, Harfi Kurtar! ===")
    while(isContinue):
        print(Fore.GREEN+ Back.BLACK + Style.BRIGHT + "\n======== ANA MENÜ ========\n")
        print("Seçenekler: [Y]eni Tur | [O]yuncu İsmini Değiştir | [S]korları Yazdır | [Ç]ıkış")
        choice = input("Seçiminiz: ").strip().upper()
        os.system("cls")

        match choice:
            case "Y":
                    hangman.selectedRandomWord()
                    isSelectRandomWord = True
            case "O":
                gamerName = input("Oyuncu ismini giriniz: ").strip()
                memberValidation(hangman.setGamerName, gamerName)
            case "S":
                os.system("cls")
                hangman.writeScores()
                isSelectRandomWord = False
            case "Ç":
                os.system("cls")
                print("Çıkış Yapıldı")
                isContinue = False

            case _:
                os.system("cls")
                print(COLOR_WARNING + "Lütfen geçerli bir ifade giriniz!")
                time.sleep(1)
                os.system("cls")

        while(isSelectRandomWord):
            # Menüyü oluşturduk
            print(COLOR_HEADER + "\n--- Yeni Tur ---\n")
            print(hangman.getHangmanFigure())
            print(f"Kelime: {hangman.getDisplayWord()}")
            print(f"Tahmin edilen harfler: {hangman.getGuessedLetters()}")
            print("Bonus puan:", end=" ")
            print(COLOR_BONUS + str(hangman.getBonus()))
            print(Fore.LIGHTBLUE_EX + "Seçenekler", end="")
            print(": [H]arf tahmini | [K]elime tahmini | [İ]şlem çöz | [I]pucu | [Ç]ıkış")
            choice = input("Seçiminiz: ").strip()

            # Girilen harf küçük 'i' ise büyük 'I'ya dönüştürme sorununu gidermek için
            if(choice == "i"):
                choice = "İ"
            else:
                choice = choice.upper()

            # Seçenekler
            match choice:
                case "H":
                    letter = input("Harf: ").strip()
                    memberValidation(hangman.letterGuessing, letter)
                case "K":
                    word = input("Kelimeyi giriniz: ").strip()
                    memberValidation(hangman.wordGuessing, word)
                case "İ":
                    os.system("cls")
                    hangman.calculator()   
                             
                case "I":
                    os.system("cls")
                    hangman.getHint()
                case "Ç":
                    os.system("cls")
                    print(f"Skorun: {hangman.getScore()}")
                    hangman.writeToFile()
                    break
                case _:
                    os.system("cls")
                    print(COLOR_WARNING + "Lütfen geçerli bir ifade giriniz!\n")
                    time.sleep(1)
                    os.system("cls")
            
            if(hangman.isWinOrLose()):
                break

if __name__ == "__main__":
    main()
