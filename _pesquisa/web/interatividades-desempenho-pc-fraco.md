# 🔎 Pesquisa: interatividades-desempenho-pc-fraco

> Busca: `HTML5 game performance low-end school computer Chromebook canvas requestAnimationFrame DOM reflow images memory single page optimization`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## Inside HTML5 Canvas: Rendering 60 FPS Browser Games — Arcade Hub Blog

`https://arcadehubplay.com/blog/html5-canvas-rendering-performance`

Inside HTML5 Canvas: Rendering 60 FPS Browser Games — Arcade Hub Blog

Inside HTML5 Canvas: How Web Browsers Render 60 FPS Action Games

Published on June 11, 2026 by Arcade Hub Engineering

For years, creating high-performance interactive games required compiled native applications. Today, the modern web browser is a powerful game console. Using the

and optimized JavaScript engines, developers can run arcade games at a fluid 60 frames per second (FPS)—and up to 120 FPS on high-refresh-rate gaming monitors—directly in the browser, without plugins.

However, achieving this performance requires understanding how browsers manage graphic rendering. In this deep dive, we will examine the internal graphics pipelines of browsers, analyze the performance differences between scheduling APIs, and explore rendering strategies that prevent lag and stutter.

"Developing browser games is an exercise in resource constraint. You are running code in a single-threaded sandbox, competing with the browser's own UI rendering."

1. The Game Loop: requestAnimationFrame vs. SetInterval

The core of any game is the **Game Loop**—a repeating cycle that processes player inputs, updates game coordinates, and draws the screen. Historically, developers scheduled loops using `setInterval(loop, 16.6)` or `setTimeout`. This is a major anti-pattern for modern rendering.

Timer functions run on the browser's main JavaScript event thread, which is subject to garbage collection pauses and page layout blocks. If a timer is scheduled for 16.6ms but the thread is busy, the loop triggers late, causing dropped frames (stutter). Furthermore, timers do not sync with the monitor's vertical refresh rate (VSync), leading to screen tearing.

. This API tells the browser that you want to perform an animation. The browser schedules your callback function to execute exactly before the next screen redraw. This yields major performance gains:

redrawing is synchronized with the monitor's refresh rate (typically 60Hz, 90Hz, or 120Hz), eliminating screen tearing.

if the user switches browser tabs, the browser pauses requestAnimationFrame loops automatically, reducing CPU/GPU overhead and saving battery.

browser layout systems can optimize and batch canvas draws for smoother rendering.

2. Handling Time: Delta Time and Frame Independence

Monitors run at different refresh rates. If your game loop moves a character by 5 pixels every frame, a player with a 60Hz screen will move the character at 300 pixels per second. A player with a 140Hz screen will move at 700 pixels per second, making the game run twice as fast!

To solve this, games use **Delta Time (dt)**—the elapsed time between the current frame and the previous frame. Instead of moving characters by a fixed pixel step per frame, we define speeds in units per millisecond or second, and multiply by delta time:

This ensures that character movement speeds remain consistent regardless of whether the game is running at 30 FPS, 60 FPS, or 120 FPS.

3. Browser Graphics Pipelines: Canvas 2D vs. WebGL

When you draw on an HTML5 Canvas using a 2D rendering context (`canvas.getContext('2d')`), the browser executes commands using its standard graphics libraries (like Skia in Chrome/Firefox or CoreGraphics in Safari). While Skia utilizes hardware acceleration (GPU) for basic operations like fills and strokes, it still has overhead when translating JavaScript draw commands into GPU commands.

For highly complex games with thousands of particles, WebGL is preferred. WebGL maps directly to OpenGL ES/Vulkan shaders, bypassing the browser's standard rendering pipeline. This allows developers to submit vertex arrays directly to GPU memory, enabling complex shaders and massive rendering capability that would bottleneck a 2D canvas context.

To run smooth browser games, use `requestAnimationFrame` for scheduling, implement delta-time calculations for frame independence, and keep garbage collection to a minimum by reusing objects (object pooling). By respect-coding the browser's event loop and rendering cycle, your HTML5 Canvas games can run with native arcade-like speed on any device.

---

## Improving HTML5 Canvas performance  |  Articles  |  web.dev

`https://web.dev/articles/canvas-performance`

Improving HTML5 Canvas performance  |  Articles  |  web.dev

Save and categorize content based on your preferences.

HTML5 canvas, which started as an experiment from Apple, is the most

the web.  Many developers now rely on it for a wide variety of

multimedia projects, visualizations, and games. However, as the

applications we build increase in complexity, developers inadvertently

There’s a lot of disconnected wisdom about optimizing canvas

performance. This article aims to consolidate some of this body into a

more readily digestible resource for developers. This article includes

fundamental optimizations that apply to all computer graphics

environments as well as canvas-specific techniques that are subject to

change as canvas implementations improve. In particular, as browser

vendors implement canvas GPU acceleration, some of the outlined

performance techniques discussed will likely become less impactful. This

Note that this article does not go into usage of HTML5 canvas. For that,

To address the quickly changing world of HTML5 canvas,

) tests verify that every proposed optimization

still works.  JSPerf is a web application that allows developers to

write JavaScript performance tests. Each test focuses on a result that

you’re trying to achieve (for example, clearing the canvas), and

includes multiple approaches that achieve the same result. JSPerf runs

each approach as many times as possible over a short time period and

gives a statistically meaningful number of iterations per second. Higher

Visitors to a JSPerf performance test page can run the test on their

browser, and let JSPerf store the normalized test results on

techniques in this article are backed up by a JSPerf result, you can

return to see up-to-date information about whether or not the technique

renders these results as graphs, embedded throughout this article.

All of the performance results in this article are keyed on the

browser version. This turns out to be a limitation, since we don't know what OS

the browser was running on, or even more importantly, whether or not HTML5

canvas was hardware accelerated when the performance test ran. You can find out

if Chrome's HTML5 canvas is hardware accelerated by visiting

If you’re re-drawing similar primitives to the screen across multiple

frames, as is often the case when writing a game, you can make large

performance gains by pre-rendering large parts of the scene.

Pre-rendering means using a separate off-screen canvas (or canvases) on

which to render temporary images, and then rendering the off-screen

For example, suppose you’re redrawing Mario running at 60 frames a

second. You could either redraw his hat, moustache, and “M” at each

frame, or pre-render Mario before running the animation.

This technique is especially effective when the rendering operation

in the above example) is expensive. A good example of this is

text rendering, which is a very expensive operation.

“pre-rendered loose” test case. When pre-rendering, it’s important to

make sure that your temporary canvas fits snugly around the image you

are drawing, otherwise the performance gain of off-screen rendering is

counterweighted by the performance loss of copying one large canvas onto

another (which varies as a function of source target size). A snug

canvas in the above test is simply smaller:

Compared to the loose one that yields poorer performance:

Since drawing is an expensive operation, it’s more efficient to load the

drawing state machine with a long set of commands, and then have it dump

For example, when drawing multiple lines, it's more efficient to create one

path with all the lines in it and draw it with a single draw call. In other

words, rather than drawing separate lines:

We get better performance from drawing a single polyline:

This applies to the world of HTML5 canvas as well. When drawing a

complex path, for example, it’s better to put all of the points into the

path, rather than rendering the segments separately (

Note, however, that with Canvas, there’s an important exception to this

rule: if the primitives involved in drawing the desired object have

small bounding boxes (for example, horizontal and vertical lines), it

may actually be more efficient to render them separately

The HTML5 canvas element is implemented on top of a state machine that

tracks things like fill and stroke styles, as well as previous points

that make up the current path. When trying to optimize graphics

performance, it’s tempting to focus solely on the graphics rendering.

However, manipulating the state machine can also incur a performance

If you use multiple fill colors to render a scene, for example, it’s

cheaper to render by color rather than by placement on the canvas. To

render a pinstripe pattern, you could render a stripe, change colors,

Or render all odd stripes and then all even stripes:

As expected, the interlaced approach is slower because changing the

Render screen differences only, not the whole new state

As one would expect, rendering less on the screen is cheaper than

rendering more. If you have only incremental differences between

redraws, you can get a significant performance boost by just drawing the

difference. In other words, rather than clearing the whole screen before

Keep track of the drawn bounding box, and only clear that.

If you are familiar with computer graphics, you might also know this

technique as “redraw regions”, where the previously rendered bounding

box is saved, and then cleared on each rendering.

This technique also applies to pixel-based rendering contexts, as is

Use multiple layered canvases for complex scenes

As mentioned before, drawing large images is expensive and should be

avoided if possible. In addition to using another canvas for rendering

off screen, as illustrated in the pre-rendering section, we can also use

canvases layered on top of one another. By using transparency in the

foreground canvas, we can rely on the GPU to composite the alphas

together at render time. You might set this up as follows, with two

absolutely positioned canvases one on top of the other.

<canvas id="bg" width="640" height="480" style="position: absolute; z-index: 0">

<canvas id="fg" width="640" height="480" style="position: absolute; z-index: 1">

The advantage over having just one canvas here, is that when we draw or

clear the foreground canvas, we don’t ever modify the background. If

your game or multimedia app can be split up into a foreground and

background, consider rendering these on separate canvases to get a

You can often take advantage of imperfect human perception and render

the background just once or at a slower speed compared to the foreground

(which is likely to occupy most of your user’s attention). For example,

you can render the foreground every time you render, but render the

Also note that this approach generalizes well for any number of

composite canvases if your application works better with a this sort of

Like many other graphics environments, HTML5 canvas allows developers to

blur primitives, but this operation can be very expensive:

the scene needs to be redrawn explicitly at each frame. Because of this,

clearing the canvas is a fundamentally important operation for HTML5

clearing the entire canvas is often undesirable, but if you

or using a canvas-specific hack to do it:

reset version, but in some cases using the

Be careful with this tip, since it depends heavily on the underlying

canvas implementation and is very much subject to change. For more

Simon Sarris' article on clearing the canvas

HTML5 canvas supports sub-pixel rendering, and there’s no way to turn it

off. If you draw with coordinates that are not integers, it

automatically uses anti-aliasing to try to to smooth out the lines.

this sub-pixel canvas performance article by Seb Lee-Delisle

If the smoothed sprite is not the effect you seek, it can be much faster

to convert your coordinates to integers using

To convert your floating point coordinates to integers, you can use

several clever techniques, the most performant of which involve adding

one half to the target number, and then performing bitwise operations on

the result to eliminate the fractional part.

Note that this sort of optimization should no longer matter once canvas

implementations are GPU accelerated which will be able to quickly

implementing interactive applications in the browser. Rather than

command the browser to render at a particular fixed tick rate, you

politely ask the browser to call your rendering routine and get called

when the browser is available. As a nice side effect, if the page is not

in the foreground, the browser is smart enough not to render.

callback aims for a 60 FPS callback rate but

doesn’t guarantee it, so you need to keep track of how much time passed

since the last render. This can look something like the following:

other rendering technologies such as WebGL.

At the time of writing, this API is only available in Chrome, Safari and

Most mobile canvas implementations are slow

Unfortunately at the time of writing, only iOS

5.0 beta running Safari 5.1 has GPU accelerated mobile canvas

implementation. Without GPU acceleration, mobile browsers don’t

generally have powerful enough CPUs for modern canvas-based

A number of the JSPerf tests described above perform an

order of magnitude worse on mobile compared to desktop, greatly

restricting the kinds of cross-device apps you can expect to

To recap, this article covered a comprehensive set of useful

optimization techniques that will help you develop performant HTML5

canvas-based projects. Now that you’ve learned something new here, go

forth and optimize your awesome creations. Or, if you don’t currently

have a game or application to optimize, check out

lets developers create JS performance tests.

which includes chapters on Canvas performance.

Except as otherwise noted, the content of this page is licensed under the

, and code samples are licensed under the

. Java is a registered trademark of Oracle and/or its affiliates.

---

## Building a High-Performance HTML5 Canvas Engine with Clean TypeScript | cliexit

`https://cliexit.com/blog/mini-html5-game-canvas/`

Building a High-Performance HTML5 Canvas Engine with Clean TypeScript | cliexit

The retro arcade stuttered every four seconds in Chrome until we profiled allocations:

objects sixty times per second. GC pauses hit 2–4 ms — invisible in a backend trace, fatal at 60 FPS. That hitch is why this lab exists.

Every backend engineer needs a frontend sandbox to burn off cognitive steam. We spent the weekend building a lightweight, zero-dependency HTML5 Canvas engine using pure TypeScript. No React overhead, no heavy web frameworks—just raw pixels driven by strict architectural typing.

The heartbeat of any interactive software matrix is the game loop. If you tie game physics directly to the browser update frames without decoupling, game speed will vary wildly based on the user’s monitor refresh rate (60Hz vs 144Hz).

// Decoupling Physics Updates from Frame Render States

In javascript-based engines, creating new coordinate vector objects inside the

cycle (which runs 60+ times per second) is an anti-pattern. It triggers the browser’s

to execute a “Stop-The-World” operation to clean up dead memory heap nodes, causing microscopic frame stutters.

. All bullet and particle nodes are instantiated once during the system boot sequence and recycled throughout the execution lifecycle.

for canvas micro-games running the same loop principles.

ships three micro-games on one bundle. Profiling in Chrome DevTools (Performance tab, 6× CPU throttle) on a 2023 MacBook Pro:

is present — if max delta exceeds 32 ms twice in a row, the loop drops a frame counter into the HUD. That is how we caught a regression where UI DOM updates ran inside

Canvas games break when CSS scales the element but internal width/height stays at 300×150 defaults. Our pattern:

Touch targets get a minimum 44 px hit slab even when the sprite is smaller — mobile Safari does not forgive 24 px buttons.

We bundle with Astro’s default pipeline — one entry script, no React reconciler on the hot path. TypeScript enforces entity IDs; the entity map is a

recycled from a free list. If you need UI chrome, keep it in HTML overlay divs, not inside the canvas draw loop.

on cliexit: one bundled script, strict typing, measurable frame times, and zero server runtime. If your browser tab stutters, profile allocation first—do not blame the canvas API.

---

## HTML5 Canvas Performance and Optimization Tips, Tricks and Coding Best Practices · GitHub

`https://gist.github.com/jaredwilli/5469626`

HTML5 Canvas Performance and Optimization Tips, Tricks and Coding Best Practices · GitHub

You signed in with another tab or window.

You switched accounts on another tab or window.

Instantly share code, notes, and snippets.

Clone this repository at &lt;script src=&quot;https://gist.github.com/jaredwilli/5469626.js&quot;&gt;&lt;/script&gt;

Save jaredwilli/5469626 to your computer and use it in GitHub Desktop.

Clone this repository at &lt;script src=&quot;https://gist.github.com/jaredwilli/5469626.js&quot;&gt;&lt;/script&gt;

Save jaredwilli/5469626 to your computer and use it in GitHub Desktop.

HTML5 Canvas Performance and Optimization Tips, Tricks and Coding Best Practices

HTML5 canvas Performance and Optimization Tips, Tricks and Coding Best Practices

With canvas being still very new to internet, and no signs of it ever getting old that I can see in the future, there are not too many documented best practices or other really important tips that are a must know for developing with it in any one particular place. Things like this are scattered around and many times on lesser known sites.

There's so many things that people need to know about, and still so much to learn about, so I wanted to share some things to help people who are learning canvas and maybe some who already know it quite well and am hoping to get some feedback from others about what they feel are some best practices or other tips and tricks for working with canvas in HTML5.

I want to start off with one I personally found to be quite a useful yet surprisingly uncommon thing for developers to do.

Just as you would any other time, in any other language whatever the case may be. It has been a best practice for everything else, and I have come to find that in a complex canvas app, things can get a little confusing when dealing with several different contexts and saved/restore states. Not to mention the code is just more readable and overall cleaner looking too.

The if statement not easier and cleaner to read and know what is what immediately going on than the else statement in this, is it not? I think this should be a method that developers should continue to practice just as they would when writing plain 'ol javascript or any other language even.

Use requestAnimationFrame instead of setInterval / setTimeout

setInterval and setTimeout were never intended to be used as animation timers, they're just generic methods for calling functions after a time delay. If you set an interval for 20ms in the future, but your queue of functions takes longer than that to execute, your timer won't fire until after these functions have completed. That could be a while, which isn't ideal where animation is concerned. RequestAnimationFrame is a method which tells the browser that an animation is taking place, so it can optimize repaints accordingly. It also throttles the animation for inactive tabs, so it won't kill your mobile device's battery if you leave it open in the background.

Nicholas Zakas wrote a hugely detailed and informative article about requestAnimationFrame on his blog which is well worth reading. If you want some hard and fast implementation instructions, then Paul Irish has written a requestAnimationFrame shim which I've used in every one of the canvas apps I have made just about.

Even better than using requestAnimationFrame in place of setTimeout and setInterval, Joe Lambert has written a new and improved shim called requestInterval and requestTimeout, which he explains what issues exist when using requestAnimFrame. You can view the gist of the script here.

Now that all the browsers have caught up on the spec for this, there has been an update to the requestAnimFrame polyfill, one which will probably remain the one to use to cover all vendors.

This is a technique for animation-heavy games which @nicolahibbert wrote about in a post of hers on optimizing canvas games. She explains how it may be better to use multiple canvases layered on top of one another rather than do everything in a single canvas.

"Drawing too many pixels to the same canvas at the same time will cause your frame rate to fall through the floor. Take Breakout for example. Trying to draw the bricks, the ball, the paddle, any power-ups or weapons, and then each star in the background – this simply won't work, it takes too long to execute each of these instructions in turn. By splitting the starfield and the rest of the game onto separate canvases, you are able to ensure a decent framerate." Nicola says.

I have had to do this for a few canvas apps I've made including Samsung's Olympic Genome Project facebook app. It's an extremely useful thing to know and to make use of whether it's needed or not. It decreases load time immensely, plus it can be a really useful technique to load images off screen since they can sometimes take a while.

var tmpCanvas = document.createElement('canvas'),

tmpCtx.drawImage(thumbImg, 0, 0, 200, 200);

Notice that the src of the image is set after it is loaded. This is a key thing to remember to do too. Once the images are done loading and drawn into these temp canvases, you can then draw them to your main canvas by using the same ctx.drawImage(), but instead of putting the image as the first argument, you use tmpCtx.canvas to reference the temporary canvas.

requestAnimFrame to Optimize Dragging Events

The 2d Context has a back reference to it's associated DOM element that you can use for quick referencing of the context which is HTMLCanvasElemen.

var ctx = doc.getElementById('canvas').getContext('2d');

console.log(ctx.canvas);    //=> HTMLCanvasElement

I would like to get more information on this and other shortcut references that may exist in canvas as well, but this is one that is pretty straightforward I think.

One of the best canvas optimization techniques for animations is to limit the amount of pixels that get cleared/painted on each frame. The easiest solution to implement is resetting the entire canvas element and drawing everything over again but that is an expensive operation for your browser to process.

The idea is to reuse as many pixels as possible between frames. What that means is the fewer pixels that need to be processed each frame, the faster your program will run. For example, when erasing pixels with the clearRect(x, y, w, h)method, it is very beneficial to clear and redraw only the pixels that have changed and not the full canvas.

Generating graphics procedurally is often the way to go, but sometimes that's not the most efficient one. If you're drawing simple shapes with solid fills, then drawing them procedurally is the best way do so. However, if you're drawing more detailed entities with strokes, gradient fills and other performance sensitive make-up you'd be better off using image sprites.

It is possible to get away with a mix of both. Draw graphical entities procedurally on the canvas once as your application starts up. After that you can reuse the same sprites by painting copies of them instead of generating the same drop-shadow, gradient and strokes repeatedly.

The canvas can be manipulated via transformations such as rotation and scaling, resulting in a change to the canvas coordinate system. This is where it's important to know about the state stack for which two methods are available:

context.save() - pushes the current state to the stack

context.restore() - reverts to the previous state

These enable you to apply transformation to a drawing and then restore back to the previous state to make sure the next shape is not affected by any earlier transformation. The states also include properties such as the fill and stroke colors.

A very powerful tool at hand when working with canvas is compositing modes which, amongst other things, allow for masking and layering. There's a wide array of available composite modes and they are all set through the canvas context's globalCompositeOperation property. The composite modes are also part of the state stack properties, so you can apply a composite operation, stack the state and apply a different one, and restore back to the state before where you made the first one. So it can be especially useful for this reason.

To allow for sub-pixel drawings, all browser implementations of canvas employ anti-aliasing (although this does not seem to be a requirement in the HTML5 spec). Anti-aliasing can be important to keep in mind if you want to draw crisp lines and notice the result looks blurred. This occurs because the browser will interpolate the image as though it was actually between those pixels. It results in a much smoother animation (you can genuinely move at half a pixel per update) but it'll make your images appear fuzzy.

To work around this you will need to either round to whole integer values or offset by half a pixel depending on if you're drawing fills or strokes.

Using Whole Numbers for drawImage() x and y Positions

If you call drawImage()on the canvas element, it's much faster if you round the x and y position to a whole number.

Here's a test case on jsperf showing how much faster using whole numbers is compared to using decimals. So it is a good idea to round your x and y position to whole numbers before rendering.

Another jsperf test shows that Math.round()is not necessarily the fastest method for rounding numbers. Using a bitwise hack actually turns out to be faster than the built in method.

Here’s a good article on canvas Sprite Optimization.

To clear the entire canvas of any existing pixels context.clearRect(x, y, w, h) is typically used – but there is another option available. Whenever the width and height of the canvas are set (even if they are set to the same value repeatedly) the canvas is reset. This is good to know when working with a dynamically sized canvas as you will notice drawings disappearing.

The Chrome Developer Tools profiler is very useful for finding out what your performance bottlenecks are. Depending on your application you may need to refactor some parts of your program to improve the performance and how browsers handle specific parts of your code.

Read more on canvas optimization techniques.

Here's some more tips and suggestions I put into a list worth sharing:

Don't include jQuery unless you need to do more than just selecting the .

I've managed to get by without it for almost everything I've made in canvas

Create abstracted functions and decouple your code. Separating functionality from appearance or initial draw state as much as possible can be very helpful in the long run and is just good practice in general.

Make common functions reusable as much as possible. Ideally, you should use a module pattern or some sort of abstracted API that breaks up code that you can reuse. I like to make a separate object that contains common functions and utilities.

Use single and double letter variable names only when it makes sense (x, y, z).

The coordinate system in canvas adds more single letters that are commonly declared as variables. Which can lead to creating multiple single/double variables (dX, dY, aX, aY, vX, vY) as part of an element. It’s better to be verbose and type out or at least abbreviate the variable names (dirX, accelX, velX) otherwise things could get pretty confusing for you later on. I’ve seen many people not doing this and it should be reiterated as a best practice.

Make constructor functions for generating anything that you will need more than one of. These can be useful for anything, whether you want to make multiples of the same shape, or at a lower level make vectors which add actions or other things to the prototype.

An example of a constructor I made for creating circles:

this.minX = this.minY = 20 + this.radius;

this.maxX = this.radius - (canvasWidth - 20);

ctx.arc(this.x, this.y, this.radius, 0, twoPI, true);

ball = new Ball(centerX, canvasHeight - paddle.height - 30);

A good base to work with is to create 3 functions

init() - do all the initial work, and setup the base vars and event handlers etc.

draw() - called once to begin the game and draws the first frame of the game, including the creation of elements that may be changing or need constructing.

update() - called at the end of draw() and within itself via requestAnimFrame. Updates properties of changing elements, only do what you need to do here.

Do the least amount of work within the loop updating and drawing only the changing pixels. Create the game elements and do any other UI work outside the animation loop. The animation loop is often a recursive function, which means it calls itself rapidly and repeatedly during the animation to draw each frame. If there are many elements being animated at once, you might want to first create the elements using a constructor function if you’re not already, and then within the constructor make a timer method that has requestAnimFrame/setTimeout sing it just how you would normally within any animation loop, but effects this element specifically only.

Consider adding timer(), draw() and animate() methods on each of your constructors for things that need to animate and for varying amounts of time. Doing this gives you full separation of control for each element and one big animation loop will not be necessary at all since the loop is broken up into each element and you start/stop at will.

Alternatively, create a Timer() constructor which you can use and give each animating element individually, thereby minimizing workload within animation loops.

After having worked on a large Facebook app which a canvas data-visualization as the primary focus and incorporated each users Facebook profile information (a massive amount of data for some people) to match you (and friends of yours also using the app) to Olympic athletes (a 6 degrees of separation type of thing) there's quite a lot I have learned in my extensive efforts to do everything I could possibly try for increasing performance within the app.

I literally spent months, and days at a time just working to refactor the code which I knew already so well, and believed it to be the most optimal way to do things. As it turned out in the end a valuable lesson I learned brings me to this last thing.

The fact is, browsers are still just not ready to handle more intensive running applications in canvas, especially if you're required to develop the app with support for Internet Explorer 8. There are sometimes cases where the DOM is faster than the current implementation of the canvas API at the time of writing this. At least I've found it to be while working on a massively complex single page animating html5 and canvas application for Samsung.

We were able to do quite well at improving the performance of things while still using canvas to do some complex work to crop images into circles, which would've probably been ok to stick with how we were doing it.

Days before the launch, we decided to try a different technique, and rather than create temporary canvases off-screen which were placed on the visible canvas once cropped into circles etc., we just appended Image DOM elements on the canvas, using the x and y coordinates that we had been using for placing the temp canvases before.

For cropping the images into circles, well that was simple, we just used the CSS3 border-radius property to do it which was far less work than the complex series of state changes and while ingenious and creative yet over-use of the clip() method.

Once they are placed in the DOM, the animation of images the occurs, and the DOM nodes for each image are animated as separate entities of the canvas. Ones that we can have full control over the styling off easily through CSS.

This technique is similar to another method for doing this type of work that is quite good to know as well, which involves layering canvases on top of each other, rather than draw them to one context.

Any automatic code formatting will immediately undo that indentation. Why not group it by leaving empty lines, like you would in any other part of the code? Like:

Maybe it's just me, but for me that's the most readable solution.

You can’t perform that action at this time.

---

## Optimizing canvas - Web APIs | MDN

`https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas`

element is one of the most widely used tools for rendering 2D graphics on the web. However, when websites and apps push the Canvas API to its limits, performance begins to suffer. This article provides suggestions for optimizing your use of the canvas element to ensure that your graphics perform well.

The following is a collection of tips to improve canvas performance.

Pre-render similar primitives or repeating objects on an offscreen canvas

If you find yourself repeating some of the same drawing operations on each animation frame, consider offloading them to an offscreen canvas. You can then render the offscreen image to your primary canvas as often as needed, without unnecessarily repeating the steps needed to generate it in the first place.

myCanvas.offscreenCanvas = document.createElement("canvas");

myCanvas.offscreenCanvas.width = myCanvas.width;

myCanvas.offscreenCanvas.height = myCanvas.height;

myCanvas.getContext("2d").drawImage(myCanvas.offscreenCanvas, 0, 0);

Avoid floating-point coordinates and use integers instead

Sub-pixel rendering occurs when you render objects on a canvas without whole values.

This forces the browser to do extra calculations to create the anti-aliasing effect. To avoid this, make sure to round all co-ordinates used in calls to

Cache various sizes of your images on an offscreen canvas when loading as opposed to constantly scaling them in

Use multiple layered canvases for complex scenes

In your application, you may find that some objects need to move or change frequently, while others remain relatively static. A possible optimization in this situation is to layer your items using multiple

For example, let's say you have a game with a UI on top, the gameplay action in the middle, and a static background on the bottom. In this case, you could split your game into three

layers. The UI would change only upon user input, the gameplay layer would change with every new frame, and the background would remain generally unchanged.

<canvas id="ui-layer" width="480" height="320"></canvas>

<canvas id="game-layer" width="480" height="320"></canvas>

<canvas id="background-layer" width="480" height="320"></canvas>

Use plain CSS for large background images

If you have a static background image, you can draw it onto a plain

property and position it under the canvas. This will negate the need to render the background to the canvas on every tick.

are faster since they use the GPU. The best case is to not scale the canvas, or have a smaller canvas and scale up rather than a bigger canvas and scale down.

const scaleX = window.innerWidth / canvas.width;

const scaleY = window.innerHeight / canvas.height;

const scaleToFit = Math.min(scaleX, scaleY);

const scaleToCover = Math.max(scaleX, scaleY);

stage.style.transformOrigin = "0 0"; // Scale from top left

stage.style.transform = `scale(${scaleToFit})`;

If your application uses canvas and doesn't need a transparent backdrop, set the

. This information can be used internally by the browser to optimize rendering.

const ctx = canvas.getContext("2d", { alpha: false });

You may find that canvas items appear blurry on higher-resolution displays. While many solutions may exist, a simple first step is to scale the canvas size up and down simultaneously, using its attributes, styling, and its context's scale.

const rect = canvas.getBoundingClientRect();

// Scale the context to ensure correct drawing operations

canvas.style.height = `${rect.height}px`;

Batch canvas calls together. For example, draw a polyline instead of multiple separate lines.

Render screen differences only, not the whole new state.

---

## How to Fix Low FPS in a Web Game | Bugnet Blog

`https://bugnet.io/blog/how-to-fix-web-game-low-fps-canvas`

How to Fix Low FPS in a Web Game | Bugnet Blog

Profile with the browser's performance tools, batch draw calls and minimize canvas state changes, cut per-frame allocations, and keep DOM and layout work out of the game loop.

A slow web game is usually drawing inefficiently or allocating every frame. The browser's profiler shows which. Here is how to find and fix the bottleneck.

Use the browser Performance panel to record a few seconds. It shows whether time goes to scripting, rendering, or GC. That tells you where to optimize instead of guessing.

2. Batch draws and minimize state changes

Each canvas state change and draw call costs. Batch sprites, sort by texture, and avoid redundant save/restore and context property changes per object. For WebGL, reduce draw calls with instancing or atlases.

Creating objects every frame triggers GC pauses. Reuse buffers and vectors. And keep DOM reads/writes and layout-triggering work out of requestAnimationFrame so the render loop is not stalled.

The hardest version of this to fix is the one you can't reproduce — it only happens on a player's hardware, OS, driver, or save state, under conditions that simply aren't present on your machine. A report that says “it crashed” or “it froze” gives you nothing to act on, so the bug survives release after release while quietly costing you players.

Automatic error capture closes that gap. Each failure arrives with its full stack trace, the device and OS, the build number, and a breadcrumb trail of what the player did right before it broke, so even a failure you have never seen becomes a specific, reproducible issue. Fold identical failures into one signature ranked by how many players each hits, and your worklist sorts itself worst-first instead of arriving as a stream of vague complaints.

This is where a tool like Bugnet earns its place. Its SDK captures every HTML5 error automatically with the full stack trace plus device, OS, memory, build, and game-state context, folds duplicates into one grouped issue with an occurrence count, and ties each to the build it first appeared on — so you fix the problem that hurts the most players first and confirm it is gone when its signature disappears from the next release.

Most of the time the fix is small. Seeing the failure clearly is the part that actually costs you.

---

## ⚠️ Paginas que NAO deram texto

- `https://freefrontend.com/html-canvas-api/` — HTTP 403
- `https://stackoverflow.com/questions/68733355/how-to-improve-html5-canvas-performance` — HTTP 403
