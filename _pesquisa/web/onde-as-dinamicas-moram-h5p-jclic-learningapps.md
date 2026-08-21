# 🔎 Pesquisa: onde-as-dinamicas-moram-h5p-jclic-learningapps

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## Examples and Downloads | H5P

`https://h5p.org/content-types-and-applications`

H5P makes it easy to create interactive content by providing a range of content types for various needs. Preview and explore these content types below.

You can create interactive content by adding the H5P plugin to your

Create a presentation with interactive slides

Create vertically stacked expandable items

Create a sequence of images that gradually change

Create a task with missing words in a text

Create an image with a question and answer button

Create an image with multiple info hotspots

Create a task where users highlight words

Create flexible multiple choice questions

Create a questionnaire to receive feedback

Create a sequence of various question types

Create a timeline of events with multimedia

Create a presentation with interactive slides

Create H5P interactive content in systems like:

H5P is an open source community driven project.

and help us create richer online experiences!

---

## Drag and Drop | H5P

`https://h5p.org/drag-and-drop`

A free HTML5-based drag and drop question type allowing creatives to create many forms of drag and drop using only a web browser.

engaging challenges using H5P and Drag and Drop

in publishing systems like Canvas, Brightspace, Blackboard, Moodle and WordPress.

Drag and drop the pieces to the correct starting positions.

Would you like to create content like this on your own?

Register on H5P.com to start creating H5P Interactive content.

Your content can be accessed via direct link, embeded, or inserted into any learning management system that supports LTI integration.

Drag and drop questions enable the learner to associate two or more elements and to make logical connections in a visual way. Create Drag and drop questions using both text and images as draggable alternatives. H5P Drag and drop questions support multiple draggable to drop zone combinations; one-to-one, one-to-many, many-to-one and many-to-many.

Learn how to create a Drag and drop question in

Drag and drop questions may be used standalone, but can also be included in:

The H5P content on this page is licensed under

Creative Commons Attribution 4.0 International

unless another Creative Commons license is specified under rights of use. The author of the content is

Is possible to add short audio into the text object?

Is possible to add short audio into the text object? In learning language, it would be very good to play a short audio with click the text.

It's currently not possible. This is something that might get added in the future, and we do accept patches or donations to make this happen.

Currently with my current status, I have no resource to give donation, but I am very interested in this project. I read the developer documents. They are not very clear for me. If you can offer some support or explanation, I am willing to do the patches. I can also help to support making some documents.

I breifly check the code and documents. It is good for h5p to have audio option for many content types. It needs to conclude a standard (I noticed that there is no

Briefly in my mind, for the audio of drag and drop, it will need

add html <audio> tag to text object for adding audio source(mp3)

make jQuery event listener for click or mouse hover

I would really appreciate if you could let me know how to continue to get involved and cooperate with h5p project.

Yeah, the documentation needs a real upgrade. I added the

, and (2) replace the image with an audio. Then (3) try to add audio to the semantics of the drag and drop. Then, finally, (4) try to make the audio play when you need it to play.

Ask for help here, or contact us directly to get help more quickly. Ok?

I did a few tests. I added a audio in h5p with jQuery (H5p JQuery). Here shows

.  Currently it uses the audio source remotely.

It is great to have a audio player but what I need most would be audio text and audio image. That is adding audio to the text and audio to the image so that when the user clicks or hovers the text/image, they can hear how to say it. This is very helpful for language learning. I plan to make every object be able to pronouce.

Currently I have a little problem to add the audio(refer to my post in

page). My problem right now is how to add the content for editor and the user can add their audio and related information. Also, I apprecate your opinion: should we create a new type (audio text and audio image) or update the old text and image object.

I also think of make the audio refer to the word itself and search a pronounciatoin database in the future. Well currently this is still far away idea.

Do you only need this to work in drag and drop? If so I would add audio to the semantics of drag and drop(H5P.DragQuestion) on the same level as x, y, height and widht - and let H5P.DragQuestion be responsible for playing the audio when texts and images are being clicked.

Yes. For drag and drop, that is all I need. I also would like to have audio function in multiple choice.  If we should do it individually for each content types, then that's it.

To implement this in drag and drop, do you mean add audio in semantics.json (arround the following?)

C.prototype.attach = function ($container) {}

Anyway, if you could do this part, it would be great and I will check the implementation.

For long-term, I am also interested in modifying multiple choice (be alle to have text, image, and audio in the choices), make short answer content type (I think h5p does not have either) and optionally create a content type that focuses on arranging orders of words to make a sentence. If you kindly give some support somtimes, I can do these little by little.

By "If so I would add audio to the semantics..." I didn't mean that I would actually do it, only that if i were to do it I would do it that way. I'm working on the xAPI integration and have a lot of other tasks lined up after that.

I think you're heading in the right direction.

Sorry that I mis-understood. I appreciate very much your help and I will continue to make it.

Great, we're happy to assist you on the forums, we just can't do the coding

I am trying to add audio info into the h5p_text. About editor interface, since the

is not finished, I need some clarification.

In semantic, I think widget is input interface in the editor. I saw html (text editor), dynamicCheckboxes, and dragQuestion. Currently I check what the widget types are by matching the code and the h5p content. Is it possible to customize or provide patches (I mean a standard or common base so that people can refer to, contribute and follow)?

Some items (for example, text and image) do not have widget, then the default applied?

". I mean 1.0 is the majorVersion in library.json?

If I would like to make a H5P.Text with audio, the best practice would be create a new library (for example H5P.audioText) similar to H5P.Text, correct? (And then add it to options for Task (a dragQuestion widget)).

Widget is the input interface yes. Didn't understand the last part of the question.

Yes, it's the library with machineName H5P.Text, majorVersion 1 and minorVersion 0.

Yes, I think that would be the way to go.

I was trying to create this content type online at h5p but could not find it in drop down list. Is it not available anymore?

When creating a new drag and drop, I am able to upload an image for the background but when I switch to tasks to add dropzones or text or images, the buttons don't respond. I can click and i see the button push action but with no result.  Any ideas?

Sounds like a JavaScript error. Could you try to open your console and paste any error message you're getting here? You use CTRL + SHIFT + I to open your console, just do that and do the things that doesn't work and see if if you get any messages in the console.

If we're doing an activity where drop zones are labeled with words, and there are multiple draggable images that correspond to those words' meanings, how can we disable the functionality that displays a dotted outline for the correct drop zone when the corresponding image is being dragged?  It's basically revealing the answer to the user before they even try placing the image in any drop zone...

Edit the draggable item and select all the dropzones and click done. This way you'll make all the dropzone a possible answer.

Edit the correct drop zone and mark the correct draggable there, this way you make the solution.

Could you assist in identifying the problem with the drag and drop on this WP theme?

It seems to have worked great on my last theme, but this one makes the words that are lifted up dissapear:

http://greatwebsiteplans.com/keyword-optimization-quiz/

That was an ugly one. We'll look into it and update you as soon as possible. I had a quick look but couldn't find the reason right away so I made a ticket for it instead and we will probably start on it next week.

Is there a show solution button for drag and drop questions?

Hi, we are using course presentations on our site and we are including drag and drop questions within these.  Is there a show solution button available for drag and drop questions? Currently the users can only see whether or not their answer is correct but cannot see what the correct answer is.

No, solution view for drag and drop questions haven't been implemented yet. We're not sure how to design it. If you have a good idea feel free to share it! Remember that it must be WCAG 2 compliant and support all the features of drag and drop (stacks of moveable alternatives and multiple alternatives may belong to the same dropzone etc.)

Maybe if after to show the solution button activate, the exercise shows the drop zone number in each drop zone, and also, nedxt to the text field the drop zone number too.

is frustrating to the students if they can not know the solution.

the drag-and-drop exercise is easy to use thanks to your tutorial. What I find extremely annoying is the sizing. I have tried with the task size and I got the result I wanted. What I did not manage to achieve was to resize the embedded code. When the exercise appears on the my website, the user has to scroll a lot just to see the whole picture and press the "Check" button. It is not that dramatical because I was  just testing and wanted to show an example on my blog, but it is not user-friendly.

Thanks and congratulations for the great job.

Hi Beatriz, you may be using the auto resizer.

In your embed code you may see this just after the </iframe> tag:

http://www.coursecontent.co.uk/wp-content/plugins/h5p/h5p-php-library/js...

This will scale the content to fit your page, so the height will scale proportionately with the auto-sized width.

Try the embed code without script.  Obviously if your project size is greater than your iframe size you will have an internal scroll bar.

Another option if you want to keep the script in order to get a smaller view on phones is to try a div outside the iframe tag with a max-width, or maybe even add a max-width on the iframe. I haven't tried this myself though.

I too don't have the option for Drag and Drop on H5P.org. Any chance of providing it please?

I don't have the Drag and Drop Tool in my Dropdown-Menu either. Can somebody please help me out?

Do note that the reason it isn't there for new users is that it is hard to use. The possible answers are set when you edit the draggable alternative,

but the correct answer is set when editing the drop zones.

I can't create a drag and drop with images. Could you please give me access to it?

Could I be given access to the drag/drop quiz

This is exactly what i'm looking for!  Could I also be given access to it from my drop-down list?

How can I change color of the drop zone? As i can see the default color is light grey, nearly white, no borber so when i create on white background it will be very difficult to see. So is there anyway i can change the color or make border for the drop zone?

I would like to know if there is an option to remove negative points. For example when i place two object on the right target and one on the wrong target I get one point because placing object on the wrong target reduces score.

I'm afraid that we don't have an option for that yet :/

Second that (0 points instead of negative points)

I'm not a developer so I have not clue the amount of work that goes into this like this, but it is confusing to my students who get 2 out of 3 right but only get one point, so +1 to trying to avoid negative scoring. Thanks : )

Thanks! Do note that many drag and drops will be possible to cheat on if we just disabled the negative scoring. For instance if there is one drop zone (fruit) and 10 draggables (some fruits, some vegetables) the student would get full score if she dragged all the draggables into the dropzone. +1 for each correct and 0 for the mistakes.

@falcon, your reasoning is true in the case of a D & D activity with only

drop zone and several draggables. In my opinion this is not the most frequent use of D & D and actually the D & D strawberry example on this site should be replaced (or complemented) by a more standard example of several drop zones with several draggables!

Anyway I am currently working on adding a "penalties/no penalties" option to the behaviour settings of D & D which would leave that decision to the activity creator. Hoping that that would please everyone.

Good, yes, I agree, it is not the most standard. There are other examples as well that we need to think about when working on this. If you check "Infinite number of element instances" for a draggable it will be possible to match it to all dropzones. Again, without negative points(or only one element per drop-zone) you can pair it with all drop-zones and get full score.

So a simple choice with a description (and probably negative scoring as the default) would be good!

(Even better would perhaps be "automatically decide scoring method"? So if we detect one of (1)There is only one dropzone and it accepts multiple entries or (2) The alternatives may have multiple instances and dropzones accepts multiple entries we go for negative scoring, if not we go for the new scoring.)

I'm generally wary of "automatic decisions" and prefer human decisions. Please have a look at my "

Add option to apply or not apply penalties to wrong answers

" pull request and comment. Looking forward to that feature to be implemented, as it has been requested by a number of users.

Looks good! I don't think it is easy for any user to see that no negative scoring will allow users to cheat, so we should at least do a small attempt to inform about that. Other than that it needs normal testing. Commented on GitHub. I think many will appreciate this change a lot!

H5P is an open source community driven project.

and help us create richer online experiences!

---

## Memory Game | H5P

`https://h5p.org/memory-game`

A free HTML5-based memory game content type allowing authors to add their own images (and optional text) to a memory game. To play the game, users search for image pairs, which will display a specified text message once a matching pair has been found. Memory games are created using only a web browser

in publishing systems like Canvas, Brightspace, Blackboard, Moodle and WordPress.

Would you like to create content like this on your own?

Register on H5P.com to start creating H5P Interactive content.

Your content can be accessed via direct link, embeded, or inserted into any learning management system that supports LTI integration.

Create your own memory games and test the memory of your site's users with this simple yet beautiful HTML5 game.

The H5P content on this page is licensed under

Creative Commons Attribution 4.0 International

unless another Creative Commons license is specified under rights of use. The author of the content is

It seems that this example does not save any results. Only "started" time is saved to "h5p_points" -table.

Tried to fix but just adding  H5P.setFinished(contentId, score, maxScore());  does not make it work.

We've got an issue on this and are planning to add it in a future version:

https://github.com/h5p/h5p-memory-game/issues/2

Feel free to contribute on how you would like the score and max score to be calculated.

I love the memory game and I wonder if would be possible to add a feature whereby you could use two different items for each matching pair? For instance, if I was teaching colours, I would have a red strawberry and the word "red" on different tiles of the pair. Or, if I was teaching phrasal verbs, I might have "get" on one tile, and "over" on the other.

https://github.com/h5p/h5p-memory-game/issues/5

In math you could have a simple matching card game: 2^2= and then a matching card 4.

Btw perhaps add support for LaTeX syntax in description of two matching cards?

Thanks again for creating this plugin :-)

This sounds like a great idea! If you create an issue on

, it will be easier for the developers to keep track of what people want. Feel free to comment on other ideas there as well :-)

Matching different cards would make language drills ENDLESSLY more fun, so it would be greatly appreciated!

It should be possible to do this in the latest version, you just need to upload a second image for the same card.

how i can change size of images/cards? They are too small :(

I'm afraid you'll have to change those sizes in code. There are no setting for changing them. This page might be helpful:

https://h5p.org/documentation/for-developers/visual-changes

Great stuff. It will be valuable, besides confiuring a text that appears when the 2 cards match, to also play an audio file. This will be useful for me to play the sound of the object matched if I am teaching a kid the names of things. Maybe also, the ability for the kid to replay the sound (either cick on a replay icon or click on the matched image directly).

Yes, good idea! I don't think the H5P core team will be able to start working on this in the short term unless it is funded, but hopefully others will contribute a pull request for this.

Request you to add a feature where we could play a sound file while opening a card. It will be very useful for vocabulary building exercise in a language class.

Thanks a lot for contributing your ideas on how to make H5P better! We’re now working on something called the H5P supporter program allowing the H5P community to vote for and fund the top voted H5P features. Also there are developers in the community who every now and then works on a feature they find interesting or useful. In order for your feature request to attract as much interest as possible make sure it follows the below guidelines

It is clear from every perspective how the feature will work. We recommend describing the feature with one or more user stories, for instance “As an author I want it to be possible to pick between different effects for the check answer animation so that the learners will see a variety of effects and also I can adapt the effects to my target audience(I’ll be using pink unicorns which works really well for both my target audience which are 4 year old girls and venture capitalists)”

If the feature can be illustrated with images or videos it always helps

Make it clear what content types this is relevant for, and or if this is a new content type

Is there an option to change cards picture from question mark when it's faced down. I would like to create custom symbol for memory cards.

There is no option for changing the back-side of the card at the moment, but I really like the idea.

If you are a developer or have a developer then Frode, the author of the library, would probably accept a pull request for this :)

It would be great to show a leaderboard front end to keep users engaged in the game

It would be great if after playing a link would be installed. Ist this possible? Can i edit the feedback text to a link?

Currently, this is not supported, but I'll note down your request!

Where would you've liked the link to appear? Perhaps in the description that popups up after finding a pair, or in the final feedback text below the task?

It would be great after the final feedback text. I like to link on a contactform... Thank so much!

We have some images in our website, so we don't want re-upload in Memory Game. Can you support for external links ?

This is something that absolutely is doable. Could you please add an issue here:

https://github.com/h5p/h5p-memory-game/issues

I did, hope you will have a new update. Thanks.

Hello, I like the plugin, but I would like to make some changes on the result.

I would like to make the cards bigger (300px) also I would like to change the front image (the interrogation mark) to another image.

- Create a pull request for the repository where you add the possibility to make cards larger and adding a front image by adding the necessary semantics for this, relevant:

- Create a hook for altering the semantics:

https://h5p.org/adding-text-editor-buttons

http://cgit.drupalcode.org/h5p/tree/h5p.api.php

Is there a way for students to match pictures with text/ pictures with a different picture?  For example, a picture of a fingerprint on one card, and the type of print on the card I want them to match it with?

Currently, this isn't possible, but many have requested this feature so I wouldn't be surprised if it turned up soon.

Ooh please yes, I am also looking for this feature.

Hi! I really enjoy the tools, so thank you for developing these great solutions! I have a question though. I teach 2 students on-line at the same time. Is it possible that they play against each other? Are there other tools which work for multiple users? Thank you in advance!

No, there aren't really any compeditive content types yet. But I think there is a lot of potential in that space.

Regarding other tools (with a competition aspect), have you tried

I'm using moodle 3.2, I'm searching in the DB where it store the time and turned off cards, but I only found in grades the total score for this.

Where can I found the other info ? And if is not being saved in moodle DB, where I can sored using moodle plugin o a third party  solution  ?

In Moodle, only the Gradebook is used to track the score of the activities by default. To be able to track more you can use a custom plugin that adds a JavaScript that hooks into the Events generated by the content and then you can send whatever you want wherever you want. This is described in the documentation section:

Memory game doesn't work at all with Internet Explorer 11

Memory game doesn't work at all with Internet Explorer 11, you can open all the cards at once, please see;

https://github.com/h5p/h5p-memory-game/issues/22

Memory game doesn't work,and how to update to 1.22

I am using 1.21 now.but all games can't be opened.dispaly nothing.

Are you seeing any error messages in your web server's console? Use Ctrl + Shift + J to open the console in Chrome.

TypeError: instance is undefined   h5p.js:1728:

Hm, is that all? Try checking the Network tab to see if there are any files that fail to load.

the js and css files in uploads path can't be loaded.

some file in "h5p/cachedassets" not loaded,such as:

https://img.mysite.com/wp-content/uploads/sites/3/h5p/cachedassets/8b9c1...

https://img.mysite.com/wp-content/uploads/sites/3/h5p/cachedassets/8b9c1...

my uploads path is on remote server,and the url prefix is "

https://img.mysite.com/wp-content/uploads

https://www.mysite.com/wp-content/uploads

now I have to look for where to set the path like those two types.

I edited the function "enqueue_assets" in "h5p\public\class-h5p-plugin.php", changed "$abs_url" to h5p cache path.

Ah yes, that's it. The plugin hasn't really been tested with remote upload paths. I've created an issue for fixing it:

Is there anything special one needs to do when setting up remote upload paths? Do you need a plugin for it?

I love h5p a lot because it added a new feel to the game section on my social networking site.... Is there a way where we can have more that one level, if someone plays the first game, can there be a next button to play another one....and the retry button doesn't show up

and write a suggestion on how you would like such a feature to be.

Would it be possible to add a behavior setting that allows users to change the speed at which the cards flip.  I would like to use this for math, but often my students cannot solve the problem or read the word problem before the cards are both flipped back over.

Yes, in the next version the unmatched cards will stay until you click the next card. This has to do with accessibility(WCAG) for people using readspeakers as well.

H5P is an open source community driven project.

and help us create richer online experiences!

---

## Find the words | H5P

`https://h5p.org/find-the-words`

A free HTML5-based word search activity that allows authors to create a list of words that will be drawn in a grid. The learners' task is to find and select the words in the grid. Find the words is available through the H5P plugin on Drupal, Moodle or Wordpress sites and is embeddable onto any website that allows embeds.

Would you like to create content like this on your own?

Register on H5P.com to start creating H5P Interactive content.

Your content can be accessed via direct link, embeded, or inserted into any learning management system that supports LTI integration.

H5P is an open source community driven project.

and help us create richer online experiences!

---

## clicZone - What is JClic?

`https://clic.xtec.cat/legacy/en/jclic/howto.htm`

applications that are used for carrying out different types of educational

activities: puzzles, associations, text exercises, crosswords...

The activities are not usually used alone, but packed

in projects. A project is formed by a set of activities and one or more

sequences, which indicate the order in which they have to be shown.

an application that  has been used by educators of different countries

since 1992 as a tool for the creation of didactic activities for their

JClic is developed in the Java platform, is a free software

project and works in different environments and operating systems.

JClic activities in any web browser and on any device, including smartphones, tablets and Chromebooks, without the need of installing Java.

Two ways of accessing the projects JClic are offered in

the library of activities in the clicZone:

HTML5 blocks are objects embedded in a web page. The projects

that are seen this way do not remain stored in the hard disk: JClic

downloads it, uses it and finally deletes it.

On March 9, 2017, JClic applets stopped using

technology to run with a new HTML5 engine named

. This change has been forced due to the loss of Java support in major web browsers, like Chrome or Firefox.

HTML5 blocks can work in two different ways:

: The HTML5 block downloads the activities in a single file with extension ".jclic.zip". Then tries to decompress it in memory. In this modality it may happen that some activities are not seen correctly.

: This is the recommended option. The web browser will download the ingredients of the activities as needed. Most activities will look right. In order to publish JClic activities in this modality, you must use the function "Export to SCORM and HTML5" of JClic Author.

JClic has a wizard which allows you to  download

the activities and put them in the projects library of the computer.

The library is created the first time JClic is started, or when you

try to do the first installation of a project.

To see the projects in the library you will need to

As in the previous case, if the installer does not start automatically

---

## ⚠️ Paginas que NAO deram texto

- `https://h5p.org/crossword` — HTTP 404
- `https://learningapps.org/createApp.php` — bloqueada ou vazia
