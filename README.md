# Advanced MongoDB

This is the repository for the LinkedIn Learning course Advanced MongoDB. The full course is available from [LinkedIn Learning][lil-course-url].

_See the readme file in the main branch for updated instructions and information._

## Instructions

This repository has folders for each of the videos in the course that requires a lot of typing.

# Advanced MongoDB
This is the repository for the LinkedIn Learning course Advanced MongoDB. The full course is available from [LinkedIn Learning][lil-course-url].

![Advanced MongoDB][lil-thumbnail-url] 

Expand on what you learned in MongoDB Essential Training by exploring advanced features and concepts within this powerful document database. Instructor Naomi Pentrel divides the course into four standalone sections. To begin, Naomi covers advanced features, such as change streams and GridFS. She then dives into advanced collection types and indexes that can help you use MongoDB more efficiently; how to scale your deployment using sharding; and how to use client-side field-level encryption to encrypt sensitive data before it even leaves the client. After wrapping up this course, you’ll have the information you need to start getting more value from your database.

## Instructions
This repository has branches for each of the videos in the course. You can use the branch pop up menu in github to switch to a specific branch and take a look at the course at that stage, or you can add `/tree/BRANCH_NAME` to the URL to go to the branch you want to access.

## Branches
The branches are structured to correspond to the videos in the course. The naming convention is `CHAPTER#_MOVIE#`. As an example, the branch named `02_03` corresponds to the second chapter and the third video in that chapter. 
Some branches will have a beginning and an end state. These are marked with the letters `b` for "beginning" and `e` for "end". The `b` branch contains the code as it is at the beginning of the movie. The `e` branch contains the code as it is at the end of the movie. The `main` branch holds the final state of the code when in the course.

When switching from one exercise files branch to the next after making changes to the files, you may get a message like this:

    error: Your local changes to the following files would be overwritten by checkout:        [files]
    Please commit your changes or stash them before you switch branches.
    Aborting

To resolve this issue:
	
    Add changes to git using this command: git add .
	Commit changes using this command: git commit -m "some message"

## Installing
1. To use these exercise files, you must have the following installed:
	- [list of requirements for course]
2. Clone this repository into your local machine using the terminal (Mac), CMD (Windows), or a GUI tool like SourceTree.
3. [Course-specific instructions]


### Instructor

Naomi Pentrel 
                            
Software Engineer 

                            

Check out my other courses on [LinkedIn Learning](https://www.linkedin.com/learning/instructors/naomi-pentrel).

[lil-course-url]: https://www.linkedin.com/learning/advanced-mongodb
[lil-thumbnail-url]: https://cdn.lynda.com/course/2476236/2476236-1661449045299-16x9.jpg
