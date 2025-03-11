def mergeStart(data, l, r, swapList):
	if l < r:
		m = (l + r) // 2

		mergeStart(data, l, m, swapList)
		mergeStart(data, m + 1, r, swapList)
		merge(data, l, m, r, swapList)

	return swapList

def merge(data, l, m, r, swapList):
	l2 = m + 1
	swapList.append([[l, m, m+1, r], "pointer"])
	if data[m] <= data[l2]:
		return
	
	while l <= m and l2 <= r:
		if data[l] < data[l2]:
			l += 1
		else:
			index = l2
			while index != l:
				data[index - 1], data[index] = data[index], data[index - 1]
				swapList.append([[index - 1, index], "swap"])
				index -= 1

			l += 1
			m += 1
			l2 += 1

	return swapList

data = [1, 4, 3, 9, 8, 3, 1,1, 4, 3, 9, 8, 3, 1, 1, 4, 3, 9, 8, 3, 1]
swapList = mergeStart([1, 4, 3, 9, 8, 3, 1,1, 4, 3, 9, 8, 3, 1, 1, 4, 3, 9, 8, 3, 1], 0, len(data) - 1, [])
print(swapList)


