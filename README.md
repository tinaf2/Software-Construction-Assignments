# CS35L-Assignments
Scripting assignments for UCLA CS 35L: Software Construction Lab

Description of each file:

shuf.py: Python script implementing the GNU shuf command that is part of GNU Coreutils.

topo-order-commits.py: This Python script designed for analyzing the commit history in a Git repository. 
                        It first locates the top-level `.git` directory, then extracts local branch names from the repository's structure. 
                        The script builds a commit graph as a directed acyclic graph (DAG), where each commit is a node, and edges represent parent-child relationships, 
                        including handling of merge commits. It performs a depth-first search to establish these relationships and then generates a topologically ordered list of commits. 
                        This ordering ensures that each commit appears before its descendants in the output, which is formatted to include branch names for commits that
                        are branch heads and special markers for transitions between segments of the repository's history. The script operates deterministically, 
                        solely using Python's standard library, without invoking external Git commands.

justone: Python script that displays the difference from the previous and current commit, assuming the repository is what an ordinary Git command would use

compare-releases: Python script that displays the difference between two tzdb releases given as arguments to the command. 
                   For example, compare-releases 2022f 2022g should output the difference between tzdb release 2022f and tzdb release 2022g.
                   
tzcount: Python script that postprocesses the output of git log and outputs a simple report of time zones and number of commits from that time zone. 
         Each line of output should look something like “-0500 1802”, meaning there were 1802 commits from the −0500 time zone. 
         Output is sorted numerically by its first (numeric timezone) column.

myspell: Bash script implementation of a spell checker that reads from standard input and outputs misspelled words to standard output. 
         Uses Unix/Linux command-line utilities including tr, sort, and comm.
