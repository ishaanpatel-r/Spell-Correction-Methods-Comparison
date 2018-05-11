
# importies!
from itertools import islice, tee

# opens up .txt files
# returns: list of words
def txt2list(path):
	with open('data/' + path, 'r') as f:
		list_ = f.readlines()
	new_list = []
	for each in list_:
		new_list += [each.replace('\n', '')]
	return new_list

# technique one: N-Gram 
def ngram_distance(main_word, check_word):

	def get_ngram(word, N):
		return ['#' + word[0]] + list(zip(*(islice(seq, index, None) 
			for index, seq in enumerate(tee(word, N))))) + [word[-1] + '#']

	# get n-gram for words
	ngram_main_word = get_ngram(main_word, 2)
	ngram_check_word = get_ngram(check_word, 2)

	# list comparison to get overlapping grams
	overlapping_grams = len(set.intersection(set(ngram_main_word), set(ngram_check_word)))

	# n-gram distance formula
	ngram_distance = (len(ngram_main_word) + len(ngram_check_word) - (2 * overlapping_grams))

	return ngram_distance

# technique two: local edit distance 
# [m, i, d, r] -> [0, 1, 1, 1]
def local_edit_distance(main_word, check_word):

	len_1=len(main_word)

	len_2=len(check_word)

	# creates empty base matrix
	x =[[0]*(len_2+1) for _ in range(len_1+1)]

	# fills columns
	for i in range(0,len_1+1): #initialization of base case values
	    x[i][0]=i
	# fills rows
	for j in range(0,len_2+1):
	    x[0][j]=j

	for i in range (1,len_1+1):
	    for j in range(1,len_2+1):
	        if main_word[i-1]==check_word[j-1]:
	            x[i][j] = x[i-1][j-1] 
	        else:
	            x[i][j]= min(x[i][j-1], x[i-1][j], x[i-1][j-1]) + 1

	return x[i][j]

# technique three: global edit distance
# [m, i, d, r] -> [1, -1, -1, -1]
def global_edit_distance(main_word, check_word):

	len_1=len(main_word)

	len_2=len(check_word)

	# creates empty base matrix
	x =[[0]*(len_2+1) for _ in range(len_1+1)]

	# fills columns
	for i in range(0,len_1+1): #initialization of base case values
	    x[i][0]=-i
	# fills rows
	for j in range(0,len_2+1):
	    x[0][j]=-j

	for i in range (1,len_1+1):
	    for j in range(1,len_2+1):
	        if main_word[i-1]==check_word[j-1]:
	            x[i][j] = x[i-1][j-1] + 1
	        else:
	            x[i][j]= max(x[i][j-1], x[i-1][j], x[i-1][j-1]) - 1

	# pprint(x)
	return x[i][j]

# technique four: custom edit distance
# [m, i, d, r] -> [-5, 4, 1, 5]
def custom_edit_distance(main_word, check_word):

	
	len_1=len(main_word)

	len_2=len(check_word)

	# creates empty base matrix
	x =[[0]*(len_2+1) for _ in range(len_1+1)]

	# fills columns
	for i in range(0,len_1+1): #initialization of base case values
	    x[i][0]=i
	# fills rows
	for j in range(0,len_2+1):
	    x[0][j]=j

	for i in range (1,len_1+1):
	    for j in range(1,len_2+1):
	        if main_word[i-1]==check_word[j-1]:
	            x[i][j] = x[i-1][j-1]  - 5
	        else:
	            x[i][j]= min(x[i][j-1] + 4, x[i-1][j] + 1, x[i-1][j-1] + 5)

	return x[i][j]

# technique five: soundex method
def soundex_comparison(main_word, check_word):

	soundex_replacement_table = {
			'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 0,
			'f' : 1, 'g' : 2, 'h' : 0, 'i' : 0, 'j' : 2,
			'k' : 2, 'l' : 4, 'm' : 5, 'n' : 5, 'o' : 0,
			'p' : 1, 'q' : 2, 'r' : 6, 's' : 2, 't' : 3,
			'u' : 0, 'v' : 1, 'w' : 0, 'x' : 2, 'y' : 0,
			'z' : 2
		}

	def f7(seq):
	    seen = set()
	    seen_add = seen.add
	    return [x for x in seq if not (x in seen or seen_add(x))]

	def get_soundex(word):

		# replace each character with soundex except first
		soundex = [word[0]] + [soundex_replacement_table[i] for i in word[1:]]

		# remove consequent duplicates
		soundex = f7(soundex)

		# remove all 0s
		soundex = [i for i in soundex if i != 0]

		return soundex

	score = 0
	main_word_soundex = get_soundex(main_word)
	check_word_soundex = get_soundex(check_word)
	
	if len(main_word_soundex) == len(check_word_soundex):
		score += 1
	else:
		score -= 1

	if len(main_word) - 2 < len(check_word) < len(main_word) + 2:
		score += 1
	else:
		score -= 1

	return score

# evaluations here
def evaluations():

	# flatten collected words for recall & precision evaluation
	flatten = lambda l: [item for sublist in l for item in sublist]

	# NGRAM : score 100, comparison <
	print()
	print()
	all_trues = {k : [] for k in misspell_list}
	print('----------------NGRAM----------------')
	correct_responses = 0
	recall_check = 0
	for i in range(0, len(misspell_list)):
		score = 100
		correct_word = misspell_list[i]
		actual_correct = correct_list[i]

		# gets best match (to measure accuracy)
		for each_dictionary_word in dictionary_list:
			new_score = ngram_distance(misspell_list[i], each_dictionary_word)
			if new_score < score:
				score = new_score
				correct_word = each_dictionary_word

		# gets each match at score of best match (to measure precision and recall)
		for each_dictionary_word in dictionary_list:
			new_score = ngram_distance(misspell_list[i], each_dictionary_word)
			if new_score == score:
				all_trues[misspell_list[i]] += [each_dictionary_word]
		
		if actual_correct in all_trues[misspell_list[i]]:
			recall_check += 1

		# prints results
		if correct_word == actual_correct:
			print(misspell_list[i], correct_word, actual_correct)
			correct_responses += 1
		else:
			print(misspell_list[i], correct_word, actual_correct, '*')
	# get accuracy, precision and recall
	print()
	accuracy = correct_responses/len(misspell_list)
	print('Accuracy', accuracy)
	precision = correct_responses/len(flatten([i for i in [v for k, v in all_trues.items()]]))
	print('Precision', precision)
	recallment = recall_check/len(misspell_list)
	print('Recall', recallment)
	F1 = 2 * ((precision*recallment)/(precision+recallment))
	print('F1', F1)



	# GED: score -100, comparison >
	print()
	print()
	all_trues = {k : [] for k in misspell_list}
	print('----------------Global Edit Distance----------------')
	correct_responses = 0
	recall_check = 0
	for i in range(0, len(misspell_list)):
		score = -100
		correct_word = misspell_list[i]
		actual_correct = correct_list[i]

		# gets best match (to measure accuracy)
		for each_dictionary_word in dictionary_list:
			new_score = global_edit_distance(misspell_list[i], each_dictionary_word)
			if new_score > score:
				score = new_score
				correct_word = each_dictionary_word

		# gets each match at score of best match (to measure precision and recall)
		for each_dictionary_word in dictionary_list:
			new_score = global_edit_distance(misspell_list[i], each_dictionary_word)
			if new_score == score:
				all_trues[misspell_list[i]] += [each_dictionary_word]
		
		if actual_correct in all_trues[misspell_list[i]]:
			recall_check += 1

		# prints results
		if correct_word == actual_correct:
			print(misspell_list[i], correct_word, actual_correct)
			correct_responses += 1
		else:
			print(misspell_list[i], correct_word, actual_correct, '*')
	# get accuracy, precision and recall
	print()
	accuracy = correct_responses/len(misspell_list)
	print('Accuracy', accuracy)
	precision = correct_responses/len(flatten([i for i in [v for k, v in all_trues.items()]]))
	print('Precision', precision)
	recallment = recall_check/len(misspell_list)
	print('Recall', recallment)
	F1 = 2 * ((precision*recallment)/(precision+recallment))
	print('F1', F1)




	# LED: score 100, comparison <
	print()
	print()
	all_trues = {k : [] for k in misspell_list}
	print('----------------Local Edit Distance----------------')
	correct_responses = 0
	recall_check = 0
	for i in range(0, len(misspell_list)):
		score = 100
		correct_word = misspell_list[i]
		actual_correct = correct_list[i]

		# gets best match (to measure accuracy)
		for each_dictionary_word in dictionary_list:
			new_score = local_edit_distance(misspell_list[i], each_dictionary_word)
			if new_score < score:
				score = new_score
				correct_word = each_dictionary_word

		# gets each match at score of best match (to measure precision and recall)
		for each_dictionary_word in dictionary_list:
			new_score = local_edit_distance(misspell_list[i], each_dictionary_word)
			if new_score == score:
				all_trues[misspell_list[i]] += [each_dictionary_word]
		
		if actual_correct in all_trues[misspell_list[i]]:
			recall_check += 1

		# prints results
		if correct_word == actual_correct:
			print(misspell_list[i], correct_word, actual_correct)
			correct_responses += 1
		else:
			print(misspell_list[i], correct_word, actual_correct, '*')
	# get accuracy, precision and recall
	print()
	accuracy = correct_responses/len(misspell_list)
	print('Accuracy', accuracy)
	precision = correct_responses/len(flatten([i for i in [v for k, v in all_trues.items()]]))
	print('Precision', precision)
	recallment = recall_check/len(misspell_list)
	print('Recall', recallment)
	F1 = 2 * ((precision*recallment)/(precision+recallment))
	print('F1', F1)



	# CED: score 100, comparison <
	print()
	print()
	all_trues = {k : [] for k in misspell_list}
	print('----------------Custom Edit Distance----------------')
	correct_responses = 0
	recall_check = 0
	for i in range(0, len(misspell_list)):
		score = 100
		correct_word = misspell_list[i]
		actual_correct = correct_list[i]

		# gets best match (to measure accuracy)
		for each_dictionary_word in dictionary_list:
			new_score = custom_edit_distance(misspell_list[i], each_dictionary_word)
			if new_score < score:
				score = new_score
				correct_word = each_dictionary_word

		# gets each match at score of best match (to measure precision and recall)
		for each_dictionary_word in dictionary_list:
			new_score = custom_edit_distance(misspell_list[i], each_dictionary_word)
			if new_score == score:
				all_trues[misspell_list[i]] += [each_dictionary_word]
		
		if actual_correct in all_trues[misspell_list[i]]:
			recall_check += 1

		# prints results
		if correct_word == actual_correct:
			print(misspell_list[i], correct_word, actual_correct)
			correct_responses += 1
		else:
			print(misspell_list[i], correct_word, actual_correct, '*')
	# get accuracy, precision and recall
	print()
	accuracy = correct_responses/len(misspell_list)
	print('Accuracy', accuracy)
	precision = correct_responses/len(flatten([i for i in [v for k, v in all_trues.items()]]))
	print('Precision', precision)
	recallment = recall_check/len(misspell_list)
	print('Recall', recallment)
	F1 = 2 * ((precision*recallment)/(precision+recallment))
	print('F1', F1)



	# Soundex: score 0, comparison >
	print()
	print()
	all_trues = {k : [] for k in misspell_list}
	print('----------------Soundex----------------')
	correct_responses = 0
	recall_check = 0
	for i in range(0, len(misspell_list)):
		score = 0
		correct_word = misspell_list[i]
		actual_correct = correct_list[i]

		# gets best match (to measure accuracy)
		for each_dictionary_word in dictionary_list:
			new_score = soundex_comparison(misspell_list[i], each_dictionary_word)
			if new_score > score:
				score = new_score
				correct_word = each_dictionary_word

		# gets each match at score of best match (to measure precision and recall)
		for each_dictionary_word in dictionary_list:
			new_score = soundex_comparison(misspell_list[i], each_dictionary_word)
			if new_score == score:
				all_trues[misspell_list[i]] += [each_dictionary_word]
		
		if actual_correct in all_trues[misspell_list[i]]:
			recall_check += 1

		# prints results
		if correct_word == actual_correct:
			print(misspell_list[i], correct_word, actual_correct)
			correct_responses += 1
		else:
			print(misspell_list[i], correct_word, actual_correct, '*')
	# get accuracy, precision and recall
	print()
	accuracy = correct_responses/len(misspell_list)
	print('Accuracy', accuracy)
	precision = correct_responses/len(flatten([i for i in [v for k, v in all_trues.items()]]))
	print('Precision', precision)
	recallment = recall_check/len(misspell_list)
	print('Recall', recallment)
	F1 = 2 * ((precision*recallment)/(precision+recallment))
	print('F1', F1)


if __name__ == "__main__":

	# read all misspelled spellings
	misspell_list = txt2list('misspell.txt')

	# read all dictionary words
	dictionary_list = txt2list('dictionary.txt')

	# read all correct words
	correct_list = txt2list('correct.txt')

	evaluations()

	