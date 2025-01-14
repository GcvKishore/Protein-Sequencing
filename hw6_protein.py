"""
Protein Sequencing Project
Name:
Roll Number:
"""

import hw6_protein_tests as test

project = "Protein" # don't edit this

### WEEK 1 ###

'''
readFile(filename)
#1 [Check6-1]
Parameters: str
Returns: str
'''
def readFile(filename):
    file = open(filename)
    split = file.read().splitlines()
    string = "".join(split)
    return string


'''
dnaToRna(dna, startIndex)
#2 [Check6-1]
Parameters: str ; int
Returns: list of strs
'''
def dnaToRna(dna, startIndex):
    list1= []
    for i in range(startIndex,len(dna),3):
        list1.append(dna[i:i+3])
        if dna[i:i+3]== "TAA" or dna[i:i+3]== "TAG" or dna[i:i+3]== "TGA":
            break
    replace=[string.replace("T","U") for string in list1]
    return replace

'''
makeCodonDictionary(filename)
#3 [Check6-1]
Parameters: str
Returns: dict mapping strs to strs
'''
def makeCodonDictionary(filename):
    import json
    dict_1 = {}
    file = open(filename)
    load = json.load(file)
    for i,j in load.items():
        for k in j:
            dict_1[k.replace("T","U")] = i
    return dict_1


'''
generateProtein(codons, codonD)
#4 [Check6-1]
Parameters: list of strs ; dict mapping strs to strs
Returns: list of strs
'''
def generateProtein(codons, codonD):
    protein=[]
    if codons[0]=='AUG':
        protein.append('Start')
    for i in range(1,len(codons)):
        if codons[i] in codonD.keys():
            protein.append(codonD[codons[i]])
    return protein
 
'''
synthesizeProteins(dnaFilename, codonFilename)
#5 [Check6-1]
Parameters: str ; str
Returns: 2D list of strs
'''
def synthesizeProteins(dnaFilename, codonFilename):
    count = 0
    proteins=[]
    file1 = readFile(dnaFilename)
    file2 = makeCodonDictionary(codonFilename)
    i=0
    while i < len(file1):
        if file1[i:i+3] == "ATG":
            dna= dnaToRna(file1, i)
            # print(dna)
            protein1 = generateProtein(dna,file2)
            # print(protein1)
            proteins.append(protein1)
            i = i+3*len(dna)
        else:
            i = i+1
            count = count+1
    print("Unused bases are : ", count)
    print("Total Bases are : ", len(file1))
    print("Proteins count are : ", len(proteins)) 
    return proteins

def runWeek1():
    print("Human DNA")
    humanProteins = synthesizeProteins("data/human_p53.txt", "data/codon_table.json")
    print("Elephant DNA")
    elephantProteins = synthesizeProteins("data/elephant_p53.txt", "data/codon_table.json")


### WEEK 2 ###

'''
commonProteins(proteinList1, proteinList2)
#1 [Check6-2]
Parameters: 2D list of strs ; 2D list of strs
Returns: 2D list of strs
'''
def commonProteins(proteinList1, proteinList2):
    uni_list = []
    for i in proteinList1:
        for j in proteinList2:
            if i==j and i not in uni_list:
                    uni_list.append(i)
    return uni_list

'''
combineProteins(proteinList)
#2 [Check6-2]
Parameters: 2D list of strs
Returns: list of strs
'''

def combineProteins(proteinList):
    list1=[]
    for i in proteinList:
        for j in i:
            if i not in list1:
                list1.append(j)
    return list1

'''
aminoAcidDictionary(aaList)
#3 [Check6-2]
Parameters: list of strs
Returns: dict mapping strs to ints
'''
def aminoAcidDictionary(aaList):
    dict1={}
    for i in aaList:
        if i in dict1:
            dict1[i] = dict1[i] + 1
        else:
            dict1[i] = 1
    return dict1


'''
findAminoAcidDifferences(proteinList1, proteinList2, cutoff)
#4 [Check6-2]
Parameters: 2D list of strs ; 2D list of strs ; float
Returns: 2D list of values
'''

def findAminoAcidDifferences(proteinList1, proteinList2, cutoff):
    lst1=combineProteins(proteinList1)
    lst2=combineProteins(proteinList2)
    dict1=aminoAcidDictionary(lst1)
    dict2=aminoAcidDictionary(lst2)
    freq1={}
    freq2={}
    x=[]
    # frequency1=0
    # frequency2=0
    final_diff=[]
    for i in dict1:
        freq1[i]=dict1[i]/len(lst1)
        if i not in x and i!='Start' and i!='Stop':
            x.append(i)
    for j in dict2:
        freq2[j]=dict2[j]/len(lst2)
        if j not in x and j!='Start' and j!='Stop':
            x.append(j)
    # print(dict1,len(dict1),"f1")
    # print(dict2,len(dict2),"f2")
    for k in x:
        frequency1=0
        frequency2=0
        if k in freq1:
            frequency1=freq1[k]
        if k in freq2:
            frequency2=freq2[k]
        diff=frequency2-frequency1
        if diff > cutoff or diff< -cutoff:
            final_diff.append([k,frequency1,frequency2])
    return final_diff

'''
displayTextResults(commonalities, differences)
#5 [Check6-2]
Parameters: 2D list of strs ; 2D list of values
Returns: None
'''
def displayTextResults(commonalities, differences):
    print("The following proteins occurred in both DNA Sequences:")
    for i in commonalities:
        cproteins=""
        lst=i[1:(len(i)-1)]
        count=0
        for j in lst:
            cproteins+=j
            count+=1
            if count!=len(lst):
                cproteins+="-"
        if len(cproteins)!=0:
            print(cproteins)
    print("The following amino acids occurred at very different rates in the two DNA sequences:")
    for i in differences:
        a=i[0]
        freq1=round(i[1]*100,2)
        freq2=round(i[2]*100,2)
        print(str(a)+" "+str(freq1)+" % in Seq1"+","+str(freq2)+"% in Seq2")
    return

def runWeek2():
    humanProteins = synthesizeProteins("data/human_p53.txt", "data/codon_table.json")
    elephantProteins = synthesizeProteins("data/elephant_p53.txt", "data/codon_table.json")

    commonalities = commonProteins(humanProteins, elephantProteins)
    differences = findAminoAcidDifferences(humanProteins, elephantProteins, 0.005)
    displayTextResults(commonalities, differences)


### WEEK 3 ###

'''
makeAminoAcidLabels(proteinList1, proteinList2)
#2 [Hw6]
Parameters: 2D list of strs ; 2D list of strs
Returns: list of strs
'''
def makeAminoAcidLabels(proteinList1, proteinList2):
    gene=[]
    list1=combineProteins(proteinList1)
    list2=combineProteins(proteinList2)
    dict_1=aminoAcidDictionary(list1)
    dict_2=aminoAcidDictionary(list2)
    for i in dict_1:
        if i not in gene:
            gene.append(i)
    for j in dict_2:
        if j not in gene:
            gene.append(j)
    gene.sort()
    return gene

'''
setupChartData(labels, proteinList)
#3 [Hw6]
Parameters: list of strs ; 2D list of strs
Returns: list of floats
'''
def setupChartData(labels, proteinList):
    list1=combineProteins(proteinList)
    dict_1=aminoAcidDictionary(list1)
    gene=[]
    for i in labels:
        if i in dict_1:
            gene.append(dict_1[i]/len(list1))
        else:
            gene.append(0)
    return gene

'''
createChart(xLabels, freqList1, label1, freqList2, label2, edgeList=None)
#4 [Hw6] & #5 [Hw6]
Parameters: list of strs ; list of floats ; str ; list of floats ; str ; [optional] list of strs
Returns: None
'''
def createChart(xLabels, freqList1, label1, freqList2, label2, edgeList=None):
    import matplotlib.pyplot as plt
    import numpy as np
    w=0.4
    xvalues=np.arange(len(xLabels))
    plt.bar(xvalues,freqList1,width=-w,align='edge',label=label1,edgecolor=edgeList)
    plt.bar(xvalues,freqList2,width=w,align='edge',label=label2,edgecolor=edgeList)
    plt.xticks(ticks=list(range(len(xLabels))),labels=xLabels,rotation="vertical")
    plt.legend()
    plt.title("Comparision of Frequencies")
    plt.show()
    return

'''
makeEdgeList(labels, biggestDiffs)
#5 [Hw6]
Parameters: list of strs ; 2D list of values
Returns: list of strs
'''
def makeEdgeList(labels, biggestDiffs):
    edgelst=[]
    words=[]
    for i in range(len(biggestDiffs)):
        words.append(biggestDiffs[i][0])
    for i in range(len(labels)):
        if labels[i] in words:
            edgelst.append("black")
        else:
            edgelst.append("white")
    return edgelst

'''
runFullProgram()
#6 [Hw6]
Parameters: no parameters
Returns: None
'''
def runFullProgram():
    humanproteins=synthesizeProteins("data/human_p53.txt","data/codon_table.json")
    eleproteins=synthesizeProteins("data/elephant_p53.txt","data/codon_table.json")
    cproteins=commonProteins(humanproteins,eleproteins)
    diff=findAminoAcidDifferences(humanproteins,eleproteins,0.005)
    displayTextResults(cproteins,diff)
    labels=makeAminoAcidLabels(humanproteins,eleproteins)
    f1=setupChartData(labels,humanproteins)
    f2=setupChartData(labels,eleproteins)
    edges=makeEdgeList(labels,diff)
    createChart(labels, f1, "Human", f2, "Elephant", edgeList=edges)
    return



### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # runWeek1()
    # test.testReadFile()
    # test.testDnaToRna()
    # test.testMakeCodonDictionary()
    # test.testSynthesizeProteins()
    # test.testCommonProteins()
    # test.testCombineProteins()
    # test.testAminoAcidDictionary()
    # test.testFindAminoAcidDifferences()
    # test.testMakeAminoAcidLabels()
    # test.testSetupChartData()
    # test.testCreateChart()
    # test.testMakeEdgeList() 
    ## Uncomment these for Week 2 ##
    
    # print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    # test.week2Tests()
    # print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # runWeek2()
   

    ## Uncomment these for Week 3 ##

    print("\n" + "#"*15 + " WEEK 3 TESTS " +  "#" * 16 + "\n")
    test.week3Tests()
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    runFullProgram()
