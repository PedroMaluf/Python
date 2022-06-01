import pickle
import numpy as np
import re
import time

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
punctuation = ('.','?','!')

#Split text into sentences (shared by D Greenberg on Stack Overflow )
def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences

#Input the text in the format of the class Book
def get_word_text(text_path):
    with open(text_path, 'r') as f:
        text = f.read()
        book = Book(text)
        book.read_book()
        book.get_correlated()

    
    return book

#Class with all the information needed
class Book:
    def __init__(self, text):
        self.text = text
        self.chapter_len = () # (mean, std)
        self.chapters = {}   # Index: chapter name, chapter len
        self.paragraphs = {} # Index: value, chapter index, paragraph len, chapter position
        self.sentences = {}  # Index: value, chapter index, paragraph index, sentence len, paragraph position
        self.words = {}      # Index: value, chapter index, paragraph index, sentence index, sentence position
        self.correlated_words = {} #Word: dict correlated words{word: mean_dis, std_dis}        
    
    #Get the basic information for each chapter, paragraph, sentence and word
    def read_book(self):
        aux_chapter = self.text.split('CHAPTER ')       #Split the text into chapters
        current_paragraph = 0
        current_sentence = 0
        current_word = 0
        chapters_size = []

        for current_chapter, chapter in enumerate(aux_chapter):
            aux_paragraphs = chapter.split('\n\n')      #Split each chapter into paragraphs

            for paragraph_in_chapter, paragraph in enumerate(aux_paragraphs):
                if current_chapter == 0:
                    self.book_name = paragraph
                    continue
                elif paragraph_in_chapter == 0:
                    chapter_title = True
                elif chapter_title:
                    chapters_size.append(len(aux_paragraphs))
                    self.chapters[current_chapter] = paragraph, len(aux_paragraphs)
                    chapter_title = False
                else:
                    aux_sentences = split_into_sentences(paragraph)     #Split each paragraph into sentences

                    for sentence_in_paragraph, sentence in enumerate(aux_sentences):
                        aux_words = re.findall(r"[\w']+|[.,!?;~-]", sentence)       #Split each sentence into words, considering punctuation and others as words

                        for word_in_sentence, word in enumerate(aux_words):
                            word = word.lower()

                            #Joining abreviations with '.' as only one word
                            if word in ('mr','mrs','st','ms','dr','inc','ltd','jr','sr','co'):
                                word = ''.join((word, aux_words[word_in_sentence + 1]))
                                del aux_words[word_in_sentence + 1]

                            self.words[current_word] = word, current_chapter, current_paragraph, current_sentence, word_in_sentence/len(aux_words)
                            current_word += 1
                        
                        self.sentences[current_sentence] = sentence, current_chapter, current_paragraph, len(aux_words), sentence_in_paragraph/len(aux_sentences)
                        current_sentence += 1

                    self.paragraphs[current_paragraph] = paragraph, current_chapter, len(aux_sentences), paragraph_in_chapter/len(aux_paragraphs)
                    current_paragraph += 1

        self.chapter_len = (np.mean(chapters_size), np.std(chapters_size))

    #Get mean and std of the distance of words in the same sentence
    def get_correlated(self):
        aux_dict = {}

        #Get all the distances
        for word in self.words:
            correlated_dict = {}
            
            for other_word in range(word + 1, len(self.words)):
                if self.words.get(word)[3] == self.words.get(other_word)[3]:
                    if self.words.get(other_word)[0] not in correlated_dict.keys():
                        correlated_dict[self.words.get(other_word)[0]] = [other_word - word]
                    else:
                        continue
                else:
                    break
                
            if self.words.get(word)[0] not in aux_dict.keys():
                aux_dict[self.words.get(word)[0]] = correlated_dict
            else:
                for correlated_word in correlated_dict.keys():
                    if correlated_word in aux_dict.get(self.words.get(word)[0]):
                        aux_dict.get(self.words.get(word)[0]).get(correlated_word).append(correlated_dict.get(correlated_word)[0])
                    else:
                        aux_dict.get(self.words.get(word)[0])[correlated_word] = correlated_dict.get(correlated_word)

        #Calculating the mean and the std
        for word in self.words:
            aux_correlated_dict = {}
            for correlated in aux_dict.get(self.words.get(word)[0]):
                aux_correlated_dict[correlated] = np.mean(aux_dict.get(self.words.get(word)[0]).get(correlated)), np.std(aux_dict.get(self.words.get(word)[0]).get(correlated)), len(aux_dict.get(self.words.get(word)[0]).get(correlated))
            self.correlated_words[self.words.get(word)[0]] = aux_correlated_dict
        
        #Assigning a small value to relations with a std equal to zero
        for word in self.correlated_words:
            for correlated in self.correlated_words.get(word):
                if self.correlated_words.get(word).get(correlated)[1] == 0:
                    self.correlated_words.get(word)[correlated] = self.correlated_words.get(word).get(correlated)[0], 0.00000001, self.correlated_words.get(word).get(correlated)[2]

def main():
    book = get_word_text('c:\PY\Python\Machine_learning\\texts\hp_sorcerer_stone.txt')
    file_pi = open('c:\PY\Python\Machine_learning\Compose_v2\\book.obj', 'wb') 
    pickle.dump(book, file_pi)

start = time.time()
main()
print(time.time() - start)
