# 🔎 Pesquisa: acessibilidade-crianca-semana-34

> Busca: `accessibility children touch targets colour blindness screen reader learning app`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## Make apps more accessible  |  App quality  |  Android Developers

`https://developer.android.com/guide/topics/ui/accessibility/apps`

Make apps more accessible  |  App quality  |  Android Developers

Save and categorize content based on your preferences.

Try to make your Android app usable for everyone, including people with

People with impaired vision, color blindness, impaired hearing, impaired

dexterity, cognitive disabilities, and many other disabilities use Android

accessibility in mind, you make the user experience better for people with

This page presents guidelines for implementing key elements of accessibility

so that everyone can use your app more easily. For more in-depth guidance on

how to make your app more accessible, see

For each set of text within your app, we recommend the

difference in perceived brightness between the color of the text and the color

of the background behind the text—to be above a specific threshold. The

exact threshold depends on the text's font size and whether the text appears in

If the text is smaller than 18sp, or if the text is bold and smaller than

14sp, use foreground and background colors that result in a

For all other text, set the color contrast ratio to at least 3:1.

The following image shows two examples of text-to-background color contrast:

Lower than recommended (left) and sufficient (right) color

To check the text-to-background color contrast in your app, use an online color

Your app's UI is easier to use if its controls are easier to see and tap. For

touch interfaces, we recommend that each interactive UI element have a focusable

, of at least 48dpx48dp. Larger is even better.

In Jetpack Compose, many built-in Material components like

already enforce this minimum size. However, when

creating custom interactive elements, you need to set the size yourself.

In the following snippet, a small UI element is made accessible by giving it a

For more information about touch target sizes, see

For each UI element in your app, include a description that

describes the element's purpose. In most cases, you include this description in

attribute, as shown in the following code

composables. Android accessibility services (like TalkBack) automatically

When adding descriptions to your app's UI elements, keep the following best

Use descriptions to convey the purpose and result of the interaction, not the

way, screen readers can announce the element correctly.

example, if selecting a button causes a "submit" action to occur in your app,

Each description should be unique. That way, when screen reader users

encounter a repeated element description, they correctly recognize that the

focus is on an element that already had focus earlier. In particular, each item

a different description, each reflecting the content that's unique

to a given item, such as the name of a city in a list of locations.

API to mark purely decorative elements so

that accessibility services can ignore them. If a UI element has a

parameter but is purely decorative (such as an

that is part of another UI element), pass

Test your code to make sure the content description is delivered as expected.

can flag common issues and expose problems in your implementation.

To learn more about making your app more accessible, see the following

Build more accessible UIs with Jetpack Compose

Content and code samples on this page are subject to the licenses described in the

. Java and OpenJDK are trademarks or registered trademarks of Oracle and/or its affiliates.

---

## Accessibility designing – Material Design 3

`https://m3.material.io/foundations/designing/structure`

Accessibility designing – Material Design 3

---

## Accessibility  |  Mobile  |  Android Developers

`https://developer.android.com/design/ui/mobile/guides/foundations/accessibility`

Accessibility  |  Mobile  |  Android Developers

Save and categorize content based on your preferences.

2011 report by the World Health Organization (WHO) and the

, approximately 15% of the global population–that is,

about one in six people–experience a significant or temporary disability in

their lifetime. Accessibility in design, then, is

inclusive, usable, and high-quality app–it leads to the best results for users

and can prevent costly rework. Android ships with a variety of features to help

you build your app to support accessibility options by default.

Ensure your app's content is as legible as possible by checking color contrast

and text sizing, and that components are visually comprehensible and easy to

Follow these guidelines to design for vision accessibility.

To allow users to adjust the font size, specify font size in

Don't make the body size any smaller than 12 sp. This guideline aligns with the

Ensure the contrast between the background and text is at least 4.5:1.

Use a 3:1 ratio between surfaces and non-text elements. For example, the ratio of a

Use more than one visual affordance for actions like links.

based on tonal palettes, and is central to making color schemes accessible by

is a Google screen reader included on Android devices

that gives users eyes-free control. You can manually test this by

Follow these guidelines to ensure your app is prepared for screen readers:

to inform accessibility services about the information shown

To satisfy Android framework requirements, provide additional textual

Set decorative item descriptions to null.

To allow skipping between blocks of actions and content, consider UI

walks you through accessibility considerations and notation using Web Content

UI elements labeled for accessibility: heading, hiding decorative image, and button label

Android provides features to enable users to interact with their devices through

app for Android lets you control your device

with spoken commands. Use your voice to open apps, navigate, and edit text

lets users interact with your Android device

using one or more devices, which can be helpful for users with limited dexterity

who have trouble interacting directly with a touch screen.

Don't rely on gestures to complete all actions;

Ensure all touch targets are at least 48 dp, even if this extends past the UI

The UI on the left lets the user delete only by swiping,

while the UI on the right also provides an additional affordance in the form

Content and code samples on this page are subject to the licenses described in the

. Java and OpenJDK are trademarks or registered trademarks of Oracle and/or its affiliates.

---

## Accessibility | Apple Developer Documentation

`https://developer.apple.com/design/human-interface-guidelines/accessibility`

Accessibility | Apple Developer Documentation

---

## Resources for developers and publishers â Google Accessibility

`https://www.google.com/intl/en-GB/accessibility/for-developers/`

Resources for developers and publishers â Google Accessibility

Information and resources to help you develop accessible products and apps.

Google encourages developers and publishers to design and build products and applications with accessibility in mind.

Making applications accessible not only ensures equal access to the roughly one billion people in the world with disabilities, but also benefits people without disabilities by allowing them to customise their experiences.

Android has an accessibility layer that helps blind and low vision users navigate their Android devices more easily. These services provide features such as text-to-speech, haptic feedback and trackball/directional pad navigation that augment the user experience.

Android Developer Accessibility Resources

Android developers can learn to design and test for accessibility using the resources below. Accessibility testing tools can help you catch common mistakes like missing content descriptions, insufficient contrast and undersized touch targets.

Accessibility checks in Robolectric testing framework

Accessibility checks in Espresso testing framework

, including many screen readers and magnifiers.

screen reader for Chrome OS. ChromeVox is available for developers to use as an extension for Chrome on the desktop. This extension allows developers to test their web apps with a screen reader inside the browser so that they can experience their products as a blind user would and conduct better accessibility testing.

Chrome Extensions are another way to make the browser more accessible for any user without needing to install external software. There are already great examples of

that allow users, including those with disabilities, to customise their experience. Learn how to

Web Accessibility by Google â Udacity course

Web Fundamentals: Accessibility â text-based course

Lighthouse: An open-source, automated tool for improving the quality of web pages

Material Design colour tool: Measure the accessibility of any colour combination

There are numerous ways to ensure that your video has closed captions. You can

by uploading a caption file, creating a new caption file from scratch, or having

YouTube automatically time your transcript. YouTube also automatically captions videos uploaded in supported

languages, which you can then edit for accuracy. Visit our blog for more information on the general state of

makes it easy to interact with and upload captions. Take a look at the Open Source

, which is a working example of how to use the API to interact with captions in YouTube, and can be used by anyone to upload multiple caption tracks for videos on a channel that they own.

Android has an accessibility layer that helps blind and low vision users navigate their Android devices more easily. These services provide features such as text-to-speech, haptic feedback and trackball/directional pad navigation that augment the user experience.

Android Developer Accessibility Resources

Android developers can learn to design and test for accessibility using the resources below. Accessibility testing tools can help you catch common mistakes like missing content descriptions, insufficient contrast and undersized touch targets.

Accessibility checks in Robolectric testing framework

Accessibility checks in Espresso testing framework

, including many screen readers and magnifiers.

screen reader for Chrome OS. ChromeVox is available for developers to use as an extension for Chrome on the desktop. This extension allows developers to test their web apps with a screen reader inside the browser so that they can experience their products as a blind user would and conduct better accessibility testing.

Chrome Extensions are another way to make the browser more accessible for any user without needing to install external software. There are already great examples of

that allow users, including those with disabilities, to customise their experience. Learn how to

Web Accessibility by Google â Udacity course

Web Fundamentals: Accessibility â text-based course

Lighthouse: An open-source, automated tool for improving the quality of web pages

Material Design colour tool: Measure the accessibility of any colour combination

There are numerous ways to ensure that your video has closed captions. You can

by uploading a caption file, creating a new caption file from scratch, or having

YouTube automatically time your transcript. YouTube also automatically captions videos uploaded in supported

languages, which you can then edit for accuracy. Visit our blog for more information on the general state of

makes it easy to interact with and upload captions. Take a look at the Open Source

, which is a working example of how to use the API to interact with captions in YouTube, and can be used by anyone to upload multiple caption tracks for videos on a channel that they own.

---
