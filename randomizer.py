import copy
import random
import re

from items_dictionary import items_list, items_template

def get_integer_value_for_task(rand):
	def replace_value(match):
		step = 1 if (match.group(3) in [ None, "", "0" ]) else int(match.group(3))
		result = rand.randrange(int(match.group(1)), int(match.group(2)) + 1, step)
		return str(result)

	return replace_value

def get_next_random_task_category(categories, items, rand):
	if categories is None:
		categories = items.keys()
	elif isinstance(categories, basestring):
		categories = [ categories ]
	elif isinstance(categories, list):
		categories = list(categories)

	rand.shuffle(categories)

	for category in categories:
		if len(items[category]) > 0:
			return category

	return None

def get_task_from_list(task_list, rand):
	task = rand.choice(task_list)
	task = re.sub("\\[([0-9]+)\\.\\.([0-9]+)(?:,([0-9]+))?\\]", get_integer_value_for_task(rand), task)

	return task

def randomize_card(template, items, seed):
	height = len(template)
	width = len(template[0])
	card = copy.deepcopy(template)
	shuffled_items = copy.deepcopy(items)

	rand = random.Random(seed)

	for category in shuffled_items:
		rand.shuffle(shuffled_items[category])

	template_indices = []

	for y in range(height):
		for x in range(width):
			index = (y, x)
			if card[y][x] is None:
				template_indices.append(index)
			else:
				template_indices.insert(0, index)

	for (y, x) in template_indices:
		category = get_next_random_task_category(card[y][x], shuffled_items, rand)
		card[y][x] = get_task_from_list(shuffled_items[category][0], rand)
		del shuffled_items[category][0]

	return card

def main():
	random_seed = random.randint(100000, 999999)
	bingo_height = len(items_template)
	bingo_width = len(items_template[0])

	random_card = randomize_card(items_template, items_list, random_seed)

	for y in range(bingo_height):
		for x in range(bingo_width):
			print random_card[y][x],

			if x >= bingo_width - 1:
				print ""
			else:
				print "\t",

	print "Seed:", random_seed

main()