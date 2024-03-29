# import the base interface for the cubixo generator
from bot.Cogs.Cubixo.iCubixoGenerator import iCubixoGenerator

#
#   Cubixeador
#   Implementation of iCubixoGenerator
#   Old implementation of this method. Its ugly, cramped and unoptimized. Its shit.
#   Might rework it later when im not lazy. For now it does the trick
#
class Cubixeador(iCubixoGenerator):
    def generate(self, text : str) -> str:
        n = text
        listixa=[]
        for i in range(len(n)):
            listixa.append(n[i].lower())
        if listixa[-3:]!=["i","x","o"]:
            listixa.append("i")
            listixa.append("x")
            listixa.append("o")
        if listixa[-4] in "aeiouAEIOU":
            listixa.pop(-4)
        ret="SHoT_The"
        for i in range(len(listixa)):
            if (listixa.index(listixa[-3],-3))%2==0:
                if listixa[i]=="i" or listixa[i]=="I":
                    ret=ret+"i"
                elif listixa[i]=="l" or listixa[i]=="L":
                    ret=ret+"L"
                elif listixa[i]==" ":
                    ret=ret+"_"
                elif i==0 or i==1:
                    ret=ret+listixa[i].upper()
                elif i%2==1:
                    ret=ret+listixa[i].upper()
                else:
                    ret=ret+listixa[i].lower()
            else:
                if listixa[i]=="i" or listixa[i]=="I":
                    ret=ret+"i"
                elif listixa[i]=="l" or listixa[i]=="L":
                    ret=ret+"L"
                elif listixa[i]==" ":
                    ret=ret+"_"
                elif i%2==0:
                    ret=ret+listixa[i].upper()
                else:
                    ret=ret+listixa[i].lower()
        return ret
