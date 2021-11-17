#!/usr/bin/python3
from math import pow, sqrt
import random

class MeanFunction:
	def __init__(self, data, preprocessing, processing, postprocessing):
		self.data = data
		self.preprocessing = preprocessing
		self.processing = processing
		self.postprocessing = postprocessing


def harmonicMean():
	data = 0                          # Stores sum of reciprocals
	def preprocessing(self, arr):
		self.length = len(arr)          # Stores the length
	def processing(self, num):
		self.data += 1/num              # Sums the reciprocals
	def postprocessing(self):
		return self.length / self.data	# Returns the final calculation
	
	return MeanFunction(data, preprocessing, processing, postprocessing)

# Added this because we get the mean for the standard deviation elsewhere so it's nice as its own function
def arithmeticMean(arr):
	s = 0
	for num in arr:
		s += num
	return s / len(arr)
def arithmeticMeanObj():
	data = 0                          # Stores the sum
	def preprocessing(self, arr):
		self.length = len(arr)          # Stores the length
	def processing(self, num):
		self.data += num                # Adds to the sum
	def postprocessing(self):
		return self.data / self.length  # returns the final calculation

	return MeanFunction(data, preprocessing, processing, postprocessing)

def geometricMean():
	data = 1
	def preprocessing(self, arr):
		self.length = len(arr)
	def processing(self, num):
		self.data *= num
	def postprocessing(self):
		return pow(self.data, 1/self.length)

	return MeanFunction(data, preprocessing, processing, postprocessing)

def rootMeanSquare():
	data = 0
	def preprocessing(self, arr):
		self.length = len(arr)
	def processing(self, num):
		self.data += num * num / self.length
	def postprocessing(self):
		return sqrt(self.data)

	return MeanFunction(data, preprocessing, processing, postprocessing)

# Separated this out since mode uses it when there's no unique values
def median(arr):
	l = len(arr)
	if(l % 2 == 0):
		return (arr[int(l / 2)] + arr[int(l / 2) - 1]) / 2
	else:
		return arr[int(l / 2)]

def medianObj():
	def preprocessing(self, arr):
		self.data = median(arr)
	def processing(self, num):
		return
	def postprocessing(self):
		return self.data
	
	return MeanFunction(0, preprocessing, processing, postprocessing)

def mode():
	def preprocessing(self, arr):
		occurences = {}
		someDuplicates = False
		for num in arr:
			if(num in occurences):
				occurences[num] += 1
				someDuplicates = True
			else:
				occurences[num] = 1

		if(not someDuplicates):
			self.data = median(arr)
		
		maxValue = occurences[arr[0]]
		maxKey = arr[0]
		for (key, value) in occurences.items():
			if(value > maxValue):
				maxValue = value
				maxKey = key
		self.data = maxKey
	def processing(self, num):
		return
	def postprocessing(self):
		return self.data

	return MeanFunction(0, preprocessing, processing, postprocessing)



# Leaving out mode because after the first iteration, all the values are floats and almost certainly unique so it ends up just being median again
meanFunctions = (
	(harmonicMean, "harmonic mean"),
	(geometricMean, "geometric mean"),
	(rootMeanSquare, "root mean square"),
	(arithmeticMeanObj, "arithmetic mean"),
	(medianObj, "median"),
	# (mode, "mode")
)



def superAvg(arr):
	if(len(arr) == 0):
		return [0] * len(meanFunctions)

	methods = []
	for i in range(len(meanFunctions)):
		methods.append(meanFunctions[i][0]())
		methods[i].preprocessing(methods[i], arr)

	for num in arr:
		for method in methods:
			method.processing(method, num)
	
	averages = []
	for method in methods:
		averages.append(method.postprocessing(method))
	
	return averages

def standardDeviation(arr):
	dist = 0

	mean = arithmeticMean(arr)
	for num in arr:
		dist += pow(mean - num, 2)
	return sqrt(dist / len(arr))

def superSuperAvg(arr, allowedDiff):
	# Things like median (and as a result, mode if no values are the same, in which case it returns median) require the array to be sorted
	# So I'll make sure nextArr always is, and here since we don't know if arr is, we'll sort it, in the future won't be necessary because nextArr is guaranteed sorted
	arr.sort()
	nextArr = superAvg(arr)
	nextArr.sort()
	iterations = 0
	while(True):
		iterations += 1

		if(standardDeviation(arr) < allowedDiff):
			break
		else:
			arr = nextArr
			nextArr = superAvg(arr)
			nextArr.sort()
	return (arr, iterations)




if __name__ == "__main__":
	print("Average functions are: [", end="")
	for type in meanFunctions[:-1]:
		print(f"{type[1]}, ", end="")
	print(f"{meanFunctions[-1][1]}]\n")


	arr = []
	for i in range(100):
		arr.append(random.randrange(1,1000))


	arr.sort()
	print(f"Initial array:\n\t{arr}\n")


	firstAverage = superAvg(arr)
	print(f"First super average:\n\t{firstAverage}")


	(finalAverages, iterations) = superSuperAvg(arr, 10 ** -5)
	finalCheckValue = arithmeticMean(finalAverages)
	print(f"After {iterations} iterations we reached a final average of ~{round(finalCheckValue, 4)}, or specifically the set:\n\t{finalAverages}\n")

	
	closest = [abs(finalCheckValue - firstAverage[0]), 0]
	for i in range(len(firstAverage)):
		if(abs(finalCheckValue - firstAverage[i]) < closest[0]):
			closest = [finalCheckValue - firstAverage[i], i]
	print(f"Closest was {firstAverage[closest[1]]}, the {meanFunctions[closest[1]][1]}.")
