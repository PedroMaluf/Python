from Amostras_madlibs import Code, Zombies, Zoo
import random

#Call randomly one of the 3 madlibs
if __name__ == "__main__":
    m = random.choice([Code, Zombies, Zoo])
    m.madlib()
