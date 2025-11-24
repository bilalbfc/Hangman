import random, json
from colorama import init, Fore, Style, Back
import unittest
from unittest.mock import patch
from adamAsmaca import Hangman, CountError
import string
import os

testCount = 1000

# Test sınıfı
class TestHangman(unittest.TestCase):
    # Her test metodundan önce çalışır.
    def setUp(self):
        # time.sleep fonksiyonunu geçici olarak değiştirip None döndürmesini sağlıyoruz
        self.sleep_pather = patch("time.sleep", return_value=None)
        self.sleep_pather.start()

        self.os_pather = patch("os.system", return_value=None)
        self.os_pather.start()

        self.hangman = Hangman()
        self.hangman._Hangman__bonus = 0
        self.hangman._Hangman__score = 0
        self.hangman._Hangman__gamerName = 0
        self.hangman._Hangman__errorCount = 6
        self.hangman._Hangman__correctGuessedLetters = set()
        self.hangman._Hangman__selectedWord = ""
        self.hangman._Hangman__gamerName = ""

        self.hangman._Hangman__categories = {
            "hayvanlar": ("köpek", "kedi", "at", "kuş", "fil","aslan","kaplan","balık","tilki","zürafa","kelebek","karga","leylek","kartal"),
            "meyveler": ("elma", "armut", "kiraz", "üzüm", "şeftali","nar","mandalina","kivi","portakal","limon","muz","erik","vişne","kayısı"),
            "teknolojiler": ("telefon","bilgisayar","tablet","kamera","internet","bluetooth","modem","klavye","fare","kulaklık")
        }
        self.hangman._Hangman__displayWord = []

    # Her test metodundan sonra çalışır. time.sleep fonksiyonunun normal işlevine dönmesini sağlar.
    def tearDown(self):
        self.sleep_pather.stop()
        self.os_pather.stop()
        if os.path.exists("scores.json"):
            os.remove("scores.json")

    
    # 1. Test: Harf Doğru mu?

    def test_letterGuessingCorrect(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        self.hangman.letterGuessing("e")
        self.assertEqual(self.hangman._Hangman__score, 10)
        self.assertIn("e", self.hangman._Hangman__correctGuessedLetters)
        self.assertEqual(self.hangman._Hangman__displayWord, ["e", "_", "_","_"])

        print()

    # 2. Test: Harf Yanlış mı?

    def test_letterGuessingIncorrect(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        self.hangman.letterGuessing("i") # elma kelimesinin içinde "i" yokk
        self.assertEqual(self.hangman._Hangman__errorCount,5)
        self.assertEqual(self.hangman._Hangman__score, -5)
        self.assertIn("i",self.hangman._Hangman__wrongGuessedLetters)

        print()

    # 3. Test: Harfin uzunluğu 1 mi?

    def test_letterGuessingIncorrectLength(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        with self.assertRaises(CountError):
            self.hangman.letterGuessing("qwerty") #Birden fazla harf girişi

        print()
    
    # 4. Test: Kelime Doğru mu?
    
    def test_wordGuessingCorrect(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        self.hangman.wordGuessing("elma")
        self.assertEqual(self.hangman._Hangman__score, 40)
        self.assertEqual(self.hangman._Hangman__correctGuessedLetters, set(["e", "l", "m", "a"]))
        self.assertEqual(self.hangman._Hangman__displayWord, ["elma"])
        print()

    # 5. Test: Kelime Yanlış mı?

    def test_wordGuessingIncorrect(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        self.hangman.wordGuessing("uzum")
        self.assertEqual(self.hangman._Hangman__errorCount, 6)
        self.assertEqual(self.hangman._Hangman__score, -5) #0-5'ten -5 olur ben burada hata yapmıştım düzelttim

        print()

    # 6. Test: Kelime istenilen uzunlukta mı?

    def test_wordGuessingIncorrectLength(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        with self.assertRaises(CountError):
            self.hangman.wordGuessing("karpuz")
        print()

    # 7. Test: Küçük Büyük Harff Duyarlılıığı

    def test_letterGuessingSensivity(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        self.hangman.letterGuessing("E")
        self.assertEqual(self.hangman._Hangman__errorCount,5) # Error sayısı azaldı
        self.assertIn("E",self.hangman._Hangman__wrongGuessedLetters) #E'yi yanlış tahöin edilen harflere at
        print("'E' harfi kelimede bulunmuyor(duyarlılık sonucu)")
        print()

    # 8. Test: Puanlama Sistemi

    def test_wordGuessingPointSystem(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        self.hangman.letterGuessing("l") #'l' harfi kelimemizde bulunuyor score+=10
        self.hangman.wordGuessing("elma") #score 10'du. score+=30 yeni score ->40
        self.assertEqual(self.hangman._Hangman__score,40)
        self.assertEqual(self.hangman._Hangman__correctGuessedLetters, set(["e", "l", "m", "a"]))
        print()

    # 9. Test:  Kaybetme olayı

    def test_loseGame(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        for letters in ["q","w","x","ç","z","ğ"]: #Burada 6 harfi yazmamızın nedeni errorCount 6 olması bu harfler kelimede bulunmamalı
            self.hangman.letterGuessing(letters)
        self.assertEqual(self.hangman._Hangman__errorCount,0)
        self.assertTrue(self.hangman.isWinOrLose())
        print()

    # 10. Test: Kazanma Olayı

    def test_winGame(self):
        self.hangman._Hangman__selectedWord = "elma"
        self.hangman._Hangman__displayWord = ["_", "_", "_", "_"]
        for letters in ["e","l","m","a"]:
            self.hangman.letterGuessing(letters)
        self.assertEqual(self.hangman._Hangman__score,40)
        self.assertTrue(self.hangman.isWinOrLose())
        print()

    # 11. Test İpucu Sistemi

    def test_getTip(self):
        self.hangman._Hangman__bonus = 1

        self.hangman.getHint() 
        self.assertEqual(self.hangman._Hangman__bonus,0)

        self.assertTrue(self.hangman._Hangman__hintTaken)

        self.hangman.getHint()
        self.assertEqual(self.hangman._Hangman__bonus, 0)
        print()

    # __GetNumbers TESTİ
    # 12. Test: Geçerli sayılar
    def test_getNumbersValid(self):
        for i in range(testCount):
            correctNumber = random.uniform(-100000, 100000)
            with patch("builtins.input", return_value=str(correctNumber)):
                result = self.hangman._Hangman__getNumbers()
                self.assertEqual(result, correctNumber)

    # 13. Test: Geçersiz sayılar
    def test_getNumbersInvalid(self):
        for i in range(testCount):
            characters = string.ascii_letters + string.punctuation
            lenght = random.randint(0, 40)
            randomWord = ''.join(random.choices(characters, k=lenght))
            with patch("builtins.input", side_effect=[randomWord, "123.2"]):
                result = self.hangman._Hangman__getNumbers()
                self.assertEqual(result, 123.2)
    # ---------------------------------------------------------------------------- #

    # __CheckTheOperation TESTİ
    # 14. Test: Doğru sayı girilmesi
    def test_checkTheOperationCorrect(self):
        for i in range(testCount):
            correctAnswer = random.uniform(-100000, 100000)
            with patch("builtins.input", return_value=str(correctAnswer)):
                userAnswer = float(input("sayı"))
                self.hangman._Hangman__checkTheOperation(correctAnswer, userAnswer)
                self.assertEqual(self.hangman._Hangman__bonus, i + 1)
                self.assertEqual(self.hangman._Hangman__score, (i + 1) * 15)

    # 15. Test: Yanlış sayı girilmesi
    def test_checkTheOperationIncorrect(self):
        for i in range(testCount):
            correctAnswer = random.uniform(-100000, 100000)
            incorrectAnswer = random.uniform(-100000, 100000)
            if (incorrectAnswer == correctAnswer): incorrectAnswer += 1
            self.hangman._Hangman__checkTheOperation(correctAnswer, incorrectAnswer)
            self.assertEqual(self.hangman._Hangman__errorCount, 6 - (i + 1))
            self.assertEqual(self.hangman._Hangman__score, (i + 1) * -10)
    # ---------------------------------------------------------------------------- #

    # __calculate TESTİ
    # 16. Test: sonuç doğru bir şekilde mi çıkıyor
    def test_calculateValidValue(self):
        operators = ["+", "-", "*", "/"]
        for i in range(testCount):
            operator = random.choice(operators)
            randomNumber1 = random.uniform(-1000, 1000)
            randomNumber2 = random.uniform(-1000, 1000)
            if (operator == "/" and randomNumber2 == 0): randomNumber2 += 1
            match (operator):
                case "+": result = randomNumber1 + randomNumber2
                case "-": result = randomNumber1 - randomNumber2
                case "*": result = randomNumber1 * randomNumber2
                case "/": result = randomNumber1 / randomNumber2

            with patch("builtins.input", side_effect=[str(randomNumber1), str(randomNumber2), str(result)]):
                correctAnswer, answer = self.hangman._Hangman__calculate(operator)
                self.assertAlmostEqual(correctAnswer, result)
                self.assertAlmostEqual(answer, result)

    # 17. Test: 0'a bölünememe testi
    def test_calculateZeroDivision(self):
        for i in range(10):
            randomNumber = random.uniform(-1000, 1000)
            with patch("builtins.input", side_effect=[str(randomNumber), "0"]):
                self.assertIsNone(self.hangman._Hangman__calculate("/"))

    # 18. Test: Üyeler doğru bir şekilde değişiyor mu
    def test_calculateAttributesUpdateProperly(self):
        for i in range(testCount):
            randomNumber = random.uniform(-1000, 1000)
            with patch("builtins.input", side_effect=[str(randomNumber), "0"]):
                self.hangman._Hangman__calculate("/")
                self.assertEqual(self.hangman._Hangman__errorCount, 6 - (i + 1))
                self.assertEqual(self.hangman._Hangman__score, (i + 1) * -10)
    # ------------------------------------------------------------------------ #

    # calculator TESTİ
    # 19. Test: Yanlış işlem Seçimi yapma
    def test_calculatorInvalidOperation(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        for i in range(testCount):
            length = random.randint(0, 20)
            randomWord = ''.join(random.choices(characters, k=length))
            with patch("builtins.input", side_effect=[randomWord, "iptal"]):
                result = self.hangman.calculator()
                self.assertIsNone(result)

    # 20. Test: Doğru işlem seçimi
    def test_calculatorCorrectOperation(self):
        operations = ["toplama", "çıkarma", "çarpma", "bölme"]
        for i in range(testCount):
            operation = random.choice(operations)

            randomNumber = random.uniform(-10000, 10000)
            with patch.object(Hangman, "_Hangman__calculate", return_value=(randomNumber, randomNumber)):
                with patch("builtins.input", return_value=operation):
                    self.assertIsNone(self.hangman.calculator())
    # ---------------------------------------------------------------------------- #

    # setGamerName TESTİ
    # 21. Test: Geçerli isim girilmesi
    def test_setGamerNameValid(self):
        for i in range(testCount):
            characters = string.ascii_letters + string.digits + string.punctuation
            length = random.randint(3, 20)
            randomName = ''.join(random.choices(characters, k=length))
            self.hangman.setGamerName(randomName)
            self.assertEqual(randomName, self.hangman._Hangman__gamerName)
    
    # 22. Test: Yanlış uzunlukta isim girilmesi
    def test_setGamerNameInvalidLength(self):
        for i in range(testCount):
            characters = string.ascii_letters + string.digits + string.punctuation
            if (random.random() < 0.50): length = random.randint(0, 2)
            else: length = random.randint(21, 100)
            randomName = ''.join(random.choices(characters, k=length))

            with self.assertRaises(CountError):
                self.hangman.setGamerName(randomName)

    # 23. Test: Başa veya sona boşluk eklenmesi
    def test_setGamerNameInvalidName(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        length = random.randint(3, 20)
        randomName = ''.join(random.choices(characters, k=length))
        if random.random(): (randomName + length * " ")
        else: ((length * " ") + randomName)
        self.hangman.setGamerName(randomName)
        self.assertEqual(randomName.strip(), self.hangman._Hangman__gamerName)
    # # ---------------------------------------------------------------------------- #

    # openRandomLetter TESTİ
    # 24. Test: Harfleri kelimeye yerleştiriyor mu
    def test_openRandomLetterAddToMember(self):
        for category in self.hangman._Hangman__categories:
            for member in category:
                self.hangman._Hangman__selectedWord = member
                letters = set()
                self.hangman._Hangman__displayWord = ["_"] * len(member)
                for i in range(len(set(member))):
                    self.hangman.openRandomLetter()

                    # Yeni açılan harfi bul
                    letter = next(char for char in self.hangman._Hangman__displayWord if char != "_" and char not in letters)
                    letters.add(letter)

                    # Bu harfin doğru konumlarda açıldığını kontrol et
                    for j in range(len(member)):
                        if (member[j] == letter): self.assertEqual(member[j], self.hangman._Hangman__displayWord[j])
                        
                self.assertEqual("".join(self.hangman._Hangman__displayWord), member)
    
    # 25. Test: Kelime sınırı aşılması
    def test_openRandomLetterInvalidLength(self):
        for category in self.hangman._Hangman__categories:
            for member in category:
                self.hangman._Hangman__selectedWord = member
                self.hangman._Hangman__displayWord = ["_"] * len(member)

                # Kelimede ki tüm farklı harfleri aç     
                for i in range(len(set(member))):
                    self.hangman.openRandomLetter()
                # Kelimede tüm harfler açılınca tekrar metot çalışınca None dönmesi kontrolü
                result = self.hangman.openRandomLetter()
                self.assertIsNone(result)
    # ---------------------------------------------------------------------------- #
  
    # writeToFile TESTİ
    # 26. Test: içinde bilgiler olan bir dosyanın içine sıralı bir şekilde eleman ekeyebiliyor mu
    def test_writeToFileAppendItem(self):
        self.hangman._Hangman__gamerName = "Ahmet"
        self.hangman._Hangman__score = 60
        gamer = {"Ahmet": 60}
        dicts = [{"Ahmet": 45, "Mehmet": 100, "Canan": 21, "Ali": 93},
                {"Ayşe": 120, "Ahmet": 140, "Murat": 110},
                {"Ajda": 10, "Kerim": 45, "Tuğkan": 1}]
        
        for index in range(len(dicts)):
            # sırayla dicts listesinden dictleri score dosyasına yzdırıyoruz
            with open("scores.json", "w", encoding="utf-8") as file:
                json.dump(dicts[index], file, ensure_ascii=False, indent=4)
            self.hangman.writeToFile()

            with open("scores.json", "r", encoding="utf-8") as file:
                score = json.load(file)
                dicts[index]["Ahmet"] = max(gamer["Ahmet"], dicts[index].get("Ahmet", 0))
                sortedDicts = dict(sorted(dicts[index].items(), key=lambda item: item[1], reverse=True))
            # liste sıralanmıp doğru bir şekilde yerleştirilmiş mi diye bakıyoruz
            self.assertEqual(list(score.items()), list(sortedDicts.items()))

    # writeScores TESTİ
    # 27. Test: Bir dosyayı sıralayabiliyor mu
    def test_writeScoresIsSort(self):
        dicts = [{"Ahmet": 45, "Mehmet": 100, "Canan": 21, "Ali": 93, "Murat": 25, "Kıvanç": 0, "Bilal": 16},
                {"Ayşe": 120, "Ahmet": 140, "Murat": 110},
                {"Ajda": 10, "Kerim": 45, "Tuğkan": 1, "Pelin": 160, "Banu": 89}]
        
        for index in range(len(dicts)):
            # sırayla dicts listesinden dictleri score dosyasına yzdırıyoruz
            with open("scores.json", "w", encoding="utf-8") as file:
                json.dump(dicts[index], file, ensure_ascii=False, indent=4)
            self.hangman.writeScores()

            with open("scores.json", "r", encoding="utf-8") as file:
                score = json.load(file)
                sortedDicts = dict(sorted(dicts[index].items(), key=lambda item: item[1], reverse=True))

                self.assertEqual(list(score.items()), list(sortedDicts.items()))

    # 28. Test: Boş dosya gelirse
    def test_writeScoresEmptyFile(self):
        with open("scores.json", "w", encoding="utf-8") as file:
            json.dump({}, file, ensure_ascii=False, indent=4)
        self.assertIsNone(self.hangman.writeScores())

    # __checkFile TESTİ
    # 29. Test: Yanlış Formatta dosya
    def test_checkFile(self):
        wrongFormats = ['{"ahmet": 45', 'mehmet: 23', '{"kamuran" 54}', '{"İsmeT": "faruk"}']

        for wrongFormat in wrongFormats:
            with open("scores.json", "w", encoding="utf-8") as file:
                json.dump(wrongFormat, file, ensure_ascii=False, indent=4)
            self.hangman._Hangman__checkFile()
            with open("scores.json", "r", encoding="utf-8") as file:
                scores = json.load(file)
            self.assertEqual(scores, {})

    # 30. Test: Yanlış tipte yazılmış dosya
    def test_checkFileInvalidType(self):
        dataTypes = ["Merhaba", " mehmeT  ", [1, "TR"], ("merhaba", 43), 21]
        for i in dataTypes:
            with open("scores.json", "w", encoding="utf-8") as file:
                json.dump(i, file, ensure_ascii=False, indent=4)
            self.hangman._Hangman__checkFile()
            with open("scores.json", "r", encoding="utf-8") as file:
                score = json.load(file)
                self.assertEqual(score, {})

    # 31. Test: Dosya olmama durumu
    def test_checkFileFileNotFound(self):
        self.hangman._Hangman__checkFile()
        self.assertTrue(os.path.exists("scores.json"))

    # 32. Test: value'nun sayı olmaması
    def test_checkFileValueIsNotNumber(self):
        dicts = [{"Ahmet": "12"}, {"Ayşe": list((1,2))}, {"Mahmut": {"Murat": 48}}]
        for member in dicts:
            with open("scores.json", "w", encoding="utf-8") as file:
                json.dump(member, file, ensure_ascii=False, indent=4)
            self.hangman._Hangman__checkFile()
            with open("scores.json", "r", encoding="utf-8") as file:
                scores = json.load(file)
                self.assertEqual(scores, {})
                


if __name__ == "__main__":
    unittest.main()