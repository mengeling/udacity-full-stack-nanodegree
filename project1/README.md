# Movie Trailer Website
[View Static Website](https://mengeling.github.io/udacity-full-stack-project-1/)

## Installation
* Press "Fork" to create a copy of this repository on your own GitHub account
* Press the "Clone or download" drop-down and copy the link
* Open your terminal and type `cd [INSERT DIRECTORY NAME]` to change the directory to the one you want to use to store the repository on your local machine
* Type `git clone [INSERT COPIED URL HERE]`

## How to Update the List of Movies
* Navigate to the local directory that contains the cloned repository
* Open the **entertainment_center.py** file
* Go to the 7th line of code where the first instance of a movie is created
* Look up your movie's title, storyline, image URL, and youtube trailer URL online and then update the code in lines 7 - 13, following this format:

```sh
[INSERT VARIABLE NAME] = media.Movie(
    "[INSERT MOVIE TITLE]",
    "[INSERT MOVIE STORYLINE]",
    "[INSERT POSTER IMAGE URL]",
    "[INSERT YOUTUBE TRAILER URL]")
```
* Continue updating the subsequent chunks of code until you've created instances for all of your favorite movies
* Update the line of code at the bottom of the file that creates the **movies** list with all of the instances included in the format shown here:

```sh
movies = [
    [INSERT 1ST MOVIE VAR], [INSERT 2ND MOVIE VAR],
    [INSERT 3RD MOVIE VAR], [INSERT 4TH MOVIE VAR],...
    ]
```

## Creating the HTML File

* Save the **entertainment_center.py** file
* Go back to your terminal and make sure your current working directory is the one that has the repository (if it isn't, use `cd [INSERT DIRECTORY NAME]` to go to the repository directory)
* Type `python entertainment_center.py` to create the HTML file for your movie website

&nbsp;
&nbsp;

![Website Screenshot](/project1/screenshot.png?raw=true)
