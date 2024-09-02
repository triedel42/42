#!/usr/bin/env
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    projects_import.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    Monorepo creator for 42 projects               +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#                                                      #+#    #+#              #
#                                                     ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import re

'''
Clones all projects from `projects_file` that is formatted as follows

	<project-name-1>
	<url-1>

	<project-name-2>
	<url-2>

	...

Afterwards removes all '.git' folders
'''
def projects_clone(projects_file: str):
	name = None
	counter = 0
	for line in open(projects_file):
		# ignore comments
		if not line or line.startswith('#'):
			continue
		# remove newlines from line
		line = line.replace('\n', '')
		# process either name or url
		if not name:
			name = line
		else:
			name = name.replace(' ', '_')
			dstname = f'{str(counter).zfill(2)}_{name}'
			os.system(f'git clone {line} ./{dstname}')
			os.system(f'rm -rf ./{dstname}/.git')
			# prepare next project
			name = None
			counter += 1

def header_remove(path):
	if not path.endswith(
		('.c', '.h', '.cpp', '.hpp', '.tpp', 'Makefile', '.mk')):
		return
	with open(path) as f:
		lines = f.readlines()
	while lines and re.match(r'^(\/\*|#\s|\s)', lines[0]):
		lines.pop(0)
	with open(path, 'w') as f:
		lines = f.writelines(lines)


def projects_sanitize():
	for root, dirs, files in os.walk('.'):
		for f in files:
			path = f'{root}/{f}'
			print(f'Removing header from {path}')
			header_remove(path)

if __name__ == '__main__':
	from sys import argv

	if len(argv) < 2:
		exit('Usage: ./projects.py <projects-file>')

	projects_clone(argv[1])
	projects_sanitize()
