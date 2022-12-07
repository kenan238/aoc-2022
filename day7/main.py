# aoc 2022 day 7
# an entire file system 😭
# this code is a bit messy with repeating things
# but hey this is aoc so if it works it works
# ill try comment though

class File:
	def __init__(self, name, size, parent):
		self.sz = size
		self.name = name
		self.parent = parent
	def stringify(self):
		return f"{self.sz} {self.name}"
	def getTotalSum(self):
		return self.sz
	def __lt__(self, other): # to sort properly
		return self.getTotalSum() < other.getTotalSum()

class Folder:
	def __init__(self, name, parent):
		self.files = []
		self.name = name
		self.parent = parent
	def add(self, file):
		self.files.append(file)
	def find(self, f):
		for file in self.files:
			if file.name == f:
				return file
		return None
	def stringify(self):
		return f"dir {self.name}"
	def getTotalSum(self):
		if self.files == []:
			return 0

		tsum = 0
		for file in self.files:
			ftsum = file.getTotalSum()
			tsum += ftsum
		return tsum
	def getFilesThatMeetReq(self, minSize): # checks for files that have a total sum of <= minSize
		valid = []
		for file in self.files:
			ftsum = file.getTotalSum()
			if ftsum <= minSize and isinstance(file, Folder):
				valid.append(file)
			itsValids = []
			if isinstance(file, Folder):
				itsValids = file.getFilesThatMeetReq(minSize)
			valid.extend(itsValids)
		return valid

	def getFilesThatHaveAtleastSize(self, size): # same as getFilesThatMeetReq but modified to do >= instead
		valid = []
		for file in self.files:
			ftsum = file.getTotalSum()
			if ftsum >= size and isinstance(file, Folder):
				valid.append(file)
			itsValids = []
			if isinstance(file, Folder):
				itsValids = file.getFilesThatHaveAtleastSize(size)
			valid.extend(itsValids)
		return valid
	def __lt__(self, other): # to sort properly
		return self.getTotalSum() < other.getTotalSum()


class Filesystem:
	def __init__(self):
		self.root = Folder('root', None)
	def createFolderIfNotExists(self, folderName, path):
		if folderName == "/":
			return
		if path == []:
			prepared = Folder(folderName, self.root)
			for file in self.root.files:
				if file.name == folderName:
					return
			self.root.files.append(prepared)
		curNode = self.root
		pathIndex = 0
		while True:
			try:
				foundNode = curNode.find(path[pathIndex])
			except IndexError:
				break
			else:
				curNode = foundNode
			pathIndex += 1
		for f in curNode.files:
			if f.name == folderName:
				return
		curNode.files.append(Folder(folderName, curNode))
		while curNode.parent != None:
			curNode = curNode.parent
		self.root = curNode

	def createFileIfNotExists(self, fileName, size, path):
		if fileName == "/":
			return
		if path == []:
			self.root.add(File(fileName, size, self.root))
			return
		curNode = self.root
		pathIndex = 0
		while True:
			try:
				foundNode = curNode.find(path[pathIndex])
			except IndexError:
				break
			if foundNode == None:
				break
			else:
				curNode = foundNode
			pathIndex += 1
		curNode.files.append(File(fileName, size, curNode))
		while curNode.parent != None:
			curNode = curNode.parent
		self.root = curNode
		
	def listRecursive(self, folder, depth): # internal function for listRoot
		if folder.files == []:
			return
		for n in folder.files:
			print(" " * depth, n.stringify())
			if type(n) == Folder:
				self.listRecursive(n, depth + 1)

	def listRoot(self):
		if self.root.files == []:
			print("....")
			return
		for n in self.root.files:
			print(n.stringify())
			if isinstance(n, Folder):
				self.listRecursive(n, 0)

def quickSumUp(files): # utility
	s = 0
	for f in files:
		s += f.getTotalSum()
	return s

fs = Filesystem()

with open("input.txt", "r") as f:
	lines = f.readlines()
	workingDirectory = [] # store all levels
	collectedLsOutput = [] # ls output
	isCollecting = False # are we collecting ls output?

	for line in lines:
		if line[0] == "$":
			if isCollecting:
				for output in collectedLsOutput: # process output 
					splittedOutput = output.split(" ")
					if not splittedOutput[0].isdigit():
						fs.createFolderIfNotExists(splittedOutput[1], workingDirectory)
					else:
						fs.createFileIfNotExists(splittedOutput[1], int(splittedOutput[0]), workingDirectory)
				collectedLsOutput = []
				isCollecting = False
			command = line[2:len(line) - 1]
			if command.split(" ")[0] != "ls":
				arg = command.split(" ")[1]
				if command.split(" ")[0] == "cd":
					if arg == "..":
						workingDirectory.pop()
					elif arg != "/":
						fs.createFolderIfNotExists(arg, workingDirectory)
						workingDirectory.append(arg)
			elif command.split(" ")[0] == "ls": # ls behaviour
				isCollecting = True
		elif isCollecting: # collect output
			collectedLsOutput.append(line[0:len(line) - 1])
		if lines[-1] == line: # force process on last line
			collectedLsOutput.pop()
			collectedLsOutput.append(line)
			for output in collectedLsOutput: # process output (repeated code)
					splittedOutput = output.split(" ")
					if not splittedOutput[0].isdigit():
						fs.createFolderIfNotExists(splittedOutput[1], workingDirectory)
					else:
						fs.createFileIfNotExists(splittedOutput[1], int(splittedOutput[0]), workingDirectory)
# fs.listRoot() uncomment to see fs
print('part 1', quickSumUp(fs.root.getFilesThatMeetReq(100000)))
TOTAL_SIZE = 70000000
UPDATE_SIZE = 30000000
used = fs.root.getTotalSum()
unused = TOTAL_SIZE - used
smallestSizeToUpdate = UPDATE_SIZE - unused
matches = fs.root.getFilesThatHaveAtleastSize(smallestSizeToUpdate)
matches.sort() # check Folder's __lt__ and File's __lt__ for sorting behaviour
print('part 2', matches[0].getTotalSum())