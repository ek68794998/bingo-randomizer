import copy
import random
import re

from SAMPLE_items_dictionary import items_list

def get_random_task(task_list, rand):
	task = rand.choice(task_list)
	task = re.sub("\\[([0-9]+)\\.\\.([0-9]+)(?:,([0-9]+))?\\]", get_random_task_integer(rand), task)

	return task

def get_random_task_integer(rand):
	def replace_value(match):
		step = 1 if (match.group(3) in [ None, "", "0" ]) else int(match.group(3))
		result = rand.randrange(int(match.group(1)), int(match.group(2)) + 1, step);
		return str(result)

	return replace_value

def randomize_card(width, height, items, seed):
	category_keys = items.keys()
	category_item_count = max([ len(items[category_key]) for category_key in category_keys ])
	categories = [ copy.deepcopy(items[category_key]) for category_key in category_keys ]

	for category in categories:
		rand = random.Random(seed)
		rand.shuffle(category)

	chosen_squares = []

	rand = random.Random(seed)
	selection_index = 0
	while selection_index < category_item_count:
		category_index = 0
		while category_index < len(categories):
			if selection_index < len(categories[category_index]):
				chosen_squares.append(get_random_task(categories[category_index][selection_index], rand))

			category_index += 1

		selection_index += 1

	return chosen_squares[0:(width * height)]

random_seed = random.randint(100000, 999999)
bingo_height = 5
bingo_width = 5

random_card = randomize_card(bingo_width, bingo_height, items_list, random_seed)

for y in range(bingo_height):
	for x in range(bingo_width):
		print random_card[y * bingo_height + x],

		if x >= bingo_width - 1:
			print ""
		else:
			print "\t",

print "Seed:", random_seed