#!/usr/bin/python3
from math import pow, sqrt
import random

def harmonicMean(arr):
	denominator = 0
	for num in arr:
		denominator += 1 / num
	return len(arr) / denominator

def geometricMean(arr):
	gm = 1
	gmPower = 1 / len(arr)
	for num in arr:
		gm *= pow(num, gmPower)
	return gm

def rootMeanSquare(arr):
	rms = 0
	l = len(arr)
	for num in arr:
		rms += num * num / l
	return sqrt(rms)

def arithmeticMean(arr):
	s = 0
	for num in arr:
		s += num
	return s / len(arr)

def median(arr):
	return arr[int(len(arr) / 2)]

def mode(arr):
	occurences = {}
	someDuplicates = False
	for num in arr:
		if(num in occurences):
			occurences[num] += 1
			someDuplicates = True
		else:
			occurences[num] = 1

	if(not someDuplicates):
		return median(arr)
	
	maxValue = occurences[arr[0]]
	maxKey = arr[0]
	for (key, value) in occurences.items():
		if(value > maxValue):
			maxValue = value
			maxKey = key
	return maxKey

# Leaving out mode because after the first iteration, all the values are floats and almost certainly unique so it ends up just being median again
averageFunctions = (
	(harmonicMean, "harmonic mean"),
	(geometricMean, "geometric mean"),
	(rootMeanSquare, "root mean square"),
	(arithmeticMean, "arithmetic mean"),
	(median, "median"),
	# (mode, "mode")
)

def superAvg(arr):
	if(len(arr) == 0):
		return [0] * len(averageFunctions)
	averages = []
	for (method, name) in averageFunctions:
		averages.append(method(arr))
	return averages

def oldSuperAvg(arr):
	if(len(arr) == 0):
		return [0, 0, 0, 0, 0]
	median = arr[int(len(arr)/2)]
	product = 1
	sum = 0
	geometricMean = 1
	geometricMeanPower = 1/len(arr)
	harmonicDenominator = 0
	rootMeanSquare = 0
	for i in arr:
		product *= i
		sum += i
		geometricMean *= pow(i, geometricMeanPower)
		harmonicDenominator += 1/i
		rootMeanSquare += i * i / len(arr)

	arithmeticMean = sum / len(arr)
	harmonicMean = len(arr) / harmonicDenominator
	rootMeanSquare = sqrt(rootMeanSquare)
	return [harmonicMean, geometricMean, rootMeanSquare, arithmeticMean, median] 

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
	arr = []
	for i in range(100):
		arr.append(random.randrange(1,1000))

	arr.sort()
	print(f"initial array:\n\t{arr}\n")

	print("Average functions are: [", end="")
	for type in averageFunctions[:-1]:
		print(f"{type[1]}, ", end="")
	print(f"{averageFunctions[-1][1]}]\n")

	firstAverage = superAvg(arr)
	print(f"First super average:\n\t{firstAverage}")
	(finalAverages, iterations) = superSuperAvg(arr, 10 ** -5)
	print(f"After {iterations} iterations we reached a final set of averages of:\n\t{finalAverages}\n")

	finalCheckValue = arithmeticMean(finalAverages)
	closest = [abs(finalCheckValue - firstAverage[0]), 0]
	for i in range(len(firstAverage)):
		if(abs(finalCheckValue - firstAverage[i]) < closest[0]):
			closest = [finalCheckValue - firstAverage[i], i]
	print(f"Closest was {firstAverage[closest[1]]}, the {averageFunctions[closest[1]][1]}.")
	
