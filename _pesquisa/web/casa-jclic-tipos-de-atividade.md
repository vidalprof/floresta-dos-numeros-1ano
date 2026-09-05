# 🔎 Pesquisa: casa-jclic-tipos-de-atividade

> Busca: `JClic activity types puzzle association text activities word search crossword description documentation zonaClic`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## D73. Module 1. The Creation of Educational Activities using JClic

`https://clic.xtec.cat/legacy/en/jclic/curs/d73m1/d73m1t4.htm`

D73. Module 1. The Creation of Educational Activities using JClic

The Creation of Educational Activities using JClic

JClic allows you to make seven basic types of activities:

.The user must discover the relationship between two groups of information.

(pelmanism). The user must discover hidden pairs of elements the same or related to each.

,where out of order information has to be put in order. This information can be graphic, text, or sound ....or combine graphics and sound at the same time.

which are resolved by writing a text which can be one word or a sentence.

, which are exercises based on words, sentences, letters and paragraphs in a text which must be completed, understood,corrected and put in order. The texts can also contain images and active content windows.

are interactive variants of these wellknown pastimes.

Some of these types have variants which gives us 16 different possibilities:

There are two groups of information with the same number of elements.Each element of the original group has a counterpart in the second group.

There are also two groups of information, but these can contain a different number of elements and between these there can be different types of relationships: one to one, various to one, loose elements...

This type of activity consists of discovering pairs of elements hidden in boxes. The pairs may be formed by two identical pieces or two elements related to each other.In each go two pieces are uncovered which " hide" again if they do not form a pair. The objective is to find all the pairs in the panel.

You are shown an initial piece of information and when you click on it you are shown another piece of information depending on the element you chose.

You are given one piece of information and you must click on those elements which fulfill certain conditions.

Information is shown and as an option you are offered the chance to activate the multimedia content which each element contains.

Two panels are shown. In one the information is mixed up and the other is empty.You have to reconstruct the object in the empty panel by taking the pieces from the other panel one by one.

In only one panel the information is mixed up.In each try two pieces are moved around until the information is in the correct order.

In the only panel available you make the pieces disappear one by one and each time a piece disappears the information is mixed up again. In each go,you can move one piece towards the hole until all the pieces are in the original order.

You eliminate certain parts of a text ( letters, words, punctuation signs, sentences ) and the user has to fill them in.

Certain words letters and sentences are selected from a text and hidden or camouflaged, and the user must fill them in.There are different ways of solving this: writing in an empty space, correcting the mistakes in an expression or by selecting answers from a list.

The user has to click on certain words, letters, numbers, symbols or punctuation signs.

At the moment of designing the activity some words or paragraphs are mixed up and the user has to put them in the right order.

Information is shown and for each of the elements the corresponding text must be written.

The user must fill in words in the panel according to the definition for each. The definitions can be written, graphic or sound. The programme automatically shows the definitions of the two words that cross where the cursor is found at any given time.

Hidden words have to found in a panel of letters which are selected at random in each game.

The game may be associated to other content in which case, pieces of information (text, sound, images or animations) will appear each time a new word is discovered.

---

## Jclic by projectestac

`http://projectestac.github.io/jclic/`

- Player and authoring tool for educational activities

JClic is a set of cross-platform Java applications useful for creating and carrying out different types of educational activities like puzzles, associations, text exercises or crosswords.

JClic is an open source project of the Department of Education of the Government of Catalonia. Teachers from different countries have contributed since 1995 to create a big repository of educational activities, shared under Creative Commons licenses in the project's main site:

: Allows students to play with the activities and, optionally, track reports of their work in a local or remote database. The activities are organized into “projects” (files with extension .jclic.zip), and projects can be grouped into “Libraries”.

: Is a variant of JClic Player designed to run embedded into HTML documents.

: Is a visual tool used by teachers and authors to create or modify activities and projects.

: Is a reporting tool designed to collect and display the results (time, tries, guesses, success...) achieved by the students when playing JClic activities.

: Is a parallel project specifically designed for embedding JClic activities into the Moodle Virtual Learning Environment. This project lives in

https://github.com/projectestac/moodle-mod_jclic

See INSTALL.txt for compilation instructions, and HACKING.txt if you want to set-up your own JClic development project with

---

## Home

`https://projectestac.github.io/jclic.js/doc/index.html`

(XTEC) for creating various types of interactive activities such as associations, puzzles, text activities, crosswords or puzzles, from elements of text, graphics and multimedia.

The program includes an authoring tool to create activities, a player and a reporting system that stores the results obtained by students. All these components, along with some guides and tutorials on how to create activities, are available in the

JClic is a Java application that runs on Linux, Windows and Mac OS. Full

Many teachers from different countries have used JClic to create interactive materials for a wide variety of levels, subjects, languages and curriculum areas. Some of these materials have been collected in a huge

, another open source project that will facilitate the publication of collections of JClic projects in static web hosting services.

packages. First of all, you must have Node.js (which includes 'npm')

To install the required packages, just go to the project's root directory and write:

This will install jQuery, Webpack and other needed components into

(along with other files useful for development)

To test and debug the resulting bundle, launch the webpack dev server:

This will launch a local HTTP server allowing to choose between pages in development mode (bundle build dynamically by

) and in production mode (serving the latest build on

You can also build this documentation running

JClic.js is organized in three main groups of classes:

class provides methods to read JClic project documents, build players, launch activities and communicate with external reporting systems.

loads JClic project files, manages the user interaction and acts as a interface between the browser and JClic classes for multiple functions. The player has:

: manages the visual appareance. Can have up to three

: are the implementations of the stock skins of JClic.

: used to track the user's navigation between activities.

: Used to collect and display scores, times and other data generated by users while playing activities.

used to connect with external reporting systems like [JClic Reports] (

http://clic.xtec.cat/en/jclic/reports/index.htm

: Utility functions to interact with SCORM 1.2 and 2004 when available

: writes the report as a persistent data into the browser session or local storage.

encapsulates all data needed to play JClic activities. Its main components are:

, that is a real DOM object with wich users interact.

AWT contains some classes similar to those defined in Java's

: an AbstractBox with active content (see below)

: a special case of ActiveBoxBag with boxes distributed in rows and columns.

: contains style specs (color, gradient, border, font, size...) common to one or more

: describes how to cut a panel in multiple cells.

: divides the panel in rectangular cells.

: Provides sound recording (usually from the microphone) so, in language activities, students can compare their pronunciation with a pattern.

: random generator of menthal arithmetics operations

: stores information about what to do when an activity finishes or when the user clicks on a link or button.

: used to decide where to jump, based on the current timing and scoring

: Used to link two cells with a thin line dragged by the user.

JClic.js is an open-source project sustained by

, the Telematic Network of the Catalan Ministry of Education.

Checking the operation of JClic.js on different browsers and platforms is possible thanks to virtual machines provided by

The production releases of JClic.js are smoothly distributed to the final users thanks to the

All project files are also available through

, a very powerful content delivery service powered by

as a platform to translate JClic.js into many languages. Please read

if you want to contribute to the project creating a new translation or improving the existing ones.

---

## Clic Zone – Bank of open educational activities

`https://projectes.xtec.cat/clic/en/`

Clic Zone – Bank of open educational activities

is a service of the Department of Education of the Government of Catalonia that offers a cooperation space open to the participation of all professionals in the educational field interested in using and sharing digital resources.

tool that allows you to create various types of interactive activities (associations, puzzles, text activities, letter soups, crosswords, panels…) where you can integrate text components, images, sounds, videos and other multimedia elements. These activities can be embedded in any blog, website or virtual learning environment. Students can use them on any computer, tablet or digital device, with the possibility of recording the results obtained.

, with thousands of useful free open educational resources created by teachers from various countries.

the JClic tools to create educational activities, use them in the classroom and collect student results.

and use them on Moodle, Classroom and other educational platforms.

how to publish you JClic activities on the Internet

Did you know that the Clic project began more than thirty-five years ago?

I have created or adapted some JClic activities, and now I want my students to be able to do them on their devices. How can I do it? There are several options to answer this…

Imma Palahí, teacher and plastic artist, has extensively used JClic as a tool for the creation of new open educational resources, making the most of its possibilities. She is the author of most of the…

The Guide for interactive self-learning of the Catalan and Occitan languages (GALÍ) offers you an extensive set of JClic activities that will help you learn and progressively consolidate your competence in these languages. GALÍ allows…

How to import JClic projects into the local library

Activities from the ClicZone projects library can be imported directly into the local JClic library, located on your computer or local network. This import was done using Java Web Start, a technology that allowed you…

The ClicZone has moved to this new Nodes space integrated into the digital field projects of the Department of Education of the Government of Catalonia. Here you will now find the JClic library, along with…

A new version of the JavaScript player of JClic was released today, improving performance on mobile and tablet devices: from now on, when viewing a JClic project on a mobile device, you’ll be able to…

---

## D73. Module 2. The Creation of Educational Activities using JClic

`https://clic.xtec.cat/legacy/en/jclic/curs/d73m2/d73m2t4.htm`

D73. Module 2. The Creation of Educational Activities using JClic

The Creation of Educational Activities using JClic

is to find words hidden in a grid full of letters.To indicate that a word has been found it is necessary to click on the first letter and drag the cursor along the word to the last letter and click again. If the word is correct, it will be marked with another colour. (the inverse).

The words can be hidden in any direction:  horizontally,

vertically or diagonally, from the right or the left.

The JClic wordsearch can be simple or with related content. In the latter, the content of a second window appears as a word is found in the wordsearch. The content of the alternative content window can be text, image, sound or animation.

where the words which have to be found are placed. JClic does not combine the positions of the words at random but that part of the distribution that is indicated and filled in with letters. These are chosen at random in each game to be put into the empty boxes.

, which corresponds to the wordsearch and

where the content that has to appear is defined (images, sounds, animations...).

As was done before in the puzzle activities,

As well as writing the words into the wordsearch the list of hidden words must be put into the box on the right. This will be gone into in more detail in the practice session.

It is very important to write the list of hidden words correctly as JClic cannot deduce which expressions are correct and which are not.

If the activity uses panel B (where the hidden content is indicated) it is necessary to write the words in the same order in which they appear in the puzzle.

---

## JClic Guide: Types of activities - projectestac/jclic GitHub Wiki

`https://github-wiki-see.page/m/projectestac/jclic/wiki/JClic-Guide%3A-Types-of-activities`

JClic Guide: Types of activities - projectestac/jclic GitHub Wiki

JClic Guide: Types of activities - projectestac/jclic GitHub Wiki

JClic allows you to make seven basic types of activities:

. The user must discover the relationship between two groups of information.

(pelmanism) The user must discover hidden pairs of elements the same or related to each.

,where out of order information has to be put in order. This information can be graphic, text, or sound ....or combine graphics and sound at the same time.

which are resolved by writing a text which can be one word or a sentence.

, which are exercises based on words, sentences, letters and paragraphs in a text which must be completed, understood,corrected and put in order. The texts can also contain images and active content windows.

are interactive variants of these wellknown pastimes.

Some of these types have variants which gives us 16 different possibilities:

There are two groups of information with the same number of elements.Each element of the original group has a counterpart in the second group.

There are also two groups of information, but these can contain a different number of elements and between these there can be different types of relationships: one to one, various to one, loose elements...

This type of activity consists of discovering pairs of elements hidden in boxes. The pairs may be formed by two identical pieces or two elements related to each other.In each go two pieces are uncovered which " hide" again if they do not form a pair. The objective is to find all the pairs in the panel.

You are shown an initial piece of information and when you click on it you are shown another piece of information depending on the element you chose.

You are given one piece of information and you must click on those elements which fulfill certain conditions.

Information is shown and as an option you are offered the chance to activate the multimedia content which each element contains.

Two panels are shown. In one the information is mixed up and the other is empty.You have to reconstruct the object in the empty panel by taking the pieces from the other panel one by one.

In only one panel the information is mixed up.In each try two pieces are moved around until the information is in the correct order.

In the only panel available you make the pieces disappear one by one and each time a piece disappears the information is mixed up again. In each go,you can move one piece towards the hole until all the pieces are in the original order.

You eliminate certain parts of a text ( letters, words, punctuation signs, sentences ) and the user has to fill them in.

Certain words letters and sentences are selected from a text and hidden or camouflaged, and the user must fill them in.There are different ways of solving this: writing in an empty space, correcting the mistakes in an expression or by selecting answers from a list.

The user has to click on certain words, letters, numbers, symbols or punctuation signs.

At the moment of designing the activity some words or paragraphs are mixed up and the user has to put them in the right order.

Information is shown and for each of the elements the corresponding text must be written.

The user must fill in words in the panel according to the definition for each. The definitions can be written, graphic or sound. The programme automatically shows the definitions of the two words that cross where the cursor is found at any given time.

Hidden words have to found in a panel of letters which are selected at random in each game.

The game may be associated to other content in which case, pieces of information (text, sound, images or animations) will appear each time a new word is discovered.

---

## GitHub - projectestac/jclic: JClic is a set of cross-platform Java applications useful for creating and carrying out dif

`https://github.com/projectestac/jclic`

GitHub - projectestac/jclic: JClic is a set of cross-platform Java applications useful for creating and carrying out different types of educational activities like puzzles, associations, text exercises or crosswords. · GitHub

You signed in with another tab or window.

You switched accounts on another tab or window.

You must be signed in to change notification settings

- Player and authoring tool for educational activities

JClic is a set of cross-platform Java applications useful for creating and carrying out different types of educational activities like puzzles, associations, text exercises or crosswords.

JClic is an open source project of the Department of Education of the Government of Catalonia. Teachers from different countries have contributed since 1995 to create a big repository of educational activities, shared under Creative Commons licenses in the project's main site:

: Allows students to play with the activities and, optionally, track reports of their work in a local or remote database. The activities are organized into “projects” (files with extension .jclic.zip), and projects can be grouped into “Libraries”.

: Variant of JClic Player that can run embedded in HTML documents. Currently not used because lack of Java Applet support in modern browsers.

: Visual tool used by teachers and authors to create or modify activities and projects.

: Reporting tool designed to collect and display the results (time, tries, guesses, success...) achieved by the students while playing JClic activities.

: Is a parallel project specifically designed for embedding JClic activities into the Moodle Virtual Learning Environment. This project is available in:

https://github.com/projectestac/moodle-mod_jclic

See INSTALL.txt for compilation instructions, and HACKING.txt if you want to set-up your own JClic development project with

JClic needs Java 1.7 or later (currently supported only in GNU/Linux, Windows and Mac OS X)

allows to play JClic activities in GNU/Linux, Mac, Windows, ChromeOS, Android, iOS...  and any operating system with a web browser supporting HTML5, without the need of Java.

JClic is a set of cross-platform Java applications useful for creating and carrying out different types of educational activities like puzzles, associations, text exercises or crosswords.

You can’t perform that action at this time.

---

## ⚠️ Paginas que NAO deram texto

- `https://integracio.clic.xtec.cat/en/jclic/howto.htm` — HTTPSConnectionPool(host='integracio.clic.xtec.cat', port=44
