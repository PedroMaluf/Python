import math
import numpy as np
import time
import scipy.stats
import pickle
from graphv2 import Graph

punctuation = ('.','?','!')

#Same class as the object loaded from pickle
class Book:
    def __init__(self, text):
        self.text = text
        self.chapter_len = () # (mean, std)
        self.chapters = {}   # Index: chapter name, chapter len
        self.paragraphs = {} # Index: value, chapter index, paragraph len, chapter position
        self.sentences = {}  # Index: value, chapter index, paragraph index, sentence len, paragraph position
        self.words = {}      # Index: value, chapter index, paragraph index, sentence index, sentence position, dict correlated words{word: word, mean_dis, std_dis}
        self.correlated_words = {} #Word: dict correlated words{word: mean_dis, std_dis}        
    
#Create graph without the multipliers
def make_graph(book):
    g = Graph()
    previous_word = None

    for word in book.words:
        word_vertex = g.get_vertex(book.words.get(word)[0])
        
        if previous_word:
            #If the previous word is a punctuation the next word must be incremented in all the punctuation
            if previous_word.value == '.' or previous_word.value == '!' or previous_word.value == '?':
                g.get_vertex('.').increment_weight(word_vertex)
                g.get_vertex('!').increment_weight(word_vertex)
                g.get_vertex('?').increment_weight(word_vertex)

            else:
                previous_word.increment_weight(word_vertex)

        previous_word = word_vertex

    g.generate_probability_mapping()

    return g

#Update graph with the multipliers
def update_graph(graph, word):
    previous_word = word

    for word in graph.words_to_multiply:
        word_vertex = graph.get_vertex(word)
        previous_word.multiply_weight(word_vertex, word_vertex.multiplier_correlateds)

    graph.generate_probability_mapping()

    return graph

#Compose a new chapter
def compose(book, g):
    composition = []
    composition_chapter_size = round(np.random.normal(book.chapter_len[0], book.chapter_len[1]))        
    first_word_in_sentence = {}     #{Sentence index: composition index}
    is_first_word_in_sentence = True

    #Create a number of paragraph based on the normal curve of chapters size
    for composition_current_paragraph in range(composition_chapter_size):
        paragraph_size = []
        paragraph_weight = []
        

        for paragraph in book.paragraphs:
            paragraph_size.append(book.paragraphs.get(paragraph)[-2])
            paragraph_weight.append(1/(1 + 10 * abs(book.paragraphs.get(paragraph)[-1] - composition_current_paragraph/composition_chapter_size)))
        
        paragraph_mean_size = np.average(paragraph_size, weights = paragraph_weight)
        paragraph_std_size = math.sqrt(np.average((paragraph_size-paragraph_mean_size)**2, weights = paragraph_weight))
        composition_paragraph_size = max(round(np.random.normal(paragraph_mean_size, paragraph_std_size)),1)
        
        #Create a number of sentence based on the normal curve of paragraph size, with the most probably size being similar to paragraphs in this position on the chapter
        for composition_current_sentence in range(composition_paragraph_size):
            spaces_in_sentence = 0      #Number of spaces in each sentence
            first_word_in_sentence[composition_current_sentence] = len(composition)
            new_sentence = False

            #The first word in a paragraph must consider the last word to be a punctuation
            if composition_current_sentence == 0:
                word = g.get_next_word(g.get_vertex('.'))

                #The first word in a sentence must be capitalized unless it is ~, meaning the start of a dialog
                if word.value != '~':
                    composition.append(word.value.capitalize())
                    is_first_word_in_sentence = False

                else:
                    composition.append(word.value)

                composition.append(' ')     #Insert a space after every word
                spaces_in_sentence += 1

            while not new_sentence:
                g.words_to_multiply = []
                index = first_word_in_sentence.get(composition_current_sentence)
                
                #Define wich words to add a multiplier and calculate the multipliers
                for i in range(index, len(composition) - 2):
                    if composition[i] == ' ':
                        continue
                    for correlated_word in book.correlated_words.get(composition[i].lower()):
                        if g.get_vertex(correlated_word) in word.adjacent.keys():
                            correlated_mean = book.correlated_words.get(composition[i].lower()).get(correlated_word)[0]
                            correlated_std = book.correlated_words.get(composition[i].lower()).get(correlated_word)[1]
                            correlated_len = book.correlated_words.get(composition[i].lower()).get(correlated_word)[2]
                            g.get_vertex(correlated_word).multiplier_correlateds.append(correlated_len * abs(scipy.stats.norm(correlated_mean, correlated_std).cdf(len(composition) - i - spaces_in_sentence) - scipy.stats.norm(correlated_mean, correlated_std).cdf(len(composition) - i + 1 - spaces_in_sentence)))
                            g.words_to_multiply.append(correlated_word)

                g = update_graph(g,word)
                word = g.get_next_word(word)
                g = make_graph(book)

                #The first word in a sentence must be capitalized unless it is ~, meaning the start of a dialog
                if is_first_word_in_sentence and word.value != '~':
                    composition.append(word.value.capitalize())
                    is_first_word_in_sentence = False
                else:
                    composition.append(word.value)

                composition.append(' ')     #Insert a space after every word
                spaces_in_sentence += 1

                #Remove the space before a ,
                if word.value == ',':
                    spaces_in_sentence -= 1
                    del composition[len(composition) - 3]
                
                #Remove the space before a punctuation and start a new sentence
                if word.value in punctuation:
                    spaces_in_sentence -= 1
                    del composition[len(composition) - 3]
                    is_first_word_in_sentence = True
                    new_sentence = True
            
        composition.append('\n\n')

    return composition

def main():
    file_pi = open('c:\PY\Python\Machine_learning\Compose_v2\\book.obj', 'rb') 
    book = pickle.load(file_pi)
    print('book read')
    g = make_graph(book)
    print('graph made')
    composition = compose(book, g)

    return ''.join(composition)   

if __name__ =='__main__':
    start = time.time()
    print(main())
    print(time.time() - start)
