**CMSI 486** Introduction to Database Systems, Fall 2020

# Assignment 0928
Before diving fully into database systems per se, we make one stopover “under the hood” by looking at data management by working with files alone. The premise here is that all database systems, regardless of model, philosophy, or generation, ultimately store their data in files. Thus, it is of value to explore what it takes to work with files _directly_—in a way, to write the very beginnings of your own database system.

## Background Reading
Continue to draw inspiration from the [Kaggle](https://www.kaggle.com/datasets) and [Awesome Public Datasets](https://github.com/awesomedata/awesome-public-datasets) collections for this assignment—and this time, keep a closer eye on datasets that have files which you can actually work with along the lines of this assignment. As before the [Netflix Prize](https://www.kaggle.com/netflix-inc/netflix-prize-data) dataset is used as the case study for the assignment’s accompanying examples—you may not use it for your own submission, but by all means download these files and try out [the given examples](./netflix-prize-example) for yourself.

Direct assistance for the action items in this assignment can be found (among other places) in:
* [Finding Things](https://swcarpentry.github.io/shell-novice/07-find/) on the command line
* Manual pages for [grep](https://man7.org/linux/man-pages/man1/grep.1p.html) and [wc](https://man7.org/linux/man-pages/man1/wc.1p.html)
* [A tutorial](https://www.grymoire.com/Unix/Awk.html) on [awk](https://man7.org/linux/man-pages/man1/awk.1p.html)

Also of use would be programming references for I/O and file processing libraries of whatever programming language you might choose, such as:
* [Python](https://docs.python.org/3.7/tutorial/inputoutput.html#reading-and-writing-files) (take a look at their [csv](https://docs.python.org/3.7/library/csv.html) library too)
* [NodeJS](https://nodejs.org/api/fs.html)—particularly handy if your dataset’s files are in [JSON format](https://stackabuse.com/reading-and-writing-json-files-with-node-js/)
* [Java](https://docs.oracle.com/javase/tutorial/essential/io/file.html)—just don’t tell Toal (lest you become a…tattle-Toal?)
* (though I doubt any of you will pick this one) [C](https://en.wikipedia.org/wiki/C_file_input/output)—unless you’re taking this as a challenge and want to legit say [“Hold my avocado 🥑”](https://www.thrillist.com/news/nation/hold-my-avocado-meme-origin)

Of course, for technologies like these, you’re likely to find a lot of additional supplements on the web.

The Elmasri & Navathe book touches on this conceptually in their Chapter 1 section on “Advantages of Using the DBMS Approach.” If you want a peek into how database management systems _do_ organize their data files in order to do what they do efficiently, you can skim Part 7 _File Structures, Hashing, Indexing, and Physical Database Design_ to get an idea of how this is done. Think of this assignment as a microcosm of that material.

In Ullman’s [Foundations of Computer Science Chapter 8](http://infolab.stanford.edu/~ullman/focs/ch08.pdf), Sections 8.4–8.6 provide similar material, though on a more abstract data structure level. Still, the data structures mentioned there do need to be converted into actual files somewhere along the way so it remains quite applicable and relevant.

## For Submission: File Database Mini-Stack
For this assignment, give yourselves and your groups a taste of what it would be like to work with data at a file level by taking a stab at performing the database operations described below.

### Warm Up to the Challenge: _netflix-practice.md_
Walk through the [Netflix Prize file database mini-stack case study](./netflix-prize-example)—ideally together as a group, so you can help each other through each example—and do a little prep by doing some freeform exploration of that data using the techniques shown therein. Ideally, everyone in the group can download and preprocess the data firsthand; if this is not feasible for some, designate one or more group members to serve as “hosts” for your work, and collaborate around a screenshare with them.

In a Markdown file on your repository called _netflix-practice.md_, do the following:
1. Write up two (2) movie queries—things like movies with certain titles or title patterns, movies released on one or more given years, etc. Provide those queries and show their results (or a subset of them, if there are too many to list).
2. Pick a viewer at random and build their complete “review profile”—actually track down the titles/years of the movies they reviewed and how they rated them. Provide the commands used to build this profile and show the results. State conclusions that your group thinks can be drawn about that viewer’s preferences and tastes.
3. Pick a movie at random and collate its review scores. Provide the commands used to gather this data and show the results. Can you draw any conclusions about the quality of this movie based on the review scores that it received?

### Let There Be…Data! (_about.md_, _.gitignore_)
After you’ve gotten some practice with the Netflix Prize data, you’ll now need to work with another dataset in all its glory (not just mimicking its structure), so choose well! Pre-visualize the kinds of files that you can work with based on the requested operations, alongside the language that you would be inclined to use for the operations that call for a little programming. Make sure to keep that in mind alongside, of course, also still picking a dataset whose core content is interesting to you.

This assignment is most effective when you implement the requested operations on that dataset _in its entirety_ (just like with the Netflix Prize case study)—so yes you’ll have to be conscious of how much disk space you have available—and get to know how the files are organized, formatted, and structured. Ideally, everyone in the group will be able to work with the files directly; however not everyone may have enough capacity to work with the entire dataset on their local computer so please be open to sharing your screen and allowing for some teammates to drive in order to give everyone that firsthand experience.

As another option for computing resources, the AWS Educate classroom for this course has also been activated and you may opt to use it in order to store your files or even work with them via an Elastic Compute Cloud (EC2) virtual machine. This is a good time to learn how to watch your credits usage and get a feel for how much you can afford to use while still having enough left for the rest of the semester.

In any case, describe your dataset and potential applications for it in a file called _about.md_. This can be very similar to the _about.md_ that you wrote for the database fiddle assignment. Make sure that _about.md_ also has links to the actual dataset, for anyone who would like to download a copy for themselves.

Whatever you do, do _not_ commit the datasets to GitHub. This is one case where GitHub isn’t a good fit.

To guarantee that this does not accidentally happen, _edit the `.gitignore` file_ so that it makes your repository ignore the files that comprise your chosen dataset.

### Feel the Power: _queries.md_
Once you have the data at your fingertips, it’s time to play database. Seek to implement the following operations. Refer back to the examples in the [netflix-prize-example](./netflix-prize-example) folder as needed. Just remember that _datasets will differ from each other_, so don’t limit yourself exclusively to what you see in the case study. In particular, note that the case study uses Python for custom programming work—this will not necessarily be the best fit for the dataset that you choose.

As before, it is also useful to contextualize things by envisioning an application that would use your chosen dataset. Having such an application in mind will help fuel ideas for the specific operations to implement in the following categories. Place query descriptions and commands in a file called _queries.md_ and commit relevant source code directly to the repository (referring to them as needed in _queries.md_):

1. Query by pure command (`grep`, `awk`)
2. Count query by pure command (`grep`, `awk`, `wc`)
3. Query by a program that scans the data file(s)
4. Query by pure command facilitated by pre-processing (with accompanying preprocessor of course)
5. “Compound” query that requires a manual combination of commands or programs

### Take Stock of Your Mini-Stack: _report.md_
Finally, finish up the exercise by writing a small technical report on everything that you did. Call this document _report.md_ and answer the following questions:
1. Which operations/commands/programs were the most difficult to implement? Which were easiest? Provide brief rationales for your responses.
2. In what way do the size and ordering of your data files affect the speed of an individual operation?
    - To support your answer, use the `time` command to get an objective reading for how long certain operations take
    - Choose your timed operations in a way that illustrates how size and ordering affects performance
3. Is there a correlation between the ease of implementation and performance? (i.e., are the hardest operations to implement always the slowest ones? vice versa? or is there no relationship at all?)

### Operational Directives/Suggestions
- Make sure to divide the implementation work relatively evenly within your group. Most groups have four (4) members and you will notice that there are eight (8) total “coding” tasks (three for Netflix, five for your dataset). Thus, letting individual group members “own” around two (2) tasks each will help spread the load. Of course you can all help each other as needed, but let each person take point on two items.
- Once more, do _not_ commit the original files to the repository—they may be too large for that. Provide links instead. Edit _.gitignore_ to avoid accidental commits.
- Not everyone’s computer might have enough storage or other capacity—AWS is an option but watch your credits; or, designate someone as the “host” for doing work and find ways to collaborate over a screenshare and (friendly) remote control of a classmate’s screen.

## How to Turn it In
Commit everything to GitHub. Reiterating the deliverables, they are:
- _netflix-practice.md_
- _about.md_
- _.gitignore_ (revised from what is already provided)
- _queries.md_
- _report.md_

## Specific Point Allocations
(work in progress)
