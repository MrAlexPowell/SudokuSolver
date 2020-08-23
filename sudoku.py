from copy import deepcopy
def puzzPrint(puzzle):
    print()
    for i in puzzle:
        for j in i:
            print(j, end=' ')
        print()

def puzzPrintFile(puzzle,file):
    for i in puzzle:
        for j in i:
            file.write(str(j)+" ")
        file.write("\n")

def getDifferences(original,modified):
    count = 0
    for i in range(len(original)):
        for j in range(len(original[i])):
            if(original[i][j]!=modified[i][j]):   
                count+=1
    return count

def getRow(m,row):
    #Returns row given index(0-8)
    return m[row]

def getCol(m, col):
    #Returns col given index(0-8)
    c = []
    for row in m:
        c.append(row[col])
    return c

def getBox(m, box):
    #Return box given index(0-8)
    b = []
    c=box%3
    r=box//3
    for i in range(3):
        for j in range(3):
            b.append(m[3*r+i][3*c+j])
    return b

def boxPoss(x,y,puzzle):
    #Return list of all possibilities of whole box
    #[[x,y,[nums]],[x2,y2,[nums2]],...[x9,y9,[nums9]]]
    box = (3*(y//3))+(x//3)
    poss = []
    c=box%3
    r=box//3
    for i in range(3):
        for j in range(3):
            ny = i+3*r
            nx = j+3*c
            if(puzzle[ny][nx]==0):
                poss.append([nx,ny,getPoss(nx,ny,puzzle,1)])
            else:
                poss.append([nx,ny,[puzzle[ny][nx]]])
    return poss

def checkNine(line):
    if (0 in line):
        return False
    elif len(set(line))!=9:
        return False
    return True

def checkGood(puzzle):
    #Check every row
    for i in range(9):
        if(not checkNine(getRow(puzzle,i))):
            return False
    #Check every col
    for i in range(9):
        if(not checkNine(getCol(puzzle,i))):
            return False
    #Check every box
    for i in range(9):
        if(not checkNine(getBox(puzzle,i))):
            return False
    return True

#__________________________________________________________
#Core Function 'getPoss' (and helper functions), which
#return a list of all possibilities for a certain square

def getPoss(x,y,puzzle,caller,invalid=[]):
    nums = [1,2,3,4,5,6,7,8,9,0]
    #Remove obvious possibilites(from row,col,box)
    for n in getRow(puzzle,y):
        if n in nums:
            nums[nums.index(n)]=0
    for n in getCol(puzzle,x):
        if n in nums:
            nums[nums.index(n)]=0
    box=(3*(y//3))+(x//3)
    for n in getBox(puzzle,box):
        if n in nums:
            nums[nums.index(n)]=0

    #Additional information for main function to call
    if(caller == 0):
        #Determine obscure numbers it can't be
        for n in getInvalid(x,y,puzzle,invalid):
            if n in nums:
                nums[nums.index(n)]=0
    return list(set(sorted(nums)))[1:]

def getInvalid(x,y,puzzle,invalid=["ZZZ"]):
    #Returns nums which are invalid
    nums = []
    if(invalid==["ZZZ"]):
        for n in blockCol(x,y,puzzle):
            if n not in nums:
                nums.append(n)
        for n in blockRow(x,y,puzzle):
            if n not in nums:
                nums.append(n)
    else:
        for n in invalid[0][y//3][x]:
            if n not in nums:
                nums.append(n)
        for n in invalid[1][y][x//3]:
            if n not in nums:
                nums.append(n)
    return nums

def getAllInvalidOnCol(puzzle):
    #Returns all nums which are invald
    #[[[box,[nums]],[box2,[nums2]],[box3,[nums3]]],...]
    allInv = []
    for y in range(9):
        allcol = []
        for x in range(0,9,3):
            allx = []
            for n in blockCol(x,y,puzzle):
                if(n not in allx):
                    allx.append(n)
            allcol.append(allx)
        allInv.append(allcol)
    return allInv

def getAllInvalidOnRow(puzzle):
    #Returns all nums which are invald
    #[[[nums],[nums2],[nums3]],...]
    allInv = []
    for y in range(0,9,3):
        allrow = []
        for x in range(9):
            ally=[]
            for n in blockRow(x,y,puzzle):
                if(n not in ally):
                    ally.append(n)
            allrow.append(ally)
        allInv.append(allrow)
    return allInv

def blockCol(x,y,puzzle):
    #Returns nums which are invalid(block/col interaction)
    nums = []
    for x2 in range(0,9,3):
        if((3*(y//3))+(x//3) != (3*(y//3))+(x2//3)):
            #[[x,y,[nums]],[x2,y2,[nums2]],...[x9,y9,[nums9]]]
            allBox = boxPoss(x2,y,puzzle)
            for n in allBox:
                if((n[1] == y) and (len(n[2])>1)):
                    for num in n[2]:
                        valid = True
                        for other in allBox:
                            if(other[1] != y):
                                if(num in other[2]):
                                    valid = False
                        if(valid == True):
                            nums.append(num)
    return nums

def blockRow(x,y,puzzle):
    #Returns nums which are invalid(block/row interaction)
    nums = []
    for y2 in range(0,9,3):
        if((3*(y//3))+(x//3) != (3*(y2//3))+(x//3)):
            #[[x,y,[nums]],[x2,y2,[nums2]],...[x9,y9,[nums9]]]
            allBox = boxPoss(x,y2,puzzle)
            for n in allBox:
                if((n[0] == x) and (len(n[2])>1)):
                    for num in n[2]:
                        valid = True
                        for other in allBox:
                            if(other[0] != x):
                                if(num in other[2]):
                                    valid = False
                        if(valid == True):
                            nums.append(num)
    return nums

#__________________________________________________________
#Function for 'OnlyPoss' Algorithm, which finds if there is
#only one number possible that can go there

def solveOnlyPoss(puzzle,invalid=[]):
    for y in range(9):
        for x in range(9):
            if(puzzle[y][x]==0):
                poss = getPoss(x,y,puzzle,0,invalid)
                if(len(poss)==1):
                    puzzle[y][x]=poss[0]

#__________________________________________________________
#Functions for 'OnlyInst' Algorithm, which determines if a
#specific place has the only instance of a number

def solveOnlyInst(puzzle,invalid=[]):
    for y in range(9):
        for x in range(9):
            if(puzzle[y][x]==0):
                puzzle[y][x] = checkInst(x,y,puzzle,invalid)


def checkInst(x,y,puzzle,invalid=[]):
    numsOld = getPoss(x,y,puzzle,0,invalid)
    nums = deepcopy(numsOld)
    if(len(nums)==1):
        return nums[0]
    for x2 in range(9):
        if(x2!=x):
            if(puzzle[y][x2]==0):
                poss = getPoss(x2,y,puzzle,0,invalid)
                for n in poss:
                    if n in nums:
                        nums[nums.index(n)]=0
    if(len(set(nums))==2):
        return list(set(sorted(nums)))[1]

    nums = deepcopy(numsOld)
    for y2 in range(9):
        if(y2!=x):
            if(puzzle[y2][x]==0):
                poss = getPoss(x,y2,puzzle,0,invalid)
                for n in poss:
                    if n in nums:
                        nums[nums.index(n)]=0
    if(len(set(nums))==2):
        return list(set(sorted(nums)))[1]

    nums = deepcopy(numsOld)
    xStart = 3*(x//3)
    yStart = 3*(y//3)
    for xA in range(3):
        for yA in range(3):
            if(not ((yStart+yA==y) and (xStart+xA==x))):
                if(puzzle[yStart+yA][xStart+xA]==0):
                    poss = getPoss(xStart+xA,yStart+yA,puzzle,0,invalid)
                    for n in poss:
                        if n in nums:
                            nums[nums.index(n)]=0
    if(len(set(nums))==2):
        return list(set(sorted(nums)))[1]
    else:
        return 0
    

#__________________________________________________________
#Main Function which runs algorithms until nothing new is added
def main(fileOut=False):
    puzzle = []
    for i in range(9):
        line = list(map(int,input().split()))
        puzzle.append(line)
    original = deepcopy(puzzle)
    bestPoss = False
    while(not checkGood(puzzle) and not bestPoss):
        best = deepcopy(puzzle)
        #Run 'OnlyPoss' until nothing is changed
        changed = True
        temp = deepcopy(puzzle)
        #Get Invalid Nums for easy access later
        invalid = [getAllInvalidOnRow(puzzle),getAllInvalidOnCol(puzzle)]
        while(changed):
            solveOnlyPoss(puzzle,invalid)
            if(temp == puzzle):
                changed = False
            else:
                temp = deepcopy(puzzle)
        if(checkGood(puzzle)):
            break
        #Run 'OnlyInst' until nothing is changed
        changed = True
        temp = deepcopy(puzzle)
        while(changed):
            solveOnlyInst(puzzle,invalid)
            if(temp == puzzle):
                changed = False
            else:
                temp = deepcopy(puzzle)
        if(best == puzzle):
            bestPoss = True
    if(bestPoss):
        print("\nThis is the current best I can do:")
        puzzPrint(puzzle)
        print("\nNumbers Solved:",getDifferences(original,puzzle))
    else:
        puzzPrint(puzzle)

    #Output to file
    if(fileOut):
        file=open("output.txt","w")
        if(bestPoss):
            file.write("This is the current best I can do:\n\n")
            puzzPrintFile(puzzle,file)
            file.write("\nNumbers Solved: "+str(getDifferences(original,puzzle)))
        else:
            puzzPrintFile(puzzle,file)
        file.close()

fileOut=False #Edit this variable if you would like output to be saved
try:
    main(fileOut)
except:
    print("Something went wrong. Check if puzzle was entered correctly.")
    if fileOut:
        file = open("output.txt","w")
        file.write("Something went wrong. Check if puzzle was entered correctly.")
        file.close()
