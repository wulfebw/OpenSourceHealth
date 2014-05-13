
# populates database with test information

from projects.models import Project 
from categories.models import Category, Group
from random import randint
from datetime import datetime


# alphabet
alpha = []
begin = ord('a')
end = ord('z')
for num in xrange(begin, end + 1):
	alpha.append(chr(num))

# 10 groups '(0-9) group'
for num in range(10):
	group_name = '{0} group'.format(num)
	g = Group(name = group_name)
	g.save()

# 52 categories '(A-Z) category'

for letter in alpha:
	group_num = randint(0,9)
	group_name = str(group_num) + ' group'
	group = Group.objects.get(name = group_name)
	category_name = '{0} category'.format(letter.upper())
	c = Category(name = category_name, group = group)
	c.save()

for num in range(2):
	for letter in alpha:
		cat_letter = alpha[randint(0,25)].upper()
		cat_name = cat_letter + ' category'
		category = Category.objects.get(name = cat_name)
		if num == 0:
			proj_name = letter + ' project'
		else:
			proj_name = letter.upper() + ' project'
		rating = randint(0,100)
		p = Project(
				name 				= proj_name,
				github_repo			= "wulfebw/api_test",
				category			= category,
				rating				= rating,
				description 		= "desc",
				website_url 		= "http://www.google.com",
				documentation_url 	= "http://www.google.com",
				bug_tracker_url		= "http://www.google.com",
				mailing_list_url	= "http://www.google.com",
				github_contributors	= 2,
				github_watchers		= 3,
				github_forks		= 4,
				github_issues		= 5,
				last_commit_date	= datetime.now(),
				first_commit_date	= datetime.now(),
				)
		p.save()



