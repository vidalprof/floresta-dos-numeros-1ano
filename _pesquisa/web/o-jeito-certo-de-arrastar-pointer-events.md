# 🔎 Pesquisa: o-jeito-certo-de-arrastar-pointer-events

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## Pointer events - Web APIs | MDN

`https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events`

This feature is well established and works across many devices and browser versions. Itâs been available across browsers since July 2020.

* Some parts of this feature may have varying levels of support.

Much of today's web content assumes the user's pointing device will be a mouse. However, since many devices support other types of pointing input devices, such as pen/stylus and touch surfaces, extensions to the existing pointing device event models are needed.

Pointer events are DOM events that are fired for a pointing device. They are designed to create a single DOM event model to handle pointing input devices such as a mouse, pen/stylus or touch (such as one or more fingers).

is a hardware-agnostic device that can target a specific set of screen coordinates. Having a single event model for pointers can simplify creating websites and applications and provide a good user experience regardless of the user's hardware. However, for scenarios when device-specific handling is desired, pointer events defines a

property to inspect the device type which produced the event.

The events needed to handle generic pointer input are analogous to

, etc.). Consequently, pointer event types are intentionally similar to mouse event types.

Additionally, a pointer event contains the usual properties present in mouse events (client coordinates, target element, button states, etc.) in addition to new properties for other forms of input: pressure, contact geometry, tilt, etc. In fact, the

properties, thus facilitating the migration of content from mouse events to pointer events.

property. For example, in the case of a pen, when the pen has physical contact with the digitizer, or at least one button is pressed while hovering.

input device that can produce events. A pointer is considered active if it can still produce further events. For example, a pen that is a down state is considered active because it can produce additional events when the pen is lifted or moved.

A sensing device with a surface that can detect contact. Most commonly, the sensing device is a touch-enabled screen that can sense input from an input device such as a pen, stylus, or finger. Some sensing devices can detect the close proximity of the input device, and the state is expressed as a hover following the mouse.

The process the browser uses to determine a target element for a pointer event. Typically, this is determined by considering the pointer's location and also the visual layout of elements in a document on screen media.

A hardware-agnostic representation of input devices that can target a specific coordinate (or set of coordinates) on a screen. Examples of

input devices are mouse, pen/stylus, and touch contacts.

Pointer capture allows the events for a pointer to be retargeted to a particular element other than the normal hit test result of the pointer's location. See

, which physically prevents the pointer from leaving a region.

plus several event types and associated global event handlers.

The standard also includes some extensions to the

The following sub-sections contain short descriptions of each interface and property.

interface and has the following properties.

Represents the angle between a transducer (a pointer or stylus) axis and the X-Y plane of a device screen.

Represents the angle between the Y-Z plane and the plane containing both the transducer (a pointer or stylus) axis and the Y axis.

A unique identifier for the pointing device generating the

A unique identifier for the pointer causing the event.

The width (magnitude on the X axis), in CSS pixels, of the contact geometry of the pointer.

the height (magnitude on the Y axis), in CSS pixels, of the contact geometry of the pointer.

the normalized pressure of the pointer input in the range of

represent the minimum and maximum pressure the hardware is capable of detecting, respectively.

The normalized tangential pressure of the pointer input (also known as barrel pressure or cylinder stress) in the range

The plane angle (in degrees, in the range of

) between the YâZ plane and the plane containing both the pointer (e.g., pen stylus) axis and the Y axis.

the plane angle (in degrees, in the range of

) between the XâZ plane and the plane containing both the pointer (e.g., pen stylus) axis and the X axis.

The clockwise rotation of the pointer (e.g., pen stylus) around its major axis in degrees, with a value in the range

Indicates the device type that caused the event (mouse, pen, touch, etc.).

Indicates if the pointer represents the primary pointer of this pointer type.

Pointer events have ten event types, seven of which have similar semantics to their mouse event counterparts (

Below is a short description of each event type.

Fired when a pointer is moved into an element's

boundaries of an element or one of its descendants, including as a result of a

event from a device that does not support hover (see

Fired when a pointer changes coordinates. This event is also used if the change in pointer state cannot be reported by other events.

A browser fires this event if it concludes the pointer will no longer be able to generate events (for example, if the related device is deactivated, or the browser decided to interpret the interaction as a pan/zoom instead). For information on how to control this behavior, see

Fired for several reasons including: pointer is moved out of the

boundaries of an element; firing the pointerup event for a device that does not support hover (see

); when a pen stylus leaves the hover range detectable by the digitizer.

boundaries of an element. For pen devices, this event is fired when the stylus leaves the hover range detectable by the digitizer.

Fired when a pointer changes any properties that don't fire

Fired when an element receives pointer capture.

Fired after pointer capture is released for a pointer.

Indicates whether the element on which it is invoked has pointer capture for the pointer identified by the given pointer ID.

that was previously set for a specific pointer event.

property is used to determine the maximum number of simultaneous touch points that are supported at any single point in time.

This section contains examples of basic usage of using the pointer events interfaces.

This example registers a handler for every event type for the given element.

const el = document.getElementById("target");

el.onpointerrawupdate = rawUpdateHandler;

el.ongotpointercapture = gotCaptureHandler;

el.onlostpointercapture = lostCaptureHandler;

This example illustrates accessing all of a pointer event's properties.

// Process this event based on the event's identifier

// Calculate the touch point's contact area

// Compare cached id with this event's id and process accordingly

// Call the appropriate pointer type handler

console.log(`pointerType ${ev.pointerType} is not supported`);

if (ev.tiltX !== 0 && ev.tiltY !== 0) processTilt(ev.tiltX, ev.tiltY);

// If this event is not primary, call the non primary handler

if (!ev.isPrimary) processNonPrimary(ev);

const el = document.getElementById("target");

In some scenarios there may be multiple pointers (for example a device with both a touchscreen and a mouse), or a pointer that supports multiple contact points (for example a touchscreen that supports multiple finger touches). The application can use the

property to identify a master pointer among the set of

for each pointer type. If an application only wants to support a primary pointer, it can ignore all pointer events that are not primary.

A mouse has only one pointer, so it will always be the primary pointer. For touch input, a pointer is considered primary if the user touched the screen when there were no other active touches. For pen and stylus input, a pointer is considered primary if the user's pen initially contacted the screen when there were no other active pens contacting the screen.

Some pointer devices (such as mouse and pen) support multiple buttons, and the button presses can be

(i.e., pressing an additional button while another button on the pointer device is already pressed).

To determine the state of button presses, pointer events uses the

The following table provides the values of

Neither buttons nor touch/pen contact changed since last event

Mouse move with no buttons pressed, Pen moved while hovering with no buttons pressed

property indicates a change in the state of the button. However, as in the case of touch, when multiple events occur with one event, all of them have the same value.

Pointer capture allows events for a particular

to be re-targeted to a particular element instead of the normal

at a pointer's location. This can be used to ensure that an element continues to receive pointer events even if the pointer device's contact moves off the element (for example by scrolling or panning).

Pointer capture will cause the target to capture all subsequent pointer events as if they were occurring over the capturing target. Accordingly,

event triggers. The capture can be released manually by calling

on the target element, or it will be implicitly released after a

If you need to move an element in the DOM, then make sure to call

will not lose track of it. E.g., if you need to use

to move an element somewhere else, then make sure to call

The following example shows pointer capture being set on an element.

const el = document.getElementById("target");

// Element 'target' will receive/capture further events

const el = document.getElementById("target");

The following example shows a pointer capture being released (when a

event occurs. The browser does this automatically when a

const el = document.getElementById("target");

// Element "target" will receive/capture further events

const el = document.getElementById("target");

const el = document.getElementById("target");

// Register pointerdown and pointercancel handlers

CSS property is used to specify whether or not the browser should apply its default (

) touch behavior (such as zooming or panning) to a region. This property may be applied to all elements except: non-replaced inline elements, table rows, row groups, table columns, and column groups.

means the browser is free to apply its default touch behavior (to the specified region) and the value of

disables the browser's default touch behavior for the region. The values

, mean that touches that begin on the specified region are only for horizontal and vertical scrolling, respectively. The value

means the browser may consider touches that begin on the element are only for scrolling and zooming.

In the following example, default touch behavior is disabled for some

element is touched, it will only pan in the horizontal direction.

Although the pointer event interfaces enable applications to create enhanced user experiences on pointer enabled devices, the reality is the vast majority of today's web content is designed to only work with mouse input. Consequently, even if a browser supports pointer events, the browser must still process mouse events so content that assumes mouse-only input will work as is without direct modification. Ideally, a pointer enabled application does not need to explicitly handle mouse input. However, because the browser must process mouse events, there may be some compatibility issues that need to be handled. This section contains information about pointer event and mouse event interaction and the ramifications for application developers.

may map generic pointer input to mouse events for compatibility with mouse-based content

. Authors can prevent the production of certain compatibility mouse events by canceling the pointerdown event but note that:

Mouse events can only be prevented when the pointer is down.

Hovering pointers (e.g., a mouse with no buttons pressed) cannot have their mouse events prevented.

events are never prevented (even if the pointer is down).

Minimize the amount of work performed in event handlers.

Add the event handlers to a specific target element (rather than the entire document or nodes higher up in the document tree).

The target element (node) should be large enough to accommodate the largest contact surface area (typically a finger touch). If the target area is too small, touching it could result in firing other events for adjacent elements.

Some additional values have been defined for the CSS

specification, but currently those values have limited implementation support.

---

## Element: setPointerCapture() method - Web APIs | MDN

`https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture`

Element: setPointerCapture() method - Web APIs | MDN

This feature is well established and works across many devices and browser versions. Itâs been available across browsers since July 2020.

interface is used to designate a specific element as the

of future pointer events. Subsequent events for the pointer will

be targeted at the capture element until capture is released (via

for an overview and examples of how pointer capture works.

it. This lets you slide the element horizontally, even when your pointer moves outside of

const slider = document.getElementById("slider");

slider.releasePointerCapture(e.pointerId);

slider.style.transform = `translate(${e.clientX - 70}px)`;

---

## Touch and mouse  |  Articles  |  web.dev

`https://web.dev/articles/mobile-touchandmouse`

Save and categorize content based on your preferences.

For close to thirty years, desktop computing experiences have centered around a keyboard and a mouse or trackpad as our main user input devices. Over the last decade, however, smartphones and tablets have brought a new interaction paradigm: touch. With the introduction of touch-enabled Windows 8 machines, and now with the release of the awesome touch-enabled Chromebook Pixel, touch is now becoming part of the expected desktop experience. One of the biggest challenges is building experiences that work not only on touch devices and mouse devices, but also on these devices where the user will use both input methods - sometimes simultaneously!

This article will help you understand how touch capabilities are built into the browser, how you can integrate this new interface mechanism into your existing apps and how touch can play nicely with mouse input.

The iPhone was the first popular platform to have dedicated touch APIs built in to the web browser.  Several other browser vendors have created similar API interfaces built to be compatible with the iOS implementation, which is now described by the

. Touch events are supported by Chrome and Firefox on desktop, and by Safari on iOS and Chrome and the Android browser on Android, as well as other mobile browsers like the Blackberry browser.

that is still a good way to get started if you haven’t looked at Touch events before.  In fact, if you haven’t worked with touch events before, go read that article now, before you continue.  Go on, I’ll wait.

All done?  Now that you have a basic grounding in touch events, the challenge with writing touch-enabled interactions is that the touch interactions can be quite a bit different from mouse (and mouse-emulating trackpad and trackball) events - and although touch interfaces typically try to emulate mice, that emulation isn’t perfect or complete; you really need to work through both interaction styles, and may have to support each interface independently.

Most Importantly: The User May Have Touch And a Mouse

Many developers have built sites that statically detect whether an environment supports touch events, and then make the assumption that they only need to support touch (and not mouse) events.  This is now a faulty assumption - instead, just because touch events are present does not mean the user is primarily using that touch input device.  Devices such as the Chromebook Pixel and some Windows 8 laptops now support BOTH Mouse and Touch input methods, and more will in the near future.  On these devices, it is quite natural for users to use both the mouse and the touch screen to interact with applications, so  "supports touch" is not the same as "doesn’t need mouse support."  You can’t think of the problem as "I have to write two different interaction styles and switch between them," you need to think through how both interactions will work together as well as independently.  On my Chromebook Pixel, I frequently use the trackpad, but I also reach up and touch the screen - on the same application or page, I do whatever feels most natural at the moment.  On the other hand, some touchscreen laptop users will rarely if ever use the touchscreen at all - so the presence of touch input shouldn’t disable or hinder mouse control.

Unfortunately, it can be hard to know if a user’s browser environment supports touch input or not; ideally, a browser on a desktop machine would always indicate support for touch events so a touchscreen display could be attached at any time (e.g. if a touchscreen attached through a

becomes available).  For all these reasons, your applications shouldn’t attempt to switch between touch and mouse - just support both!

#1 - Clicking and Tapping - the "Natural" Order of Things

The first problem is that touch interfaces typically try to emulate mouse clicks - obviously, since touch interfaces need to work on applications that have only interacted with mouse events before!  You can use this as a shortcut - because "click" events will continue to be fired, whether the user clicked with a mouse or tapped their finger on the screen.  However, there are a couple of problems with this shortcut.

First, you have to be careful when designing more advanced touch interactions: when the user uses a mouse it will respond via a click event, but when the user touches the screen both touch and click events will occur.  For a single click the order of events is:

This, of course, means that if you are processing touch events like touchstart, you need to make sure that you don’t process the corresponding mousedown and/or click event as well.  If you can cancel the touch events (call preventDefault() inside the event handler), then no mouse events will get generated for touch.  One of the most important rules of touch handlers is:

However, this also prevents other default browser behavior (like scrolling) - although usually you’re handling the touch event entirely in your handler, and you will WANT to disable the default actions.  In general, you’ll either want to handle and cancel all touch events, or avoid having a handler for that event.

Secondly, when a user taps on an element in a web page on a mobile device, pages that haven’t been designed for mobile interaction have a delay of at least 300 milliseconds between the touchstart event and the processing of mouse events (mousedown). It could be done using Chrome, you can turn on

in Chrome Developer Tools to help you test touch interfaces on a non-touch system!

This delay is to allow the browser time to determine if the user is performing another gesture - in particular, double-tap zooming.  Obviously, this can be problematic in cases where you want to have instantaneous response to a finger touch.  There is

to try to limit the scenarios in which this delay occurs automatically.

The first and easiest way to avoid this delay is to "tell" the mobile browser that your page is not going to need zooming - which can be done using a fixed viewport, e.g. by inserting into your page:

<meta name="viewport" content="width=device-width,user-scalable=no">

This isn’t always appropriate, of course - this disables pinch-zooming, which may be required for accessibility reasons, so use it sparingly if at all (if you do disable user scaling, you may want to provide some other way to increase text readability in your application).  Also, for Chrome on desktop class devices that support touch, and other browsers on mobile platforms when the page has viewports that are not scalable,

#2: Mousemove Events Aren’t Fired by Touch

It’s important to note at this point that the emulation of mouse events in a touch interface does not typically extend to emulating mousemove events - so if you build a beautiful mouse-driven control that uses mousemove events, it probably won’t work with a touch device unless you specifically add touchmove handlers too.

Browsers typically automatically implement the appropriate interaction for touch interactions on the HTML controls - so, for example, HTML5 Range controls will just work when you use touch interactions.  However, if you’ve implemented your own controls, they will likely not work on click-and-drag type interactions; in fact, some commonly used libraries (like jQueryUI) do not yet natively support touch interactions in this way (although for jQueryUI, there are several monkey-patch fixes to this issue).  This was one of the first problems I ran into when upgrading my  Web Audio Playground application to work with touch - the sliders were jQueryUI-based, so they did not work with click-and-drag interactions.  I changed over to HTML5 Range controls, and they worked.  Alternately, of course, I could have simply added touchmove handlers to update the sliders, but there’s one problem with that…

#3: Touchmove and MouseMove Aren’t the Same Thing

A pitfall I've seen a few developers fall into is having touchmove and mousemove handlers call into the same codepaths.  The behavior of these events is very close, but subtly different - in particular,

touch events always target the element where that touch STARTED, while mouse events target the element currently under the mouse cursor.

This is why we have mouseover and mouseout events, but there are no corresponding touchover and touchout events - only touchend.

The most common way this can bite you is if you happen to remove (or relocate) the element that the user started touching. For example, imagine an image carousel with a touch handler on the entire carousel to support custom scrolling behavior. As available images change, you remove some

elements and add others. If the user happens to start touching on one of those images and then you remove it, your handler (which is on an ancestor of the img element) will just stop receiving touch events (because they’re being dispatched to a target that’s no longer in the tree) - it'll look like the user is holding their finger in one place even though they may have moved and eventually removed it.

You can of course avoid this problem by avoiding removing elements that have (or have ancestors that have) touch handlers while a touch is active. Alternately, the best guidance is rather than register static touchend/touchmove handlers, wait until you get a touchstart event and then add touchmove/touchend/touchcancel handlers to the

of the touchstart event (and remove them on end/cancel). This way you'll continue to receive events for the touch even if the target element is moved/removed. You can play with this a little

- touch the red box and while holding hit escape to remove it from the DOM.

The mouse pointer metaphor separated cursor position from actively selecting, and this allowed developers to use hover states to hide and show information that might be pertinent to the users.  However, most touch interfaces right now do not detect a finger "hovering" over a target - so providing semantically important information (e.g. providing "what is this control?" popup) based on hovering is a no-no, unless you also give a touch-friendly way to access this information.  You need to be careful about how you use hovering to relay information to users.

Interestingly enough, though, the CSS :hover pseudoclass CAN be triggered by touch interfaces in some cases - tapping an element makes it :active while the finger is down, and it also acquires the :hover state.  (With Internet Explorer, the :hover is only in effect while the user’s finger is down - other browsers keep the :hover in effect until the next tap or mouse move.) This is a good approach to making pop-out menus work on touch interfaces - a side effect of making an element active is that the :hover state is also applied.  For example:

<div class="content">This is an awesome picture of me</div>

Once another element is tapped the element is no longer active, and the hover state disappears, just as if the user was using a mouse pointer and moved it off the element.  You may wish to wrap the content in an

element in order to make it a tabstop as well - that way the user can toggle the extra information on a mouse hover or click, a touch tap, or a keypress, with no JavaScript required.  I was pleasantly surprised as I began work to make my

to work well with touch interfaces that my pop-out menus already worked well on touch, because I’d used this kind of structure!

The above method works well for mouse pointer based interfaces, as well as for touch interfaces. This is in contrast to using "title" attributes on hover, which will NOT show up when the element is activated:

<img src="/awesome.png" title="this doesn't show up in touch">

While mice have a conceptual disassociation from reality, it turns out that they are extremely accurate, as the underlying operating system generally tracks exact pixel precision for the cursor.  Mobile developers on the other hand have learned that finger touches on a touch screen are not as accurate, mostly because of the size of the surface area of the finger when in contact with the screen (and partly because your fingers obstruct the screen).

Many individuals and companies have done extensive user research on how to design applications and sites that are accommodating of finger based interaction, and many books have been written on the topic.  The basic advice is to increase the size of the touch targets by increasing the padding, and reduce the likelihood of incorrect taps by increasing the margin between elements.  (Margins are not included in the hit detection handling of touch and click events, while padding is.)  One of the primary fixes I had to make to the Web Audio Playground was to increase the sizes of the connection points so they were more easily touched accurately.

Many browser vendors who are handling touch based interfaces have also introduced logic into the browser to help target the correct element when a user touches the screen and reduce the likelihood of incorrect clicks - although this usually only corrects click events, not moves (although Internet Explorer appears to modify mousedown/mousemove/mouseup events as well).

#6: Keep Touch Handlers Contained, or They’ll Jank Your Scroll

It’s also important to keep touch handlers confined only to the elements where you need them; touch elements can be very high-bandwidth, so it’s important to avoid touch handlers on scrolling elements (as your processing may interfere with browser optimizations for fast jank-free touch scrolling - modern browsers try to scroll on a GPU thread, but this is impossible if they have to check with javascript first to see if each touch event is going to be handled by the app).  You can check out

One piece of guidance to follow to avoid this problem is to make sure that if you are only handling touch events in a small portion of your UI, you only attach touch handlers there (not, e.g., on the

of the page); in short, limit the scope of your touch handlers as much as possible.

The final interesting challenge is that although we’ve been referring to it as "Touch" user interface, nearly universally the support is actually for Multi-touch - that is, the APIs provide more than one touch input at a time.  As you begin to support touch in your applications, you should consider how multiple touches might affect your application.

If you have been building apps primarily driven by mouse, then you are used to building with at most one cursor point - systems don’t typically support multiple mice cursors.  For many applications, you will be just mapping touch events to a single cursor interface, but most of the hardware that we have seen for desktop touch input can handle at least 2 simultaneous inputs, and most new hardware appears to support at least 5 simultaneous inputs.  For developing an

, of course, you would want to be able to support multiple simultaneous touch inputs.

The currently implemented W3C Touch APIs have no API to determine how many touch points the hardware supports, so you’ll have to use your best estimation for how many touch points your users will want - or, of course, pay attention to how many touch points you see in practice and adapt.  For example, in a piano application, if you never see more than two touch points you may want to add some "chords" UI.  The PointerEvents API  does have an API to determine the capabilities of the device.

Hopefully this article has given you some guidance on common challenges in implementing touch alongside mouse interactions.  More important than any other advice, of course, is that you need to test your app on mobile, tablet, and combined mouse-and-touch desktop environments.  If you don’t have touch+mouse hardware, use Chrome’s "

" to help you test the different scenarios.

It’s not only possible, but relatively easy following these pieces of guidance, to build engaging interactive experiences that work well with touch input, mouse input, and even both styles of interaction at the same time.

Except as otherwise noted, the content of this page is licensed under the

, and code samples are licensed under the

. Java is a registered trademark of Oracle and/or its affiliates.

---

## touch-action CSS property - CSS | MDN

`https://developer.mozilla.org/en-US/docs/Web/CSS/touch-action`

This feature is well established and works across many devices and browser versions. Itâs been available across browsers since September 2019.

* Some parts of this feature may have varying levels of support.

property sets how an element's region can be manipulated by a touchscreen user (for example, by zooming features built into the browser).

By default, panning (scrolling) and pinching gestures are handled exclusively by the browser. An application using

event when the browser starts handling a touch gesture. By explicitly specifying which gestures should be handled by the browser, an application can supply its own behavior in

listeners for the remaining gestures. Applications using

disable the browser handling of gestures by calling

to ensure the browser knows the intent of the application before any event listeners have been invoked.

When a gesture is started, the browser intersects the

values of the touched element and its ancestors, up to the one that implements the gesture (in other words, the first containing scrolling element). This means that in practice,

is typically applied only to top-level elements which have some custom behavior, without needing to specify

explicitly on any of that element's descendants.

will not have any impact on the behavior of the current gesture.

Enable browser handling of all panning and zooming gestures.

Disable browser handling of all panning and zooming gestures.

Enable single-finger horizontal panning gestures. May be combined with

Enable single-finger vertical panning gestures. May be combined with

Enable panning and pinch zoom gestures, but disable additional non-standard gestures such as double-tap to zoom. Disabling double-tap to zoom removes the need for browsers to delay the generation of

events when the user taps the screen. This is an alias for "

" (which, for compatibility, is itself still valid).

Enable single-finger gestures that begin by scrolling in the given direction(s). Once scrolling has started, the direction may still be reversed. Note that scrolling "up" (

) means that the user is dragging their finger downward on the screen surface, and likewise

means the user is dragging their finger to the right. Multiple directions may be combined except when there is a simpler representation (for example,

Enable multi-finger panning and zooming of the page. This may be combined with any of the

may inhibit operating a browser's zooming capabilities. This will prevent people experiencing low vision conditions from being able to read and understand page content.

MDN Understanding WCAG, Guideline 1.4 explanations

Understanding Success Criterion 1.4.4 | Understanding WCAG 2.0

all elements except: non-replaced inline elements, table rows, row groups, table columns, and column groups

The most common usage is to disable all gestures on an element (and its non-scrollable descendants) that provides its own dragging and zooming behavior â such as a map or game surface.

background: linear-gradient(blue, green);

---
