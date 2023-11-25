
class Hasher():

    def __init__(self):
        pass
    def hash(self, s1, s2):
        maxL = len(s1) if len(s1) < len(s2) else len(s2)
        
        charsS1 = []

        for i in range(maxL):
            if (s1[i] == s2[i]):
                charsS1.append(s1[i])

        charsS2 = []

        for i in range(maxL):
            if (s2[i] == s1[i]):
                charsS2.append(s2[i])
        
        common = len(charsS1) if len(charsS1) > len(charsS2) else len(charsS2)
        
        return float(common / maxL)
