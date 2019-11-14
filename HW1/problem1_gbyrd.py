# STAT/CS 287
# HW 01
#
# Name: Galen Byrd
# Date: <FILL ME IN>


def similarity(A,B):
    """Computes and prints the similarity between two sets defined as the number 
    of elements in both sets, divided byt the total unique number of elements in both sets"""
    print("similarity: ",len(A.intersection(B))/len(A.union(B)))


A={1,2,3,4,5}
B={4,5,6,7,8}
print("Set A: ",A)
print("Set B: ",B)
similarity(A,B)

primes = {2, 3, 5, 7}
odds = {1, 3, 5, 7, 9}
print("Set primes: ",primes)
print("Set odds: ",odds)
similarity(primes,odds)
