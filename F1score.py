def F1score(a, b, c):
	Precision = a/b
	Recall = a/c
	F1Score = 2*(Precision*Recall)/(Precision+Recall)
	print("Precision(정확률)")
	print(Precision)
	print("Recall(재현률)")
	print(Recall)
	print("F1Score")
	print(F1Score)

F1score(1947, 5000, 8717)

Precision = 1947/5000
Recall = 1947/8717
F1Score = 2*(Precision*Recall)/(Precision+Recall)

print(Precision)
print(Recall)
print(F1Score)

Precision2 = 745/5000
Recall2 = 745/8717
F1Score2 = 2*(Precision2*Recall2)/(Precision2+Recall2)

print(Precision2)
print(Recall2)
print(F1Score2)

Precision3 = 2485/5000
Recall3 = 2485/8717
F1Score3 = 2*(Precision3*Recall3)/(Precision3+Recall3)

print(Precision3)
print(Recall3)
print(F1Score3)
