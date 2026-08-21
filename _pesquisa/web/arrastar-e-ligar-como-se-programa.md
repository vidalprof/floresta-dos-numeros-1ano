# 🔎 Pesquisa: arrastar-e-ligar-como-se-programa

> Busca: `drag and drop educational game HTML touch and mouse children implementation pitfalls matching pairs activity`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## How to Make Drag Effect Using Mouse and Touch Events | TokozZing

`https://tokozzing.com/blog/how-to-make-drag-effect-using-mouse-and-touch-events`

How to Make Drag Effect Using Mouse and Touch Events | TokozZing

How to Make Drag Effect Using Mouse and Touch Events

A couple of months ago, I started a project with other peers to create a website that helps Korean learners, especially young kids, practice Korean through interactive games.

This project was initiated by a teacher currently working at a Korean school in the US. It aims to help students easily learn Korean by repeatedly practicing the consonants, vowels, and their combinations through various games.

The main target audience is young kids, so the game had to be simple to play while including many interactive elements to keep them engaged. One of the games, a word-matching game, requires users to find matching words and drag the answer to the correct spot.

The drag effect I implemented this time was simpler than the one I created for my portfolio website (which had a Trello-style drag-and-drop feature).

However, this new drag effect needed to work on both pointer and touch devices. Although the

event provides some helpful features, like

, I needed to explore the differences between drag events and touch events to ensure compatibility across devices.

Here are some key differences between touch events and drag events:

Touch events are triggered when a user touches the screen.

These events are triggered immediately upon contact with the screen, giving them a faster response time.

Drag events are mainly used for handling drag-and-drop actions with a mouse or pointer device.

Drag events require the element to be draggable by setting

in HTML, and they won’t start unless the element is set to be draggable.

Drag events are typically suited for desktop interactions and tend to be slower compared to mouse events or touch events, especially

because they are controlled by the browser’s native drag-and-drop event system.

Touch events can detect multiple touch points

Touch events are lightweight and optimized for mobile, where response speed is crucial.

Used in several gestures, such as drag-and-drop, swipes, taps, and pinches.

There aren’t many differences between handling events in vanilla JavaScript and React.

Drag events require elements to be explicitly set as draggable.

Drag events support data transfer, which is useful when transferring data, such as files or text, between applications of elements.

Drag events are single-point and cannot track multiple gestures.

Since React uses virtual DOM, direct DOM manipulation is discouraged, and the drop event in React should be handled differently, especially when DOM needs to be updated.

When transferring data like files or text, using the

event is convenient in many ways. However, when implementing an action to drag a specific element and move it to another position—especially if you want consistent behavior across multiple devices—I found that using both

events can make things significantly more complex and challenging to manage. This led me to explore simpler and more efficient methods to handle drag interactions across different devices.

So, I came up with a method that combines

event is also a single-point event, but it shares many behavioral characteristics with touch events. By using these two events together, I could apply the same logic across different devices.

Here’s a quick summary of the advantages of using these two events together:

Mouse and touch events both provide direct access to the element’s coordinates(

). This allows you to handle the element’s position directly, giving full control over the dragging behavior.

With mouse and touch events, you can unify the logic by using the same handlers(e.g.,

for touch). This creates simpler, more maintainable code and reduces redundancy.

Mouse events work seamlessly on desktop, while touch events handle mobile more effectively. Combining these makes it easier to ensure consistent, smooth interactions on both types of devices without additional fallback code.

When implementing a drag-and-drop effect using mouse and touch events, I listed out the key functionalities needed.

First, when the initial event is triggered on the target element, the pointer or touch point position must be saved to move the element along with the pointer or touch point. Then, tracking the pointer's movement and updating the element’s position is essential.

Finally, depending on the event outcome, the DOM or styling should be updated when the pointer reaches the target drop area.

Save the pointer or touch point position within the drag element when the initial event (

Update the drag element’s position during the movement using

Pre-store the drop element's location and, when the pointer or touch point event (

) occurs within this area, update the DOM or styling as needed upon drop.

My approach to creating the dragging effect involves attaching

event listeners to the draggable elements. When these events are triggered, the handler stores the pointer's screen position, the offset position of the pointer within the draggable element, and the dragging item’s information.

, to store drag and drop items and their positions. In this hook, once a

listeners are attached to track the pointer’s position, while

listeners check the dropping position. As the pointer moves, the hook updates the pointer’s position, allowing the dragging element to follow the pointer accurately.

To show a grabbing motion when the drag starts, I applied

hook allowed me to update the position of the dragging item smoothly.

One issue I encountered, however, was implementing a hover effect when the drag item hovers over the drop item. When I added the Tailwind class

&:hover { background-color: var(--bg-lighter); }

), the effect didn’t actually work as expected.

The reason for the issue was that since the dragging item is right under the pointer, the actual element that could trigger

effect was the drag item itself. So, I tweaked the logic little bit by checking if the

This condition enabled the hover effect to activate correctly when the pointer entered the

event was triggered. If it was, the item moved to the drop zone; if not, it returned to its original position using the

In summary, implementing drag-and-drop functionality across both mouse and touch devices required a custom approach using the

hook to handle events and positions efficiently. By combining

events, I was able to create a smooth, cross-device drag-and-drop experience. This process highlighted the importance of tailoring interactions for different device types, and in the future, additional features like snapping to the drop area or adding transition effects could further improve the user experience.

---

## Matching Pairs: Basic Drag and Drop Challenge

`https://www.educaplay.com/learning-resources/24704291-basic_drag_and_drop_challenge.html`

Matching Pairs: Basic Drag and Drop Challenge

To be used in an LMS (Moodle, Blackboard...)

Downloading games is an exclusive feature for users with an Academic Plan or a Commercial Plan.

now and start integrating your games into your LMS, website or blog.

If you wish, you can download a demo game here and test its integration:

<iframe allow="fullscreen; autoplay; allow-top-navigation-by-user-activation" allowfullscreen width="795" height="690" frameborder="0" src="https://www.educaplay.com/game/24704291-basic_drag_and_drop_challenge.html"></iframe>

You have exceeded the maximum number of games you can integrate into Google Classroom with your current Plan.

To integrate as many games as you want in Google Classroom, you need an

You have exceeded the maximum number of games you can integrate into Microsoft Teams with your current Plan.

To integrate as many games as you want in Microsoft Teams, you need an

You can integrate the game into an LMS compatible with LTI 1.1 or LTI 1.3 such as

. This way, the scores will be automatically saved into the platform’s gradebook.

Downloading games is an exclusive feature for users with an Academic Plan or a Commercial Plan.

now and start integrating your games into your LMS, website or blog.

If you wish, you can download a demo game here and test its integration:

You have exceeded the maximum number of games you can print with your current Plan.

To print as many games as you want, you need an

You have exceeded the maximum number of games you can integrate into Google Classroom with your current Plan.

To integrate as many games as you want in Google Classroom, you need an

You have exceeded the maximum number of games you can integrate into Microsoft Teams with your current Plan.

To integrate as many games as you want in Microsoft Teams, you need an

Downloading games is an exclusive feature for users with an Academic Plan or a Commercial Plan.

now and start integrating your games into your LMS, website or blog.

If you wish, you can download a demo game here and test its integration:

Match each item to its correct category. Test your sorting skills!

Make your own free game from our game creator

Compete against your friends to see who gets the best score in this game

This card game is designed to review the stages of the cell cycle.

Match the description to the correct Amendment from the Bill of Rights.

Match the key terms descriptions to the Balance Sheet and Income Statement classifications

You have exceeded the maximum number of games you can print with your current Plan.

To print as many games as you want, you need an

Match each item to its correct category. Test your sorting skills!

---

## DAY 4 PROJECT : DRAG & DROP - DEV Community

`https://dev.to/shrishti_srivastava_/day-4-project-drag-drop-4p4p`

DAY 4 PROJECT : DRAG & DROP - DEV Community

PROJECT NAME : Creating a Fun Drag and Drop Color Game Using HTML, CSS, and JavaScript

The main objective of this project is to create a game where users can drag colored boxes and drop them into designated areas. The game will include multiple colored boxes, and users can enjoy the interaction and visual appeal of dragging and dropping these elements.

This project is a fantastic way to learn and practice DOM manipulation, event handling, and styling in web development. Let's dive into the details of this fun and educational project!

: For adding interactivity and handling the drag-and-drop functionality.

The drag function enables drag-and-drop functionality for elements with the draggable attribute. It achieves this by handling mouse events (mousedown, mousemove, and mouseup) to update the position of the elements as they are dragged.

dragging: A flag to track the element currently being dragged.

mouseX and mouseY: Store the mouse's initial x and y coordinates when the drag starts.

eleX and eleY: Store the initial x and y coordinates of the element being dragged.

boxes: Select all elements with the draggable attribute.

boxes.forEach: Iterate over each draggable element and attach a mousedown event listener to initiate the drag. Also, initialize the top and left CSS properties of each element to 0.

e.preventDefault(): Prevent default behavior to ensure smooth dragging.

dragging = this: Set the dragging variable to the element that triggered the mousedown event.

mouseX and mouseY: Capture the initial mouse position.

eleX and eleY: Capture the initial position of the element being dragged.

Attach mousemove and mouseup event listeners to the document to handle the drag and drop actions.

deltaMouseX and deltaMouseY: Calculate the change in mouse position since the drag started.

Update the left and top styles of the dragging element based on the change in mouse position and the element's initial position.

Set dragging to false to indicate that no element is being dragged anymore.

Optionally, you could remove the mousemove and mouseup event listeners here to clean up, although not strictly necessary.

All the drag function to set up the drag-and-drop functionality for all draggable elements.

Creating a drag and drop game using HTML, CSS, and JavaScript is an exciting way to improve your web development skills. This project covers the essentials of DOM manipulation and event handling, providing a solid foundation for more advanced projects. Give it a try, and see how creative you can get with your own variations!

For further actions, you may consider blocking this person and/or

We're a place where coders share, stay up-to-date and grow their careers.

---

## Technology Activities Mouse Practice Drag Click Drop Bundle Computer Lab

`https://www.teacherspayteachers.com/Product/Mouse-Practice-Drag-Click-Drop-Activities-Bundle-Computer-Lab-Back-to-School-10428526`

Technology Activities Mouse Practice Drag Click Drop Bundle Computer Lab

Technology Activities Mouse Practice Drag Click Drop Bundle Computer Lab

"Students really enjoy these when I give them. Excellent for g1 mouse reinforcement and for teaching KG."

"My students loved using this resource during our circle time. They were engaged and excited to move the objects. I will be using again in the coming school year. I loved it. ❤️"

is perfect for K-3 elementary students to practice using their

. It is also a great way to practice letter word matching, shapes, colors, counting, and emotions. Also, use a

to practice mouse skills in computer lab or regular classroom.

The activity is easy for teachers to set up and requires no prep, so it is perfect for starting off the day, fun Fridays, early finishers, technology - computer class, or for practicing following directions.

To use the activity, students simply drag and drop the objects on the screen into the correct places. For example, they might drag and drop letters to match them to words or drag and drop shapes to match them to their names.

This can work with a mouse or trackpad. There are two instruction slides inside to explain how to click and drag with each.

Included in EACH monthly Mouse Skills Practice:

Here are some specific examples of activities that students can do with this digital mouse practice activity:

Students can drag and drop letters to match them to words, such as matching the letter "A" to the word "apple."

Students can drag and drop shapes to match them to their names, such as matching a triangle to the word "triangle."

Students can drag and drop colored objects to match them to their names, such as matching a red apple to the word "red."

Students can drag and drop objects to count them, such as counting the number of pumpkins on the screen

This digital mouse practice activity is a fun and engaging way for students to practice their mouse skills and learn about a variety of topics at the same time. It is also a great way for students to practice following directions and work independently.

with this bundle and get activities for the entire year! Assign new slides each month.

& be notified of new resources. Did you know when new resources are added in my store, they are

& know how you used this in your classroom. When you review, you earn TPT credits for

As always, please contact me with any questions! Thank you for your support.

Reported resources will be reviewed by our team.

Technology Activities Mouse Practice Drag Click Drop Bundle Computer Lab

12 months of activities. Each month contains 30 slides.

"Students really enjoy these when I give them. Excellent for g1 mouse reinforcement and for teaching KG."

"My students loved using this resource during our circle time. They were engaged and excited to move the objects. I will be using again in the coming school year. I loved it. ❤️"

Back to School Tech Computer Lab Activities Mouse Practice Typing Keyboarding

The Ultimate Tech Skills Bundle: Monthly Mouse &amp; Typing Practice for the Year! Ready to build your students' computer confidence from the ground up? This Ultimate Tech Skills Bundle is your one-stop shop for teaching foundational mouse and keyboarding skills! Packed with a full year of no-prep,

is perfect for K-3 elementary students to practice using their

. It is also a great way to practice letter word matching, shapes, colors, counting, and emotions. Also, use a

to practice mouse skills in computer lab or regular classroom.

The activity is easy for teachers to set up and requires no prep, so it is perfect for starting off the day, fun Fridays, early finishers, technology - computer class, or for practicing following directions.

To use the activity, students simply drag and drop the objects on the screen into the correct places. For example, they might drag and drop letters to match them to words or drag and drop shapes to match them to their names.

This can work with a mouse or trackpad. There are two instruction slides inside to explain how to click and drag with each.

Included in EACH monthly Mouse Skills Practice:

Here are some specific examples of activities that students can do with this digital mouse practice activity:

Students can drag and drop letters to match them to words, such as matching the letter "A" to the word "apple."

Students can drag and drop shapes to match them to their names, such as matching a triangle to the word "triangle."

Students can drag and drop colored objects to match them to their names, such as matching a red apple to the word "red."

Students can drag and drop objects to count them, such as counting the number of pumpkins on the screen

This digital mouse practice activity is a fun and engaging way for students to practice their mouse skills and learn about a variety of topics at the same time. It is also a great way for students to practice following directions and work independently.

with this bundle and get activities for the entire year! Assign new slides each month.

& be notified of new resources. Did you know when new resources are added in my store, they are

& know how you used this in your classroom. When you review, you earn TPT credits for

As always, please contact me with any questions! Thank you for your support.

Reported resources will be reviewed by our team.

Such an awesome resource to use with kindergarteners in a tech classroom!

I purchased this for Preschool Tech classes to build mouse skills when a site that I used became subscription only. This was well worth the money and I can use this again next year. 12 months of great themed mouse skill activity slides that engaged the students and required little teacher assistance and lots of student skill practice. This was exactly what I was looking for. Great resource!

This made my life so much easier! It was well put together and easy to follow along!

Students really enjoy these when I give them. Excellent for g1 mouse reinforcement and for teaching KG.

Autism, Emerging bilinguals, Learning difficulties, Mild to severe disabilities

My students loved using this resource during our circle time. They were engaged and excited to move the objects. I will be using again in the coming school year. I loved it. ❤️

This activity was great at the beginning of the year. Thank  you

My students really enjoyed this activity and I appreciate how easy it is to modify for students who need extra help. Thank you - I really use a lot of your activities. They're all amazing.

This resource helped my littles with their skills on the Chromebook.  Great resource!

TPT is the largest marketplace for PreK-12 resources, powered by a community of educators.

Get our weekly newsletter with free resources, updates, and special offers.

35,000 worksheets, games, and lesson plans

Essential reference for synonyms and antonyms

Comprehensive resource for word definitions and usage

Spanish-English dictionary, translator, and learning

French-English dictionary, translator, and learning

Diccionario inglés-español, traductor y sitio de aprendizaje

---

## Drag Drop Learning Games | Teachers Pay Teachers

`https://www.teacherspayteachers.com/store/drag-drop-learning-games/category-matching-games-digital-255844`

Drag Drop Learning Games | Teachers Pay Teachers

Rated 4.91 out of 5, based on 4252 reviews

I am a self-employed educational resource developer with a background in web design and computer programming.

DIGITAL Merry Christmas Memory Matching Card Game

Your kiddos will love trying to remember and match the different Christmas vocabulary words and icons in this challenging and fun interactive memory game. There are two versions of the game to choose from, one with 10 pairs of items to match and the other with 15 pairs. There is also an option for playing with one player or two players or teams. When playing alone, a clock is provided, and the number of card turns is tracked. This digital resource integrates seamlessly with your Google Classroom

DIGITAL US Geography Fifty State Memory Matching Card Game

This fun interactive matching game includes all fifty states of the USA.  Students click or tap to turn the cards over looking for two of the same state.  The cards feature a picture of the state's shape as well as its name.  There is a timer and a card counter included, so they can play several times and try to improve their score.  The game changes every time. This digital memory game is a web based app and should work on any PC, Mac, Chromebook, desktop, laptop, or tablet that is connected to

Digital Alphabet Memory Game - Upper and Lower Case Matching

This fun interactive matching game covers all 26 upper and lower case letters of the English alphabet.  Students click or tap to turn the cards over looking for cards that have the same letter - once in its uppercase form and once in its lowercase.  There is a timer and a card counter included, so they can play several times and try to improve their score.  The game changes every time and includes fun noises along the way. This digital memory game is a web based app and should work on any PC, Ma

DIGITAL Zoo Animals Memory Matching Card Game

This fun interactive matching game includes 25 different animals kids might find at the zoo.  Students click or tap to turn the cards over looking for two of the same animal.  The cards feature a picture of the animal as well as its name.  There is a timer and a card counter included, so they can play several times and try to improve their score.  The game changes every time.

This digital memory game is a web based app and should work on any PC, Mac, Chromebook, desktop, laptop, or tablet that

DIGITAL Dinosaur Themed Memory Matching Card Game

Animate your next virtual get together with this fun dinosaur themed memory matching game.  Your kiddos (or guests) will love trying to remember and match the different pictures in this challenging and engaging interactive memory game.   It is a great way to train visual recall and overall memory development.  There are two versions of the game to choose from, one with 20 items to match and the other with 30 items. There is also an option for playing with one player or two players or teams. When

DIGITAL Valentine's Day Memory Matching Card Game

Animate your next virtual get together with this fun Valentine’s Day memory matching game.  Your kiddos (or guests) will love trying to remember and match the different tea party items in this challenging and engaging interactive memory game.   It is a great way to train visual recall and overall memory development.  There are two versions of the game to choose from, one with 20 items to match and the other with 30 items. There is also an option for playing with one player or two players or team

DIGITAL Moon Phases Memory Matching Card Game

This fun interactive matching game includes the names and images for the eight phases of the moon.  Students click or tap to turn the cards over looking for two of the same phase.  There is a timer and a card counter included, so you can play several times and try to improve your score.  The game changes every time. This digital memory game is a web based app and should work on any PC, Mac, Chromebook, desktop, laptop, or tablet that is connected to the internet.  There is nothing additional to

DIGITAL Community & Safety Signs Memory Matching Card Game

Your students will love playing this challenging interactive memory game featuring 33 community and safety signs. There are two versions of the game to choose from, one with 10 pairs of signs to match and the other with 15 pairs. There is also an option for playing with one player or two players or teams. When playing alone, a clock is provided, and the number of card turns is tracked. This digital resource integrates seamlessly with your Google Classroom if you wish. You merely need to click on

DIGITAL Homophones Memory Matching Card Game

Your kiddos will love trying to remember and match the different homophones in this challenging and engaging interactive memory game.   It is a great way to review vocabulary and spelling while having fun playing a game.  Everyone is sure to enjoy uncovering the cute pictures that go along with the words. There are two versions of the game to choose from, one with 10 pairs of homophones to match and the other with 15 pairs. There is also an option for playing with one player or two players or te

DIGITAL 1st Grade Sight Word Memory Matching Card Game

This fun interactive matching game covers 41 first grade sight words.  Students click or tap to turn the cards over looking for cards that have the same word.  There is a timer and a card counter included, so they can play several times and try to improve their score.  The game changes every time and includes fun noises along the way. This digital memory game is a web based app and should work on any PC, Mac, Chromebook, desktop, laptop, or tablet that is connected to the internet.  There is not

DIGITAL Sight Word Memory Matching Game - BUNDLED

DIGITAL Synonym Memory Matching Card Game

This fun interactive matching game covers 65 different pairs of synonyms.  Students click or tap to turn the cards over looking for words that have similar meanings.  There is a timer and a card counter included, so they can play several times and try to improve their score.  The game changes every time. This digital memory game is a web based app and should work on any PC, Mac, Chromebook, desktop, laptop, or tablet that is connected to the internet.  There is nothing additional to download or

DIGITAL Polar Animal Game - Memory Matching Cards - Arctic Themed

Animate your next virtual get together with this fun polar themed memory matching game.  Your kiddos (or guests) will love trying to remember and match the different items in this challenging and engaging interactive memory game.   It is a great way to train visual recall and overall memory development.  There are two versions of the game to choose from, one with 20 items to match and the other with 30 items. There is also an option for playing with one player or two players or teams. When playi

DIGITAL Donut Matching Game - Doughnut Memory Game

Your kiddos will love trying to remember and match the delicious doughnuts in this challenging and fun interactive memory game. There are two versions of the game to choose from, one with 10 pairs of doughnuts to match and the other with 15 pairs. There is also an option for playing with one player or two players or teams. When playing alone, a clock is provided, and the number of card turns is tracked.   This digital resource integrates seamlessly with your Google Classroom if you wish. You mer

DIGITAL Pre Primer Sight Word Memory Matching Card Game

This fun interactive matching game covers 47 pre-primer sight words.  Students click or tap to turn the cards over looking for cards that have the same word.  There is a timer and a card counter included, so they can play several times and try to improve their score.  The game changes every time and includes fun noises along the way. This digital memory game is a web based app and should work on any PC, Mac, Chromebook, desktop, laptop, or tablet that is connected to the internet.  There is noth

DIGITAL Sight Word Memory Matching Game - BUNDLED

DIGITAL Spring Vocabulary Memory Matching Card Game

Your kiddos will love trying to remember and match the spring themed pictures to thier names in this challenging and fun interactive memory game. This is a great game for adults too!  There are two versions of the game to choose from, one with 10 pairs of items to match and the other with 15 pairs. There is also an option for playing with one player or two players or teams. When playing alone, a clock is provided, and the number of card turns is tracked. This digital resource integrates seamless

DIGITAL 2D Shapes Memory Matching Card Game

Your kiddos will love trying to remember and match the different two dimensional geometric shapes to their name in this challenging and fun interactive memory game. There are two versions of the game to choose from, one with 10 pairs of shapes to match and the other with 15 pairs. There is also an option for playing with one player or two players or teams. When playing alone, a clock is provided, and the number of card turns is tracked. This digital resource integrates seamlessly with your Googl

DIGITAL African Animal Safari Themed Memory Matching Card Game

Your students will love going on a safari adventure with this challenging and fun interactive memory. There are two versions of the game to choose from, one with 10 pairs of items to match and the other with 15 pairs. There is also an option for playing with one player or two players or teams. When playing alone, a clock is provided, and the number of card turns is tracked. This digital resource integrates seamlessly with your Google Classroom if you wish. You merely need to click on the Google

DIGITAL Fairytale Themed Memory Matching Card Game

Your kiddos will love trying to remember and match the fairy tale elements in this challenging and fun interactive memory game. There are two versions of the game to choose from, one with 10 pairs of items to match and the other with 15 pairs. There is also an option for playing with one player or two players or teams. When playing alone, a clock is provided, and the number of card turns is tracked.   This digital resource integrates seamlessly with your Google Classroom if you wish. You merely

Ice Cream Themed Memory Matching Card Game

Your kiddos will love trying to remember and match the different ice cream treats in this challenging and fun interactive memory game. There are two versions of the game to choose from, one with 10 pairs of treats to match and the other with 15 pairs. There is also an option for playing with one player or two players or teams. When playing alone, a clock is provided, and the number of card turns is tracked. This digital resource integrates seamlessly with your Google Classroom if you wish. You m

DIGITAL Emotions and Feelings Memory Matching Card Game

This fun interactive matching game includes 19 different emoticons to match with the emotion they express.  Students click or tap to turn the cards over looking for an emoticon and an emotion that match.  There is a timer and a card counter included, so you can play several times and try to improve your score.  The game changes every time.

This digital memory game is a web based app and should work on any PC, Mac, Chromebook, desktop, laptop, or tablet that is connected to the internet.  There

I am a self-employed educational resource developer with a background in web design and computer programming.

Published author with a dozen or so puzzle books to my name.

I am originally from California but have lived in France for almost half of my life.

TPT is the largest marketplace for PreK-12 resources, powered by a community of educators.

Get our weekly newsletter with free resources, updates, and special offers.

35,000 worksheets, games, and lesson plans

Essential reference for synonyms and antonyms

Comprehensive resource for word definitions and usage

Spanish-English dictionary, translator, and learning

French-English dictionary, translator, and learning

Diccionario inglés-español, traductor y sitio de aprendizaje

---

## ⚠️ Paginas que NAO deram texto

- `https://www.computerskillslab.com/` — HTTP 403
- `https://codepen.io/noyiri/pen/zeoRwB` — HTTP 403
