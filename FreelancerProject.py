import linecache
import copy

#TODO: Sort each net file list
#TODO: find mins and maxes in each list and replace them, fixed insts are not getting replaced


	
# 11 insts types 
# ['FDRE', 'LUT2', 'LUT3', 'LUT4', 'LUT5', 'LUT6', 'RAMB36E2', 'DSP48E2', 'IBUF', 'OBUF', 'BUFGCE']

listOfInstances = [] # Where all insts are saved along with their information

listOfNets = [] # Where all the nets are saved along with their insts

def main():


	readInsts() # Fill the listOfInstances list

	readNetFile() # Fill the listOfNets list

	sortMaxMinSwapLists() # Swap the min values

	writeFile()


def writeFile():
	f = open("NewCoordinates_SerialNo.txt","w")

	for x in listOfNets:
		for i in x.insts:
			f.write("inst_" + str(i.inum) + " " + str(i.xcord) + " " + str(i.ycord) + " " + i.snum + " " + i.ftype + "\n")




def sortMaxMinSwapLists():

	for x in listOfNets:	# for every Net 
		#print("For Net %s"%(x.name))

		# ----------------------------- SORT X AXIS ---------------------------------------

	
		x.insts.sort(key=lambda x: x.xcord, reverse=False)	# Sort list in X axis


		index_xmax = len(x.insts) - 1	# Get index of xmax
		xmax = x.insts[index_xmax] # This is the current xmax

		xmin = x.insts[0]	# List is sorted so min is always at position 0


		for i in range (len(x.insts)-1): # Iterate all elements except the min which is in place 0


			if xmin.itype == "FIXED": # We do not change fixed insts
				break

			xmax = x.insts[index_xmax] # This is the current xmax

			
			xmin.xcord = xmax.xcord # Y remains constant # THIS LINE CAUSES PROBLEM


			if(isSameType(xmin.xcord,xmin.ycord,xmin.itype)): # Check if the same type, if they are we are done with xmin for Net
				#print("Inst %s changed with inst %s coordinates %d %d"%(xmin.inum,xmax.inum,xmin.xcord,xmax.xcord))
				break
			else:
				index_xmax -= 1 # We move to the next xmax


		# ----------------------------- SORT Y AXIS ---------------------------------------

		x.insts.sort(key=lambda x: x.ycord, reverse=False)	# Sort list in Y axis

		index_ymax = len(x.insts) - 1	# Get index of ymax
		ymax = x.insts[index_ymax] # This is the current ymax

		ymin = x.insts[0]

		for i in range (len(x.insts)-1): # Iterate all elements except the min which is in place 0


			if ymin.itype == "FIXED": # We do not change fixed insts
				break

			ymax = x.insts[index_ymax] # This is the current xmax

			
			ymin.ycord = ymax.ycord # X remains constant 


			if(isSameType(ymin.ycord,ymin.ycord,ymin.itype)): # Check if the same type, if they are we are done with xmin for Net
				#print("Inst %s changed with inst %s coordinates %d %d"%(xmin.inum,xmax.inum,xmin.xcord,xmax.xcord))
				break
			else:
				index_xmax -= 1 # We move to the next xmax

		# for i in x.insts:
		# 	print(i)



def isSameType(xcord,ycord,itype):
	#check if the inst in those coordinates is the same type as the given inst
	for i in listOfInstances:	# For every i in list of instances
		if i.xcord == xcord and i.ycord == ycord and i.itype[:-1] == itype[:-1]: # [:-1] is for LUT, we ignore the number
			return True	# If x,y coordinates and type are the same then the swapping was successful
	return False # We didn't found an inst with the same coordinates and type
	



def readNetFile():

	with open("design.nets","r") as f: # Read the design.nets file
		for line in f: # For every line in file f
			if line.split()[0] =="net": # Split the line into substring and get the first one, if its net get into if clause
				p = Net(line.split()[1]) # Create a Net object with substring in position 1 as name
				listOfNets.append(p) # Put it into list of Nets

				line = next(f)	# Get to next line after net
							  	# Idea is that now we want to read insts
				try:			# To avoid some errors		
					while line != "endnet":	#If we read endnet means that the net is over
						x = searchInst(line.split()[0]) # Example : inst_4
						p.insts.append(x)	# Every net has a list of insts, put that inst we read there
						line = next(f)		# Move to next line
				except: 
					None	# If exception do nothing



def searchInst(inst_word):
	inst_num = int(inst_word[5:]) # If inst_4, gets 4, we need to find inst_4
	j = inst_num
	for i in range(0,10): # Usually their is a false approximation 5 places in the listofInstances array, example inst_4 is at index 2
		try:
			if listOfInstances[j].inum == inst_num:
				x = copy.deepcopy(listOfInstances[j])
				return x
			else:
				j -= 1
		except:
			j -= 1	
			continue



def iterateReversedListY(list,x): # For the current inst x, iterate the list of each type which contains the ordered coordinates
	for inst in reversed(list):
		# If the max is bigger that x.ycord, the X axis is the same and y and inst are different
				if inst.ycord > x.ycord and inst.xcord==x.xcord and int(x.inum) != int(inst.inum): 
					# Print what is being replaced by what and break from the for loop
					# Print is for debugging purposes
					# print("inst_%s %s (%s,%s) replaces ycord by inst_%s %s (%s,%s)"%(x.inum, x.itype, x.xcord ,x.ycord, inst.inum, inst.itype, inst.xcord, inst.ycord))
					x.ycord = x.ycord
					break


def swapYAxis():
	for x in listOfInstances:
		if x.ftype=="FIXED": # Fixed inst should not be moved
			continue

		# Inst is UNFIXED
		if x.itype == "FDRE": 
			iterateReversedListY(listFDRE,x)
		elif x.itype in "RAMB36E2": 
			iterateReversedListY(listRAMB,x)
		elif x.itype == "DSP48E2":
			iterateReversedListY(listDSP,x)
		elif x.itype == "IBUF":
			iterateReversedListY(listIBUF,x)
		elif x.itype == "OBUF":
			iterateReversedListY(listOBUF,x)
		elif x.itype == "BUFGCE":
			iterateReversedListY(listBUFGCE,x)
		elif "LUT" in x.itype:
			iterateReversedListY(listLUT,x)



def sortYAxis(): # Sorts all lists by the ycord attribute
	listLUT.sort(key=lambda x: x.ycord, reverse=True)
	listFDRE.sort(key=lambda x: x.ycord, reverse=True)
	listRAMB.sort(key=lambda x: x.ycord, reverse=True)
	listDSP.sort(key=lambda x: x.ycord, reverse=True)
	listIBUF.sort(key=lambda x: x.ycord, reverse=True)
	listOBUF.sort(key=lambda x: x.ycord, reverse=True)
	listBUFGCE.sort(key=lambda x: x.ycord, reverse=True)


def swapXAxis(): # Lists are already ordered on their X coordinates, see Coordinates_SerialNo.txt
	for x in listOfInstances:
		if x.ftype=="FIXED": # Fixed inst should not be moved
			continue

		# Inst is UNFIXED
		if x.itype == "FDRE": 
			iterateReversedListX(listFDRE,x)
		elif x.itype in "RAMB36E2": 
			iterateReversedListX(listRAMB,x)
		elif x.itype == "DSP48E2":
			iterateReversedListX(listDSP,x)
		elif x.itype == "IBUF":
			iterateReversedListX(listIBUF,x)
		elif x.itype == "OBUF":
			iterateReversedListX(listOBUF,x)
		elif x.itype == "BUFGCE":
			iterateReversedListX(listBUFGCE,x)
		elif "LUT" in x.itype:
			iterateReversedListX(listLUT,x)
			

def iterateReversedListX(list,x): # For the current inst x, iterate the list of each type which contains the ordered coordinates
	for inst in reversed(list):
		# If the max is bigger that x.xcord, the Y axis is the same and x and inst are different
				if inst.xcord > x.xcord and inst.ycord==x.ycord and int(x.inum) != int(inst.inum): 
					# Print what is being replaced by what and break from the for loop
					# Print is for debugging purposes
					# print("inst_%s %s (%s,%s) replaces xcord by inst_%s %s (%s,%s)"%(x.inum, x.itype, x.xcord ,x.ycord, inst.inum, inst.itype, inst.xcord, inst.ycord))
					x.xcord = inst.xcord
					break

    

def readInsts():
	f1 = open("Coordinates_SerialNo.txt","r") # Open file

	Lines = f1.readlines() # Gets all lines as String

	for line in Lines: 

		words = line.split() # Split line into words

		inum = int(words[0][5:]) # Get only the inst number, example inst_333 gets 333

		itype = findInstancesTypesBasedOnInstNum(str(inum)) # Find the type of inst

		p = Instance(inum, int(words[1]), int(words[2]), words[3],itype,words[4]) # Create the Instance object
		listOfInstances.append(p) # Put it on the list

		listOfInstances.sort(key=lambda x: x.inum, reverse=False) # Sort the list based on inum

		f1.close() # Close file



def findInstancesTypesBasedOnInstNum(inum):
	# For e.g. inst_451 is at line 450 of design.nodes so to save complexity I search that inst_num - 1 because probably it will be there
	# The maximum difference is 4, 3340 is at line 3336 at design.nodes
	# It's not in (inum-1) search more -- max is 4, 5 just to be sure, if input file will be bigger set bigger range
	for i in range(1,5):
		line = linecache.getline("design.nodes", int(inum)-i) # If we are searching inst_451 probably its in design.nodes line 450

		words = line.split() # Get each substring of string and put them in a table

		try:	# Put it in a try clause to get away from errors
			if words[0][5:] == inum:	# Example: inum = 450 , words[0] = inst_451 , words[0][5:] = 451
				return words[1]
		except:	#If an error occurs do nothing
			None


class Instance:
# Ex:
#	inum: inst_1299
#	xcord: 1	Xcoordinate
#	ycord: 0	Ycoordinate
#	snum: 24	Serial Number
#	itype: LUT4		['FDRE', 'LUT2', 'LUT3', 'LUT4', 'LUT5', 'LUT6', 'RAMB36E2', 'DSP48E2', 'IBUF', 'OBUF', 'BUFGCE']
#	ftype: FIXED	FIXED/UNFIXED

	def __init__(self,inum,xcord,ycord,snum,itype,ftype): # Constructor of the Instance class, by instance I mean inst_XXX
		self.inum = inum
		self.xcord = xcord
		self.ycord = ycord
		self.snum = snum
		self.itype = itype
		self.ftype = ftype

	def __repr__(self): # Returns this formatted String when printing and Instance object, useful for debugging purposes
		return "Inum: inst_{}, xcord: {} , ycord: {}, serialNum: {}, itype: {}, ftype: {}".format(self.inum,self.xcord,self.ycord,self.snum,self.itype,self.ftype)


class Net(): # Class that contains a net object, with a name and a list of insts

	def __init__(self,name):
		self.name = name
		self.insts = []
		

		
if __name__ == "__main__":
	main()


# One list per type of inst, note that all LUT are together
# listFDRE = []
# listLUT = []
# listRAMB = []
# listDSP = []
# listIBUF = []
# listOBUF = []
# listBUFGCE = []


# def fillInstsListTypes(): # This is where I fill the lists for each type of inst

# 	for x in listOfInstances: # listOfInstances contains all insts
# 		if x.itype == "FDRE":
# 			listFDRE.append(x)
# 		elif x.itype in "RAMB36E2": 	
# 			listRAMB.append(x)
# 		elif x.itype == "DSP48E2":
# 			listDSP.append(x)
# 		elif x.itype == "IBUF":
# 			listIBUF.append(x)
# 		elif x.itype == "OBUF":
# 			listOBUF.append(x)
# 		elif x.itype == "BUFGCE":
# 			listBUFGCE.append(x)
# 		elif "LUT" in x.itype:
# 			listLUT.append(x)

# def findMinsAndMaxs(xcord,ycord):

# 	global xmin,xmax,ymin,ymax	

# 	if xcord < xmin:
# 		xmin = xcord
# 	elif xcord > xmax:
# 		xmax = xcord

# 	if ycord < ymin:
# 		ymin = ycord
# 	elif ycord > ymax:
# 		ymax = ycord
