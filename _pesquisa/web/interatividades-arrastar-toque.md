# 🔎 Pesquisa: interatividades-arrastar-toque

> Busca: `drag and drop touch pointer events best practices children educational HTML5 game touch-action ghost click`

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

## GitHub - drag-drop-touch-js/dragdroptouch: Polyfill that enables HTML5 drag drop support on mobile (touch) devices. · Gi

`https://github.com/drag-drop-touch-js/dragdroptouch`

GitHub - drag-drop-touch-js/dragdroptouch: Polyfill that enables HTML5 drag drop support on mobile (touch) devices. · GitHub

You signed in with another tab or window.

You switched accounts on another tab or window.

You must be signed in to change notification settings

Polyfill that enables HTML5 drag drop support on mobile (touch) devices.

The HTML5 specification includes support for drag and drop operations.

Unfortunately, this specification is based on mouse events, rather than

pointer events, and so most mobile browsers do not implement it. As such,

applications that rely on HTML5 drag and drop have reduced functionality

class is a polyfill that translates touch events into

standard HTML5 drag drop events. If you add the polyfill to your pages,

drag and drop operations should work on mobile devices just like they

This demo should work on desktop as well as on mobile devices, including

iPads and Android tablets. To test this on a desktop, turn on "responsive

design mode", which is both a button in the browser developer tools, as

This package lives in the npm registry as

and can be installed with any package manager that can pull from the

npm install -s @dragdroptouch/drag-drop-touch

yarn install @dragdroptouch/drag-drop-touch

polyfill script to your page to enable drag and drop on devices with touch input:

and immediately enables it so that you do not need to write any code yourself.

If omitted, the library will instead set up a

DragDropTouch.enable(dragRoot, dropRoot, options)

All three arguments are optional. If left off,

polyfills the entire page. If you only want the polyfill to apply to specific

, which is required. If left off, you'll probably

Uncaught SyntaxError: import.meta may only appear in a module

You can also load the library using a CDN solution such as jsDelivr:

https://cdn.jsdelivr.net/npm/@dragdroptouch/drag-drop-touch@latest/dist/drag-drop-touch.esm.min.js

As an ES module, you can also use this polyfill as an import in any other script:

// Set up the default full page polyfill:

// Or, explicitly polyfill only certain elements

// Or even explicitly polyfill only certain elements with non-default behaviour

polyfill attaches listeners to the document's touch events:

, it checks whether the target element has the draggable

attribute or is contained in an element that does. If that is the case, it

saves a reference to the "drag source" element and prevents the default

, it checks whether the touch has moved a certain threshold

distance from the origin. If that is the case, it raises the

event and continues monitoring moves to fire

To avoid interfering with the automatic browser translation of some touch events

into mouse events, the polyfill performs a few additional tasks:

the user touches a draggable element but doesn't start dragging,

event when there's a new touchstart right after a click,

event when the touch lasts a while but the user doesn't

The following options can be passed into the enabling function to change how the

is a flag that determines whether to allow scrolling when

a drag reaches the edges of the screen. This can be either

is the number of milliseconds we'll wait before the

polyfill triggers a context menu event on long press. This value is 900 by

determines how see-through the "drag placeholder", that's

attached to the cursor while dragging, should be. This value is a number in

the interval [0, 1], where 0 means fully transparent, and 1 means fully opaque.

is the size of the "hot region" at the edge of the

screen as a percentage value on which scrolling will be allowed, if the

flag is true (which is its default value). This value is

is the number of pixels to scroll if a drag event occurs

within a scrolling hot region. This value is 10 by default.

is the number of pixels that a touchmove needs to

actually move before the polyfill switches to drag mode rather than click mode.

is a flag that tells the polyfill whether a a long-press

is required before polyfilling drag events. This value can be either

is a flag that determines whether the polyfill should be

enabled irrespective of whether the browser indicates that it's running on

a touch-enabled device or not. This value is

: is the number of milliseconds the polyfill will wait

before it considers an active press to be a "long press". This value is 400

is the number of pixels we allow a touch event to drift

over the course of a long press start. This value is 25 by default.

is the drift in pixels that determines whether

a long press actually starts a long press, or starts a touch-drag instead.

Thanks to Eric Bidelman for the great tutorial on HTML5 drag and drop:

Thanks also to Chris Wilson and Paul Kinlan for their article on mouse and touch events:

Thanks to Tim Ruffles for his iOS shim code which was inspiring:

If you wish to work on this library, fork and clone the repository, then run

to install all the dependency, followed by a one-time

, which will install the necessary components for running

integration tests. Build testing consists of linting the source code using

, and compiling it into three bundles (debug, normal, and minified) using

statements preserved, useful for when tests fail to pass and you're trying to find out what's actually happening.

To manually test in the browser, you can run

URL that is printed to the console once the initial build tasks have finished.

This runs a local server that lets you run the demo page, but with the

instead, which preserves all debug statements used in the TypeScript source.

To add your own debug statements, use the

a normal statement, or multiple statements wrapped in a new block.

Polyfill that enables HTML5 drag drop support on mobile (touch) devices.

You can’t perform that action at this time.

---

## Integrating Touch Support to Drag-and-Drop Interfaces — Chariot Solutions

`https://chariotsolutions.com/blog/post/integrating-touch-support-to-drag-and-drop-interfaces/`

Integrating Touch Support to Drag-and-Drop Interfaces — Chariot Solutions

Integrating Touch Support to Drag-and-Drop Interfaces

, we went over how to use the HTML Drag-and-Drop interface, which is a well-supported web API that’s available to use across major web browsers. Here, we will go over how we can extend our

to support touch interactions so that our application can be used across various devices but still provide the same functionality the user expects.

For demonstration purposes I will be simulating a virtual mobile device using the Chrome Developer Tools within the Chrome browser. With this limitation we can keep external setup to a minimum as possible.

Throughout the article I will provide a link to a CodePen that has playable demos to supplement the concepts described here. The examples do require additional setup to enable touch controls. Here is what this looks like specifically for the Chrome browser:

Open Chrome Developer Tools: Option + Command/Ctrl + I or right click inside the browser window to show a context menu and select “Inspect”.

Enable Device Toolbar: Command/Ctrl + Shift + M or selecting the icon from the menu.*

Choose a device to see how the example looks across various devices. You can also stretch the corners as well.

* Support for other browsers may be limited. I have noticed on Chrome that touch controls are enabled automatically when the Device Toolbar is enabled but on other browsers there could be other steps needed. For example, on Firefox it is the “Responsive Design Mode” that we want to see here. Firefox, also explicitly forces you to select the “Enable touch simulation” to toggle touch support.

In today’s digital landscape, ensuring your web applications are fully accessible and functional across all devices is more crucial than ever. With a significant portion of internet traffic coming from mobile devices, integrating touch support into your web applications is not just an enhancement but a necessity. The first part of our blog series introduced the implementation of the Drag-and-Drop API for desktop browsers. However, as we extend this functionality in the second part here, we focus on touch surfaces, which are predominant in mobile devices. By adapting drag-and-drop capabilities to recognize touch events, we can offer a seamless, intuitive user experience that mirrors interactions users expect on their smartphones.

Why isn’t touch support enabled automatically in the previous example? The Drag and Drop API uses the DragEvent interface which in turn inherits its properties from the MouseEvent interface. On a mobile phone typically we don’t have access to a pointing device such as a mouse. For touch surfaces, such as the screen of a smartphone, we will need to listen for TouchEvents and explore how to extend our drag-and-drop demo to support these events via a “touch-drag” gesture, ensuring a seamless user experience across various devices.

Touch events are similar to mouse events but are specifically designed to interpret interactions from a finger or stylus input on a touch-sensitive surface such as a touchscreen or a trackpad.

The primary touch events we will focus on are:

: A touch point is placed on the touch surface.

: A touch point is moved along the touch surface.

: A touch point is removed from the touch surface.

, using the touch simulator, we demonstrate pressing down on the surface, moving the recorded touch point a certain distance, and then finally ending the touch by reducing the pressure until the contact of the touch point is no longer registered.*

* Simulating touch support requires additional setup. Please ensure all steps were followed in the ‘How to Use the Examples’ section.

Adapting a Drag-and-Drop Interface for Touch Input

To make our drag-and-drop setup touch compatible, we need to map TouchEvents to the corresponding mouse events used in the drag-and-drop API. In the following sections we go through the initial setup to hook into the touch event lifecycle, how to map specific touch events with their DragEvent counterparts to achieve the same user experience, and finally updating the view to show the final positions of our elements.

demo that is shown below. The initial code listens for dragstart and dragend events on draggable elements and handles the dragover event on containers to dynamically decide where within the container the dragged element should be dropped. This setup works perfectly on desktops where mouse events are the primary mode of interaction.

const draggables = document.querySelectorAll('.draggable');

const containers = document.querySelectorAll('.container');

draggable.addEventListener('dragstart', () => {

draggable.addEventListener('dragend', () => {

container.addEventListener('dragover', e => {

const afterElement = getDragAfterElement(container, e.clientY);

const draggable = document.querySelector('.dragging');

container.insertBefore(draggable, afterElement);

We extend our functionality to respond to touchstart, touchmove, and touchend events, which are the touch equivalents of the mousedown, mousemove, and mouseup events that help power the drag-and-drop demo.

Initializing Touch Interactions: We start by listening to the touchstart event on the draggable elements. When a touch begins, we activate the dragging state and prevent the default action, which typically involves scrolling or zooming.

Handling Touch Movement: During the touchmove event, we update the position of the draggable element in real-time, making it follow the user’s finger. Additionally, we show a placeholder within potential drop containers to indicate where the element will land if released.

Completing the Touch: On touchend, we finalize the drag operation by moving the draggable element to its new position indicated by the placeholder and then clean up by removing the placeholder and resetting the styles.

draggable.addEventListener("touchstart", (e) => {

draggable.addEventListener("touchmove", (e) => {

draggable.style.left = `${touch.clientX}px`;

draggable.style.top = `${touch.clientY}px`;

.elementFromPoint(touch.clientX, touch.clientY)

const afterElement = getDragAfterElement(

potentialContainer.insertBefore(placeholder, afterElement);

potentialContainer.appendChild(placeholder);

draggable.addEventListener("touchend", () => {

if (activeElement && placeholder && placeholder.parentNode) {

placeholder.parentNode.insertBefore(activeElement, placeholder);

Here is what the demo looks like now. The first example is using drag events and the second example shows touch events.

As we utilize touch simulators within Chrome Developer Tools in our development process, it’s important to remember that these tools, while incredibly useful, do not fully replicate the nuances of physical interactions on actual devices. Simulators help bridge the initial gap in the development cycle by providing a convenient and quick way to test touch interactions. However, to ensure that our applications provide the best user experience and function correctly across various devices, exhaustive testing on physical devices is crucial. Real-world testing allows us to observe and rectify issues related to touch sensitivity, gesture recognition, and overall user interface responsiveness, which might not be fully apparent in a simulated environment. Therefore, while simulators are beneficial for early testing, they should be complemented by comprehensive testing on actual hardware to ensure the highest quality of the final product.

By extending the drag-and-drop functionality to support touch events, you can enhance the mobile user experience of your web applications. This allows users on all types of devices to interact with your application in an intuitive and natural manner, making your application more accessible and user-friendly. This is definitely not everything that can be achieved. There are more advanced touch motions that can be handled such as multiple touch points on a surface or a pinch-and-zoom gesture to handle scaling of an element. I hope the examples provided can help as a starting point in your next application.

---

## interact.js - JavaScript drag and drop, resizing and multi-touch
        gestures for modern browsers

`https://interactjs.io/docs/action-options/`

interact.js - JavaScript drag and drop, resizing and multi-touch

Help Provide Humanitarian Aid to Ukraine.

are used to enable and configure actions for target elements. They all have some common options as well as some action-specific options and event properties.

Drag, resizem and gesture interactions fire

s which have the following properties common to all action types:

The element that is being interacted with

The Interactable that is being interacted with

The Interaction that the event belongs to

Page x and y coordinates of the starting event

Client x and y coordinates of the starting event

to simply allow/disallow the action or an object with properties to change certain settings.

is used to limit the number of concurrent interactions that can target an interactable. By default, any number of interactions can target an interactable.

By default only 1 interaction can target the same interactable+element combination. If you want to allow multiple interactions on the same target element, set the

then drag, resize and gesture actions will have to be started with a call to

The action will start after the pointer is held down for the given number of milliseconds.

Change inertia settings for drag, and resize. See

feature is enabled, interact will style the cursor of draggable and resizable elements as you hover over them.

// the library uses biderectional arrows <-> by default,

// but we want specific arrows (<- or ->) for each diriection

, but that will disable cursor styling for all actions. To disable or change the cursor for each action, you can set a

function which takes info about the current interaction and returns the CSS cursor value to set on the target element.

or an HTMLElement) when a drag or resize move happens at the edge of the container.

option lets you specify a target CSS selector or Element which must be the target of the pointer down event in order for the action to start. This option available for drag, resize and gesture, as well as

option, you may specify handles for each action separately and for all your pointerEvents listeners.

be children of the target interactable element.

lets you specify elements within your target with which to avoid starting actions. This is useful when certain elements need to maintain default behavior when interacted with. For example, dragging around a text/contentEditable, by wrapping this object with a draggable element and ignoring the editable content you maintain the ability to highlight text without moving the element.

Enable the action for the Interactable. If the options object has no

---

## interact.js - JavaScript drag and drop, resizing and multi-touch
        gestures for modern browsers

`https://interactjs.io/docs/`

interact.js - JavaScript drag and drop, resizing and multi-touch

Help Provide Humanitarian Aid to Ukraine.

interact.js is a JavaScript library for drag and drop, resizing and multi-touch gestures for modern browsers. Its free and open source version comes with powerful options like inertia and modifiers for snapping and restricting.

across different browsers and devices and provide convenient ways to

pretend that the user’s pointer moved in a way that it wasn’t really moved

interact.js doesn’t move elements for you

. Styling an element so that it moves while a drag happens has to be done from your own event listeners. This way, you’re in control of everything that happens.

🌟 If you prefer to have feedback out-of-the-box, have a look at

. It comes with built-in hardware accelerated feedback, list reordering, spring physics, Vue & React components and more.

, the basic steps to setting up your targets and interactions are:

Add event listeners to provide visual feedback and update your app’s state.

// target elements with the "slider" class

// keep the drag coords within the element

// target elements with the "slider" class

// keep the drag coords within the element

function takes an element or a CSS selector string and returns an

object which has various methods to configure actions and event listeners. Pointer interactions of down → move → up sequences begin drag, resize, or gesture actions. By adding event listener functions for these action, you can respond to

s which provide pointer coordinates, speed, element size, etc.

interact.js supports 3 basic action types which are triggered by pointer down → move → up sequences:

for moving elements or drawing on a canvas. This can be combined with

for watching the size and position of an element while the pointer is used to move one or two of the element’s edges.

for 2-finger gestures with angle, scale, etc. data.

Pro builds on the draggable action to provide

feature for drag and drop rearranging of lists of elements.

---

## How to work with JavaScript Drag and drop for touch devices?

`https://www.tutorialspoint.com/article/How-to-work-with-JavaScript-Drag-and-drop-for-touch-devices`

How to work with JavaScript Drag and drop for touch devices?

How to work with JavaScript Drag and drop for touch devices?

JavaScript drag and drop functionality provides an intuitive way to move elements within web pages. While the HTML5 Drag and Drop API works well on desktop, touch devices require additional handling to ensure proper functionality.

To make an element draggable in HTML5, add the

attribute to the element. By default, images and text selections are draggable, but other elements need this attribute.

<div class="item" draggable="true">Drag me</div>

The drag and drop process involves two sets of events:

- Fires when dragged element enters drop zone

- Fires continuously while over drop zone

- Fires when dragged element leaves drop zone

- Fires when element is dropped on target

<div id="div1" ondrop="drop(event)" ondragover="allowDrop(event)">

<img src="/javascript/images/javascript-mini-logo.jpg" draggable="true" ondragstart="drag(event)" id="drag1" width="88" height="31">

<div id="div2" ondrop="drop(event)" ondragover="allowDrop(event)"></div>

ev.dataTransfer.setData("text", ev.target.id);

var data = ev.dataTransfer.getData("text");

ev.target.appendChild(document.getElementById(data));

Touch devices don't support the HTML5 Drag and Drop API natively. To make drag and drop work on touch devices, you need to handle touch events:

<div class="draggable" id="draggable"></div>

let startX, startY, initialLeft, initialTop;

const draggable = document.getElementById('draggable');

draggable.addEventListener('mousedown', startDrag);

document.addEventListener('mousemove', drag);

document.addEventListener('mouseup', stopDrag);

draggable.addEventListener('touchstart', startDragTouch);

document.addEventListener('touchmove', dragTouch);

document.addEventListener('touchend', stopDrag);

draggable.style.left = (initialLeft + deltaX) + 'px';

draggable.style.top = (initialTop + deltaY) + 'px';

draggable.style.left = (initialLeft + deltaX) + 'px';

draggable.style.top = (initialTop + deltaY) + 'px';

CSS property to prevent default touch behaviors

Handle both mouse and touch events for cross-device compatibility

Comparison: Desktop vs Touch Implementation

While HTML5 provides native drag and drop for desktop browsers, touch devices require custom event handling using touch events. For universal compatibility, implement both approaches in your applications.

---

## Understanding Success Criterion 2.5.7: Dragging Movements | WAI | W3C

`https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements`

Understanding Success Criterion 2.5.7: Dragging Movements | WAI | W3C

For any action that involves dragging, provide a simple pointer alternative.

Some people cannot use a mouse to drag items.

or the functionality is determined by the

This requirement applies to web content that interprets pointer actions (i.e., this does not apply to actions that are required to operate the user agent or assistive technology).

The intent of this success criterion is to ensure functionality that uses a dragging movement has another

mode of operation without the need for the dexterity required to drag elements.

Some people cannot perform dragging movements in a precise manner. Others use a specialized or adapted input device, such as a trackball, head pointer, eye-gaze system, or speech-controlled mouse emulator, which may make dragging cumbersome and error-prone.

When an interface implements functionality that uses dragging movements, users perform four discrete actions:

tap or click to establish a start-point, then

performing a repositioning of the pointer, before...

Not all users can accurately press and hold that contact while also repositioning the pointer. An alternative method must be provided so that users with mobility impairments who use a pointer (mouse, pen, or touch contact) can use the functionality.

Example of a typical horizontal range slider being dragged.

For example, while a range slider is operated by dragging the slider thumb, an alternative pointer method to change the value is to click/tap anywhere on the slider track to move the thumb to that position.

Example of a typical draggable content carousel.

This requirement is separate from keyboard accessibility because people using a touchscreen device may not use a physical keyboard. Keyboard specific interactions such as tabbing or arrow keys may not be possible when encountering a drag and drop control. Note, however, that providing a text input can be an acceptable single-pointer alternative to dragging. For example, an input beside a slider could allow any user to enter a precise value for the slider. In such a situation, the on-screen keyboard that appears for touch users offers a single-pointer means of entering an alphanumeric value.

alternative can't exclusively rely on a path-based gesture, such as swiping or "flicking", as this would fail the requirements of

apply to scrolling and dragging gestures enabled by the user agent, as it's the user agent's responsibility to provide an accessibility-supported mechanism for these. In browsers operated with a mouse, users generally scroll content by dragging the browser's scrollbar. In touchscreen browsers, users generally scroll by "dragging" the page on the screen. Similarly, most touchscreen browsers provide a "drag to refresh" gesture to refresh/reload a page. In all these cases, the functionality is provided by the browser, rather than implemented by the content – so this criterion

that make a section of content scrollable, as the actual scrolling mechanism even in these situations is provided by the user agent. The criterion

apply if content actively suppresses the user agent's own scrolling functionality and/or implements its own scrolling mechanism – in these cases, the scrolling/dragging gesture is interpreted and processed by the content itself, and thus falls under the responsibility of the content author.

Relationship to keyboard accessibility requirements

require dragging features to be keyboard accessible. However, achieving keyboard equivalence for a dragging operation does not automatically meet this success criterion, unless that equivalent keyboard operation also provides controls that can be clicked or tapped with a pointer. It is possible to create an interface that works with dragging and keyboard controls, but still does not work using only clicks or taps. While many designs can be created for a dragging alternative which address both keyboard accessibility and operability by single pointer operation, the two requirements are evaluated independently.

Distinguishing dragging movements from path-based pointer gestures

This success criterion applies to dragging movements in general, which involve the user "grabbing" an element and moving it to another position. Once the pointer engages with a target to pick up/grab it, the direction of the dragging movement does not factor into the interaction at all.

is concerned with gestures that are path-based, as well as multi-point gestures. For pointer gestures, the direction of the pointer movement matters. However, if an action involves

a dragging movement (such as grabbing a slider thumb, moving it, and then releasing it)

a path-based gesture (if the slider requires the user to exactly follow its track, or otherwise the user's grip on the slider thumb is "lost"), it may fail against the requirements of

Alternatives for dragging movements on the same page

Where functionality can be executed via dragging movements and an equivalent option exists that allows for single-pointer access without dragging, this success criterion is satisfied. It does not have to be the same component, so long as the functionality is equivalent. An example is a color wheel where a color can be changed by dragging an indicator. In addition, text fields for the numerical input of color values allow the definition of a color without requiring dragging movements. (Note that a text input is considered device agnostic; although the purpose is to enter characters, text entry can take place through voice, pointer or keyboard.)

Users who struggle with performing dragging movements can still operate an interface with a pointer interface.

A map allows users to drag the view of the map around, and the map has up/down/left/right buttons to move the view as well.

A sortable list of elements may, after tapping or clicking on a list element, provide adjacent controls for moving the element up or down in the list by simply tapping or clicking on those controls.

A task board that allows users to drag and drop items between columns also provides an additional pop-up menu after tapping or clicking on items for moving the selected element to another column by tapping or clicking on pop-up menu entries.

A radial control widget (color wheel) where the value can be set by dragging the marker for the currently selected color to another position, also allows picking another color value by tapping or clicking on another place in the color wheel.

A range slider control widget, where the value can be set by dragging the visual indicator (thumb) showing the current value, allows tapping or clicking on any point of the slider track to change the value and set the thumb to that position.

A widget where you can drag a gift to one person in a photo of a group of people also has a menu alternative where users can select the person that should receive the gift from the menu.

A graphical interface allows the user to draw a selection rectangle on an image by first setting one corner of the rectangle on the pointer down-event, dragging the opposite corner with the pointer, and then setting that second corner position on the pointer up-event. As a non-drag alternative, the user can enable a selection mode, click/tap the first corner, then click/tap the opposite corner, without the need to keep the pointer pressed and dragging.

In an online quiz, users are expected to draw a connecting line between each item in one column and its respective counterpart item in a second column. Users who can't (or don't want to) draw those lines manually can also just click/tap on one item in the first column, then click/tap on an item in the second column, and the connecting line is drawn automatically.

A kanban widget with several vertical columns representing states in a defined process allows the user drag elements to move them to another column. The user can also accomplish this by selecting the element with a single tap or click, and then activating an arrow button to move the selected element.

A news site has a horizontal carousel with different news teasers that can be dragged to move items into view. It also offers forward and backward buttons on the left and right of the carousel, to move the carousel to the previous and next item with a simple click/tap. These buttons can be visible (for instance, as large arrow icons) or visually hidden (but still operable with a pointer).

Each item in this section represents a technique or combination of techniques

that the Accessibility Guidelines Working Group deems sufficient for meeting this success criterion.

A technique may go beyond the minimum requirement of the criterion. There may be other ways of meeting the criterion not covered by these techniques.

For information on using other techniques, see

Understanding Techniques for WCAG Success Criteria

particularly the "Other Techniques" section.

G219: Ensuring that an alternative is available for dragging movements that operate on content

The following are common mistakes that are considered failures of this success criterion by the Accessibility Guidelines Working Group.

F108: Failure of Success Criterion 2.5.7 Dragging Movements due to not providing a single pointer method that does not require a dragging movement

, or along with a mainstream user agent, to provide functionality to meet the requirements

of users with disabilities that go beyond those offered by mainstream user agents

Functionality provided by assistive technology includes alternative presentations

(e.g., as synthesized speech or magnified content), alternative input methods (e.g.,

voice), additional navigation or orientation mechanisms, and content transformations

Assistive technologies often communicate data and messages with mainstream user agents

The distinction between mainstream user agents and assistive technologies is not absolute.

Many mainstream user agents provide some features to assist individuals with disabilities.

The basic difference is that mainstream user agents target broad and diverse audiences

that usually include people with and without disabilities. Assistive technologies

target narrowly defined populations of users with specific disabilities. The assistance

provided by an assistive technology is more specific and appropriate to the needs

of its target users. The mainstream user agent may provide important functionality

to assistive technologies like retrieving web content from program objects or parsing

platform event that occurs  when the trigger stimulus of a pointer is depressed

The down-event may have different names on different platforms, such as "touchstart" or "mousedown".

an operation where the pointer engages with an element on the

and the element (or a representation of its position) follows the pointer until an

Examples of draggable elements include list items, text elements, and images.

if removed, would fundamentally change the information or functionality of the content,

information and functionality cannot be achieved in another way that would conform

and outcomes achievable through user action

series of user actions where each action is required in order to complete an activity

Changing the example provided to avoid potential confusion

an input modality that only targets a single point on the page/screen at a time – such as a mouse, single finger on a touch screen, or stylus.

Single pointer interactions include clicks, double clicks, taps, dragging motions, and single-finger swipe gestures. In contrast, multipoint interactions involve the use of two or more pointers at the same time, such as two-finger interactions on a touchscreen, or the simultaneous use of a mouse and stylus.

Changing "touch screen" to "touchscreen" for consistency

platform event that occurs  when the trigger stimulus of a pointer is released

The up-event may have different names on different platforms, such as "touchend" or "mouseup".

any software that retrieves and presents web content for users

---

## Pointer Events API

`https://www.w3schools.com/JS/js_api_pointer_events.asp`

is a modern web standard that provides a unified input model for handling various

pointing devices, such as a mouse, pen/stylus, and touch (finger).

It simplifies development by consolidating separate mouse and touch event models into a single,

interactive interfaces that provide a consistent experience for all users, regardless of hardware.

Fired when a pointer becomes active (button pressed, physical contact).

Fired when a pointer is no longer active (button released, contact ended).

Fired when a pointer changes coordinates.

Fired when a pointer is moved into an element.

Fired when a pointer moves out of an element.

Similar to pointerover, but does not bubble up through the DOM hierarchy.

Similar to pointerout, but does not bubble.

Fired when the system cancels the pointer interaction (interrupted by the OS opening a system menu).

The PointerEvent interface inherits properties from MouseEvent and adds specific ones:

A unique ID for each pointer, allowing tracking in multi-touch scenarios.

A string indicating the device type: "mouse", "pen", or "touch".

A boolean true for the primary pointer (the first finger in a multi-touch).

A normalized value (0 to 1) indicating the pressure applied by the pointer.

Developers can write a single set of event listeners (

reducing code duplication and complexity.

In addition to standard mouse event properties (like client coordinates),

, such as pressure, tiltX, tiltY, width, and height,

allow an element to receive pointer events when the pointer

moves outside its boundaries (useful for sliding or dragging).

CSS property is a separate feature that controls whether

or not an element can be the target of any pointer interactions.

and touch interactions on an HTML element and its descendants.

This CSS property is useful for creating layered interfaces, or temporarily disabling interactions

on certain elements without modifying the underlying JavaScript logic.

Coding fundamentals as a game. Bite-sized lessons and challenges.

If you want to use W3Schools services as an educational institution, team or enterprise, send us an e-mail:

If you want to report an error, or if you want to make a suggestion, send us an e-mail:

W3Schools is optimized for learning and training. Examples might be simplified to improve reading and learning.

Tutorials, references, and examples are constantly reviewed to avoid errors, but we cannot warrant full correctness

of all content. While using W3Schools, you agree to have read and accepted our

---
