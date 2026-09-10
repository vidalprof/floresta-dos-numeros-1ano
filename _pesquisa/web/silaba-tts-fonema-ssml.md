# 🔎 Pesquisa: silaba-tts-fonema-ssml

> Busca: `TTS pronounce single syllable not spelled letters SSML phoneme IPA say-as characters portuguese edge-tts azure speech synthesis phoneme tag`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## Pronunciation with Speech Synthesis Markup Language (SSML) - Speech service - Foundry Tools | Microsoft Learn

`https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-pronunciation`

Pronunciation with Speech Synthesis Markup Language (SSML) - Speech service - Foundry Tools | Microsoft Learn

Access to this page requires authorization. You can try

Access to this page requires authorization. You can try

You can use Speech Synthesis Markup Language (SSML) with text to speech to specify how the speech is pronounced. For example, you can use SSML with phonemes and a custom lexicon to improve pronunciation. You can also use SSML to define how a word or mathematical expression is pronounced.

Refer to the following sections for details about how to use SSML elements to improve pronunciation. For more information about SSML syntax, see

element is used for phonetic pronunciation in SSML documents. Always provide human-readable speech as a fallback.

Phonetic alphabets are composed of phones, which are made up of letters, numbers, or characters, sometimes in combination. Each phone describes a unique sound of speech. The phonetic alphabet is in contrast to the Latin alphabet, where any letter might represent multiple spoken sounds. Consider the different

pronunciations of the letter "c" in the words "candy" and "cease" or the different pronunciations of the letter combination "th" in the words "thing" and "those."

For a list of locales that support phonemes, see footnotes in the

element's attributes are described in the following table.

The phonetic alphabet to use when you synthesize the pronunciation of the string in the

attribute. The string that specifies the alphabet must be specified in lowercase letters. The following options are the possible alphabets that you can specify:

A string containing phones that specify the pronunciation of the word in the

Each locale supports a specific phone set

. If the specified string contains unrecognized phones, text to speech service will return http 400 error for invalid SSML.

, to stress one syllable by placing stress symbol before this syllable, you need to mark all syllables for the word. Or else, the syllable before this stress symbol is stressed. For

, if you want to stress one syllable, you need to place the stress symbol after this syllable, whether or not all syllables of the word are marked.

The supported values for attributes of the

. In the first two examples, the values of

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">

<phoneme alphabet="ipa" ph="tÉ.ËmeÉª.toÊ"> tomato </phoneme>

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">

<phoneme alphabet="ipa" ph="tÉmeÉªËtoÊ"> tomato </phoneme>

<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="en-US">

<phoneme alphabet="sapi" ph="iy eh n y uw eh s"> en-US </phoneme>

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">

<s>His name is Mike <phoneme alphabet="ups" ph="JH AU"> Zhou </phoneme></s>

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">

<phoneme alphabet='x-sampa' ph='he."lou'>hello</phoneme>

You can define how single entities (such as company, a medical term, or an emoji) are read in SSML by using the

elements. To define how multiple entities are read, create an XML structured custom lexicon file. Then you upload the custom lexicon XML file and reference it with the SSML

For a list of locales that support custom lexicon, see footnotes in the

element's attributes are described in the following table.

The URI of the publicly accessible custom lexicon XML file with either the

is recommended but not required, GitHub URIs and other publicly accessible links are also supported. If you don't want to make custom lexicon public, you can use

. For more information about the custom lexicon file, see

Pronunciation Lexicon Specification (PLS) Version 1.0

The supported values for attributes of the

After you publish your custom lexicon, you can reference it from your SSML. The following SSML example references a custom lexicon that was uploaded to

https://www.example.com/customlexicon.xml

. We support lexicon URLs from Azure Blob Storage. However, note that other public URLs may not be compatible.

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"

xmlns:mstts="http://www.w3.org/2001/mstts"

<lexicon uri="https://www.example.com/customlexicon.xml"/>

BTW, we will be there probably at 8:00 tomorrow morning.

Could you help leave a message to Robert Benigni for me?

To define how multiple entities are read, you can define them in a custom lexicon XML file with either the

The custom lexicon file is a valid XML document, but it can't be used as an SSML document.

Here are some limitations of the custom lexicon file:

: The custom lexicon file size is limited to a maximum of 100 KB. If the file size exceeds the 100-KB limit, the synthesis request fails. You can split your lexicon into multiple lexicons and include them in SSML if the file size exceeds 100 KB.

: The custom lexicon is cached with the URI as the key on text to speech when it's first loaded. The lexicon with the same URI isn't reloaded within 15 minutes, so the custom lexicon change needs to wait 15 minutes at the most to take effect.

The supported elements and attributes of a custom lexicon XML file are described in the

Pronunciation Lexicon Specification (PLS) Version 1.0

. Here are some examples of the supported elements and attributes:

attribute to indicate which locale it should be applied for. One custom lexicon is limited to one locale by design, so if you apply it for a different locale, it doesn't work. The

attribute to indicate the alphabet used in the lexicon. The possible values are

element is case sensitive in the custom lexicon. For example, if you only provide a phoneme for the

elements are used to indicate the pronunciation of an acronym or an abbreviated term.

element provides text that describes how the

is pronounced. The syllable boundary is '.' in the IPA alphabet. The

element can't contain white space when you use the IPA alphabet.

that helps you find errors (with detailed error messages) in the custom lexicon file. Using the tool is recommended before you use the custom lexicon XML file in production with the Speech service.

The following XML example (not SSML) would be contained in a custom lexicon

file. When you use this custom lexicon, "BTW" is read as "By the way." "Benigni" is read with the provided IPA "bÉËniËnji."

xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"

xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon

http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"

You can't directly set the pronunciation of a phrase by using the custom lexicon. If you need to set the pronunciation for an acronym or an abbreviated term, first provide an

xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"

xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon

http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"

<phoneme>ËskÉtlÉnd.ËmiËdiÉm.weÉªv</phoneme>

You could also directly provide your expected

for the acronym or abbreviated term. For example:

The preceding custom lexicon XML file examples use the IPA alphabet, which is also known as the IPA phone set. We suggest that you use the IPA because it's the international standard. For some IPA characters, they're the "precomposed" and "decomposed" version when they're being represented with Unicode. The custom lexicon only supports the decomposed Unicode.

The Speech service defines sapi phonetic set for these locales:

. For more information on the detailed Speech service phonetic alphabet, see the

attribute with custom lexicons as demonstrated here:

xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"

xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xsi:schemaLocation="http://www.w3.org/2005/01/pronunciation-lexicon

http://www.w3.org/TR/2007/CR-pronunciation-lexicon-20071212/pls.xsd"

alphabet="x-microsoft-sapi" xml:lang="en-US">

<phoneme> b eh 1 - n iy - n y iy </phoneme>

element indicates the content type, such as number or date, of the element's text. This element provides guidance to the speech synthesis engine about how to pronounce the text.

element's attributes are described in the following table.

Indicates the content type of an element's text. For a list of types, see the following table.

Provides additional information about the precise formatting of the element's text for content types that might have ambiguous formats. SSML defines formats for content types that use them. See the following table.

Indicates the level of detail to be spoken. For example, this attribute might request that the speech synthesis engine pronounce punctuation marks. There are no standard values defined for

The following content types are supported for the

attribute values are supported for all locales of the following languages: Arabic, Catalan, Chinese, Danish, Dutch, English, French, Finnish, German, Hindi, Italian, Japanese, Korean, Norwegian, Polish, Portuguese, Russian, Spanish, and Swedish.

The text is spoken as individual letters (spelled out). The speech synthesis engine pronounces:

<say-as interpret-as="characters">Test</say-as>

<say-as interpret-as="characters" format="casesensitive">Test</say-as>

The text is spoken as individual letters (spelled out) with proper pause. The speech synthesis engine pronounces:

<say-as interpret-as="alphanumeric" format="spell">ABCDEF</say-as>

You can specify pause with "-". The speech synthesis engine pronounces:

<say-as interpret-as="alphanumeric" format="spell">AB-CD-EF</say-as>

The text is spoken as a cardinal number. The speech synthesis engine pronounces:

There are <say-as interpret-as="cardinal">10</say-as> options

The text is spoken as an ordinal number. The speech synthesis engine pronounces:

Select the <say-as interpret-as="ordinal">3rd</say-as> option

The text is spoken as a sequence of individual digits. The speech synthesis engine pronounces:

<say-as interpret-as="number_digit">123456789</say-as>

The text is spoken as a fractional number. The speech synthesis engine pronounces:

<say-as interpret-as="fraction">3/8</say-as> of an inch

). The speech synthesis engine pronounces:

Today is <say-as interpret-as="date">10-12-2016</say-as>

As "Today is October twelfth two thousand sixteen."

Today is <say-as interpret-as="date" format="dmy">10-12-2016</say-as>

As "Today is December tenth two thousand sixteen."

attribute specifies whether the time is specified by using a 12-hour clock (hms12) or a 24-hour clock (hms24). Use a colon to separate numbers representing hours, minutes, and seconds. Here are some valid time examples: 12:35, 1:14:32, 08:15, and 02:50:45. The speech synthesis engine pronounces:

The train departs at <say-as interpret-as="time" format="hms12">4:00am</say-as>

attribute specifies the duration's format (

). The speech synthesis engine pronounces:

<say-as interpret-as="duration">01:18:30</say-as>

As "one hour eighteen minutes and thirty seconds".

<say-as interpret-as="duration" format="ms">01:18</say-as>

This tag is only supported on English and Spanish.

The text is spoken as a telephone number. The speech synthesis engine pronounces:

The number is <say-as interpret-as="telephone">(888) 555-1212</say-as>

As "My number is area code eight eight eight five five five one two one two."

The text is spoken as a currency. The speech synthesis engine pronounces:

<say-as interpret-as="currency">99.9 USD</say-as>

As "ninety-nine US dollars and ninety cents."

The text is spoken as a unit. The speech synthesis engine pronounces:

<say-as interpret-as="unit">10 m</say-as>

The text is spoken as an address. The speech synthesis engine pronounces:

I'm at <say-as interpret-as="address">150th CT NE, Redmond, WA</say-as>

As "I'm at 150th Court Northeast Redmond Washington."

The text is spoken as a person's name. The speech synthesis engine pronounces:

In Chinese names, some characters pronounce differently when they appear in a family name. For example, the speech synthesis engine says ä» in

<say-as interpret-as="name">ä»åç</say-as>

The supported values for attributes of the

The speech synthesis engine speaks the following example as "Your first request was for one room on October nineteenth twenty ten with early arrival at twelve thirty five PM."

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">

<voice name="en-US-Ava:DragonHDLatestNeural">

Your <say-as interpret-as="ordinal"> 1st </say-as> request was for <say-as interpret-as="cardinal"> 1 </say-as> room

on <say-as interpret-as="date" format="mdy"> 10/19/2010 </say-as>, with early arrival at <say-as interpret-as="time" format="hms12"> 12:35pm </say-as>.

element to indicate that the alias attribute's text value should be pronounced instead of the element's enclosed text. In this way, the SSML contains both a spoken and written form.

element's attributes are described in the following table.

The text value that should be pronounced instead of the element's enclosed text.

The supported values for attributes of the

The speech synthesis engine speaks the following example as "World Wide Web Consortium."

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">

<voice name="en-US-Ava:DragonHDLatestNeural">

<sub alias="World Wide Web Consortium">W3C</sub>

To read the markdown content, you can wrap the markdown text with the

element. TTS only reads the text content in the markdown and ignores the markdown syntax.

For example, the following SSML will read out two sentences: "This is headline" and "And this is a bold text", and the markdown syntax won't be read.

<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>

TTS supports the markdown syntax defined in the CommonMark specification, which is a widely used markdown specification. For more information about the CommonMark specification, see

There are two ways to read a mathematical expression:

Embed the plain text mathematical expression directly in SSML and specify the math domain using

Reading plain text mathematical expressions

Represent the mathematical expression with MathML elements.

Reading mathematical expressions with MathML

The two features are currently supported in the following locales: de-DE, en-AU, en-GB, en-US, all the sibling locales of English, es-ES, es-MX, all the sibling locales of Spanish, fr-CA, fr-FR, it-IT, ja-JP, ko-KR, pt-BR, and zh-CN.

Reading plain text mathematical expressions

To enable complex mathematical expression reading, you can add

element to enable math-specific pronunciation rules.

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">

<voice name="en-US-AvaMultilingualNeural">

By default, parentheses aren't read out in mathematical expressions.

If you'd like the parentheses read out, you can specify

<mstts:mathspeechverbosity level="verbose" />

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">

<voice name="en-US-AvaMultilingualNeural">

<mstts:prompt domain="Math" /><mstts:mathspeechverbosity level="verbose" />

If you'd like the expression read out in other language with a multilingual voice, specify lang element in SSML.

<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">

<voice name="en-US-AvaMultilingualNeural">

<lang xml:lang="es-ES">x = (-b Â± â(bÂ² - 4ac)) / 2a</lang>

Reading mathematical expressions with MathML

The Mathematical Markup Language (MathML) is an XML-compliant markup language that describes mathematical content and structure. The Speech service can use the MathML as input text to properly pronounce mathematical notations in the output audio.

specifications are supported, except the MathML 3.0

Take note of these MathML elements and attributes:

<math xmlns="http://www.w3.org/1998/Math/MathML">

elements don't output speech, so they're ignored.

If an element isn't recognized, it'll be ignored, but the child elements within it will still be processed.

The XML syntax doesn't support the MathML entities, so you must use the corresponding

to represent the entities, for example, the entity

should be represented by its unicode characters

The text to speech output for this example is "a squared plus b squared equals c squared".

<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>

<math xmlns='http://www.w3.org/1998/Math/MathML'>

Language support: Voices, locales, languages

Want to try using Ask Learn to clarify or guide you through this topic?

---

## Speech Synthesis Markup Language (SSML)  |  Cloud Text-to-Speech  |  Google Cloud Documentation

`https://docs.cloud.google.com/text-to-speech/docs/ssml`

Speech Synthesis Markup Language (SSML)  |  Cloud Text-to-Speech  |  Google Cloud Documentation

Save and categorize content based on your preferences.

in your Cloud Text-to-Speech request to allow for more customization in your

audio response by providing details on pauses, and audio formatting for

acronyms, dates, times, abbreviations, or text that should be censored.

The following shows an example of SSML markup and the Cloud TTS

src="https://www.example.com/MY_MP3_FILE.mp3">didn't

Here is the synthesized text for the example SSML document:

The Cloud TTS supports a subset of the available SSML tags,

For more information about how to create audio data from SSML input with the

If you're new to Google Cloud, create an account to evaluate how

scenarios. New customers also get $300 in free credits to run, test, and

Depending on your implementation, you may need to escape

quotation marks or quotes in the SSML payload that you send to

Cloud TTS. The following example shows how to

format SSML input included within a JSON object.

'ssml':'<speak>The <say-as interpret-as=\"characters\">SSML</say-as>

standard <break time=\"1s\"/>is defined by the

<sub alias=\"World Wide Web Consortium\">W3C</sub>.</speak>'

Avoid using SSML reserve characters in the text that is to be converted

to audio. When you need to use an SSML reserve character, prevent the

character from being read as code by using its escape code. The following

table shows reserved SSML characters and their associated escape codes.

The following sections describe the SSML elements and options that can be used in your Actions.

Your browser does not support the HTML5 Audio element.

An empty element that controls pausing or other prosodic boundaries between words. Using

between any pair of tokens is optional. If this element is not present between words, the break is automatically determined based on the linguistic context.

Sets the length of the break by seconds or milliseconds (e.g. "3s" or "250ms").

Sets the strength of the output's prosodic break by relative terms. Valid values are: "x-weak", weak", "medium", "strong", and "x-strong". The value "none" indicates that no prosodic break boundary should be outputted, which can be used to prevent a prosodic break that the processor would otherwise produce. The other values indicate monotonically non-decreasing (conceptually increasing) break strength between tokens. The stronger boundaries are typically accompanied by pauses.

The following example shows how to use the

Step 1, take a deep breath. <break time="200ms"/>

Step 3, take a deep breath again. <break strength="weak"/>

Your browser does not support the HTML5 Audio element.

This element lets you indicate information about the type of text construct that is contained within the element. It also helps specify the level of detail for rendering the contained text.

, which determines how the value is spoken. Optional attributes

The following example is spoken as "forty two dollars and one cent". If the language attribute is omitted, it uses the current locale.

<say-as interpret-as='currency' language='en-US'>$42.01</say-as>

The following example is spoken as "one eight zero zero two zero two one two one two". If the "google:style" attribute is omitted, it speaks zero as letter O.

The "google:style='zero-as-zero'" attribute currently only works in EN locales.

<say-as interpret-as='telephone' google:style='zero-as-zero'>1800-202-1212</say-as>

The following example is spelled out letter by letter:

<say-as interpret-as="verbatim">abcdefg</say-as>

Your browser does not support the HTML5 Audio element.

attribute is a sequence of date field character codes. Supported field character codes in

} for year, month, and day (of the month) respectively.  If the field code appears once for year, month, or day then the number of digits expected are 4, 2, and 2 respectively. If the field code is repeated then the number of expected digits is the number of times the code is repeated.  Fields in the date text may be separated by punctuation and/or spaces.

attribute controls the spoken form of the date. For

only the day fields and one of month or year fields are required, although both may be supplied. This is the default when less than all three fields are given. The spoken form is "The {ordinal day} of {month}, {year}".

The following example is spoken as "The tenth of September, nineteen sixty":

<say-as interpret-as="date" format="yyyymmdd" detail="1">

Your browser does not support the HTML5 Audio element.

The following example is spoken as "The tenth of September":

<say-as interpret-as="date" format="dm">10-9</say-as>

Your browser does not support the HTML5 Audio element.

the day, month, and year fields are required and this is the default when all three fields are supplied. The spoken form is "{month} {ordinal day}, {year}".

The following example is spoken as "September tenth, nineteen sixty":

<say-as interpret-as="date" format="dmy" detail="2">

Your browser does not support the HTML5 Audio element.

The following example is spoken as "C A N":

<say-as interpret-as="characters">can</say-as>

Your browser does not support the HTML5 Audio element.

The following example is spoken as "Twelve thousand three hundred forty five" (for US English) or "Twelve thousand three hundred and forty five (for UK English)":

<say-as interpret-as="cardinal">12345</say-as>

Your browser does not support the HTML5 Audio element.

The following example is spoken as "First":

<say-as interpret-as="ordinal">1</say-as>

Your browser does not support the HTML5 Audio element.

The following example is spoken as "five and a half":

<say-as interpret-as="fraction">5+1/2</say-as>

Your browser does not support the HTML5 Audio element.

The following example comes out as a beep, as though it has been censored:

<say-as interpret-as="expletive">censor this</say-as>

Your browser does not support the HTML5 Audio element.

Converts units to singular or plural depending on the number. The following example is spoken as "10 feet":

<say-as interpret-as="unit">10 foot</say-as>

Your browser does not support the HTML5 Audio element.

The following example is spoken as "Two thirty P.M.":

<say-as interpret-as="time" format="hms12">2:30pm</say-as>

Your browser does not support the HTML5 Audio element.

attribute is a sequence of time field character codes. Supported field character codes in

} for hour, minute (of the hour), second (of the minute), time zone, 12-hour time, and 24-hour time respectively. If the field code appears once for hour, minute, or second then the number of digits expected are 1, 2, and 2 respectively. If the field code is repeated then the number of expected digits is the number of times the code is repeated.  Fields in the time text may be separated by punctuation and/or spaces.  If hour, minute, or second are not specified in the format or there are no matching digits then the field is treated as a zero value. The default

attribute controls whether the spoken form of the time is 12-hour time or 24-hour time. The spoken form is 24-hour time if

is omitted and the format of the time is 24-hour time. The spoken form is 12-hour time if

is omitted and the format of the time is 12-hour time.

Supports the insertion of recorded audio files and the insertion of other audio formats in conjunction with synthesized speech output.

A URI referring to the audio media source. Supported protocol is

that is the offset from the audio source's beginning to start playback from. If this value is greater than or equal to the audio source's actual duration, then no audio is inserted.

that is the offset from the audio source's beginning to end playback at. If the audio source's actual duration is less than this value, then playback ends at that time.  If

The ratio output playback rate relative to the normal input rate expressed as a percentage. The format is a positive

followed by %. The currently supported range is [50% (slow - half speed), 200% (fast - double speed)].  Values outside that range may (or may not) be adjusted to be within it.

specifying how many times to insert the audio (after clipping, if any, by

). Fractional repetitions aren't supported, so the value will be rounded to the nearest integer. Zero is not a valid value and is therefore treated as being unspecified and has the default value in that case.

that is a limit on the duration of the inserted audio after the source is processed for

attributes (rather then the normal playback duration). If the duration of the processed audio is less than this value, then playback ends at that time.

decibels. Maximum range is +/-40dB but actual range may be effectively less, and output quality may not yield good results over the entire range.

The following are the currently supported settings for audio:

Single channel is preferred, but stereo is acceptable.

240 seconds maximum duration. If you want to play audio with a longer duration, consider implementing a

Our UserAgent when fetching the audio is "Google-Speech-Actions".

element are optional and are used if the audio file cannot be played or if the output device does not support audio.  The contents may include a

element in which case the text contents of that element are used for display. For more information, see the Recorded Audio section in the

can host your audio files on an https URL).

To learn more about media responses, see the

Your browser does not support the HTML5 Audio element.

<p><s>This is sentence one.</s><s>This is sentence two.</s></p>

Your browser does not support the HTML5 Audio element.

Use <s>...</s> tags to wrap full sentences, especially if they contain SSML elements that change prosody (that is, <audio>, <break>, <emphasis>, <par>, <prosody>, <say-as>, <seq>, and <sub>).

If a break in speech is intended to be long enough that you can hear it, use <s>...</s> tags and put that break between sentences.

Indicate that the text in the alias attribute value replaces the contained text for pronunciation.

element to provide a simplified pronunciation of a difficult-to-read word. The last example below demonstrates this use case in Japanese.

<sub alias="World Wide Web Consortium">W3C</sub>

Your browser does not support the HTML5 Audio element.

Your browser does not support the HTML5 Audio element.

An empty element that places a marker into the text or tag sequence. It can be used to reference a

specific location in the sequence or to insert a marker into an output stream

Your browser does not support the HTML5 Audio element.

Used to customize the pitch, speaking rate, and volume of text contained by the element. Currently the

. There are three options for setting the value of the

Specify a relative value (e.g. "low", "medium", "high", etc) where "medium" is the default pitch.

st" respectively. Note that "+/-" and "st" are required.

%" respectively. Note that "%" is required but "+/-" is optional.

element to speak slowly at 2 semitones lower than normal:

<prosody rate="slow" pitch="-2st">Can you hear me now?</prosody>

Your browser does not support the HTML5 Audio element.

Used to add or remove emphasis from text contained by the element. The

, but without the need to set individual speech attributes.

This element supports an optional "level" attribute with the following valid values:

<emphasis level="moderate">This is an important announcement</emphasis>

Your browser does not support the HTML5 Audio element.

A parallel media container that allows you to play multiple media elements at once. The only allowed content is a set of one or more

Unless a child element specifies a different begin time, the implicit begin time for the element is the same as that of the

container. If a child element has an offset value set for its

attribute, the element's offset will be relative to the beginning time of the

element, the begin attribute is ignored and the beginning time is when SSML speech synthesis process starts generating output for the root

<speak>Who invented the Internet?</speak>

<media xml:id="answer" begin="question.end+2.0s">

<speak>The Internet was invented by cats.</speak>

<media begin="answer.end-0.2s" soundLevel="-6dB">

src="https://actions.google.com/.../cartoon_boing.ogg"/>

<media repeatCount="3" soundLevel="+2.28dB"

src="https://actions.google.com/.../cat_purr_close.ogg"/>

Your browser does not support the HTML5 Audio element.

A sequential media container that allows you to play media elements one after another. The only allowed content is a set of one or more

elements. The order of the media elements is the order in which they are rendered.

attributes of child elements can be set to offset values (see

below). Those child elements' offset values will be relative to the end of the previous element in the sequence or, in the case of the first element in the sequence, relative to the beginning of its

<speak>Who invented the Internet?</speak>

<speak>The Internet was invented by cats.</speak>

src="https://actions.google.com/.../cartoon_boing.ogg"/>

<media repeatCount="3" soundLevel="+2.28dB"

src="https://actions.google.com/.../cat_purr_close.ogg"/>

Your browser does not support the HTML5 Audio element.

element. The following table describes the valid attributes for a

A unique XML identifier for this element. Encoded entities are not supported. The allowed identifier values match the regular expression

The beginning time for this media container. Ignored if this is the root media container element (treated the same as the default of "0"). See the

A specification for the ending time for this media container. See the

specifying how many times to insert the media. Fractional repetitions aren't supported, so the value will be rounded to the nearest integer. Zero is not a valid value and is therefore treated as being unspecified and has the default value in that case.

that is a limit on the duration of the inserted media. If the duration of the media is less than this value, then playback ends at that time.

decibels. Maximum range is +/-40dB but actual range may be effectively less, and output quality may not yield good results over the entire range.

over which the media will fade in from silent to the optionally-specified

. If the duration of the media is less than this value, the fade in will stop at the end of playback and the sound level will not reach the specified sound level.

over which the media will fade out from the optionally-specified

until it is silent. If the duration of the media is less than this value, the sound level is set to a lower value to ensure silence is reached at the end of playback.

A time specification, used for the value of `begin` and `end` attributes of

elements), is either an offset value (for example,

- Time offset value is an SMIL Timecount-value that allows values that match the regular expression:

"\s\*(+|-)?\s\*(\d+)(\.\d+)?(h|min|s|ms)?\s\*"

The first digit string is the whole part of the decimal number and the second digit string is the decimal fractional part. The default sign (i.e. "(+|-)?") is "+". The unit values correspond to hours, minutes, seconds, and milliseconds respectively. The default for the units is "s" (seconds).

- A syncbase value is an SMIL syncbase-value that allows values that match the regular expression:

"([-_#]|\p{L}|\p{D})+\.(begin|end)\s\*(+|-)\s\*(\d+)(\.\d+)?(h|min|s|ms)?\s\*"

The digits and units are interpreted in the same way as an offset value.

tag to produce custom pronunciations of words

tag directs the pronunciation of a single

There are up to three levels of stress that can be placed in a transcription:

: Denoted with /ˈ/ in IPA and /"/ in X-SAMPA.

: Denoted with /ˌ/ in IPA and /%/ in X-SAMPA.

: Not denoted with a symbol (in either notation).

Some languages might have fewer than three levels or not denote stress placement

levels available for your language. Stress markers are placed at the start of

each stressed syllable. For example, in US English:

As a general rule, keep your transcriptions more broad and phonemic in nature.

For example, in US English, transcribe intervocalic /t/ (instead of using a

There are some instances where using the phonemic representation makes your TTS

results sound unnatural (for example, if the sequence of phonemes is

One example of this is voicing assimilation for /s/ in English. In this case the

assimilation should be reflected in the transcription:

Every syllable must contain one (and only one) vowel. This means that you should

avoid syllabic consonants and instead transcribe them with a reduced vowel. For

You can optionally specify syllable boundaries by using /./. Each syllable must

contain one (and only one) vowel. For example:

As an alternative to providing pronunciations inline with the

tag, provide a dictionary of custom pronunciations in the speech synthesis RPC. When the custom pronunciation dictionary is in the request, the input text will automatically be transformed with the SSML

As an example, the following request with text input and custom pronunciation will be transformed and will be equivalent to the SSML below.

text: 'Hello world! It is indeed a beautiful world!',

ssml: '<speak>Hello <phoneme alphabet="ipa" ph="wɜːld">world</phoneme>! It is indeed a beautiful <phoneme alphabet="ipa" ph="wɜːld">world</phoneme>!</speak>'

durations. For example, the following example would be verbalized as

<say-as interpret-as="duration" format="h:m">5:30</say-as>

The format string supports the following values:

tag allows you to use more than one voice in a single SSML

request. In the following example, the default voice is an English male voice.

All words will be synthesized in this voice except for "qu'est-ce qui t'amène

ici", which will be verbalized in French using a female voice instead of the

default language (English) and gender (male).

<speak>And then she asked, <voice language="fr-FR" gender="female">qu'est-ce qui

t'amène ici</voice><break time="250ms"/> in her sweet and gentle voice.</speak>

<speak>The dog is friendly<voice name="fr-CA-Wavenet-B">mais la chat est

mignon</voice><break time="250ms"/> said a pet shop

a combination of the following attributes. All three attributes are

optional but you must provide at least one if you don't provide a

: Used as a tiebreaker in cases where there are multiple possibilities

of which voice to use based on your configuration.

: Your desired language. Only one language can be specified in a

tag. Specify your language in BCP-47 format. You can find

You can also control the relative priority of each of the

preferred attributes rather than required. The Cloud Text-to-Speech API considers

preferred attributes on a best effort basis in the order they are listed

tag. If any preferred attributes are configured

incorrectly, Cloud TTS might still return a valid voice but

with the incorrect configuration dropped.

<speak>And there it was <voice language="en-GB" gender="male" required="gender"

ordering="gender language">a flying bird </voice>roaring in the skies for the

---

## Speech Synthesis Markup Language (SSML) overview - Speech service - Foundry Tools | Microsoft Learn

`https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup`

Speech Synthesis Markup Language (SSML) overview - Speech service - Foundry Tools | Microsoft Learn

Access to this page requires authorization. You can try

Access to this page requires authorization. You can try

Speech Synthesis Markup Language (SSML) overview

Speech Synthesis Markup Language (SSML) is an XML-based markup language that you can use to fine-tune your text to speech output attributes such as pitch, pronunciation, speaking rate, volume, and more. It gives you more control and flexibility than plain text input.

You can hear voices in different styles and pitches reading example text by using the

SSML is designed to give you flexibility in how you want your speech output to sound, and it provides different properties for how you can customize that output. You can use SSML to:

that determines the structure, content, and other characteristics of your text to speech output. For example, you can use SSML to define a paragraph, a sentence, a break or a pause, or silence. You can wrap text with event tags, like a bookmark or viseme, that your application can process later. A viseme is the visual description of a phoneme, the individual speech sounds, in spoken language.

, language, name, style, and role. You can use multiple voices in a single SSML document. You can also adjust the emphasis, speaking rate, pitch, and volume. SSML can also insert prerecorded audio, such as a sound effect or a musical note.

of the output audio. For example, you can use SSML with phonemes and a custom lexicon to improve pronunciation. You can also use SSML to define how a word or mathematical expression is pronounced.

SSML functionality is available in various tools that might fit your use case.

You're billed for each character that's converted to speech, including punctuation. Although the SSML document itself isn't billable, the service counts optional elements that you use to adjust how the text is converted to speech, like phonemes and pitch, as billable characters. For more information, see the

tool lets you author plain text and SSML in Speech Studio. You can listen to the output audio and adjust the SSML to improve speech synthesis. For more information, see

Speech synthesis with the Audio Content Creation tool

accepts SSML via the "speak" SSML method across the different supported languages.

Language and voice support for the Speech service

Want to try using Ask Learn to clarify or guide you through this topic?

---

## Fix TTS Pronunciation Errors: Developer's Guide 2026

`https://deepgram.com/learn/developers-guide-fixing-tts-pronunciation-errors`

Fix TTS Pronunciation Errors: Developer's Guide 2026

A Developer's Guide to Fixing Common TTS Pronunciation Errors

Systematic approach to fix TTS pronunciation errors using SSML, lexicons, and text preprocessing. Includes testing strategies for production deployment.

TTS pronunciation errors cluster into four predictable categories: heteronyms that require context disambiguation, domain terminology absent from training data, alphanumeric sequences with ambiguous verbalization rules, and text normalization failures on dates, currency, and structured data.

Each category demands different correction approaches. SSML phoneme tags work for isolated words. PLS lexicons scale for domain vocabulary. Text preprocessing catches systematic patterns before synthesis. The challenge is matching error types to correction methods based on your latency constraints, maintenance capacity, and provider capabilities. This guide maps that decision framework.

TTS pronunciation errors cluster into predictable categories, each requiring different correction methods: heteronyms, domain terminology, alphanumeric sequences, and text normalization failures.

SSML phoneme tags provide runtime pronunciation control for cloud providers that support the standard, while Deepgram Aura-2 handles pronunciation through text formatting and preprocessing.

PLS lexicons centralize pronunciation corrections for domain vocabulary, though support and activation mechanisms vary by provider.

Text preprocessing catches normalization errors before they reach the TTS engine, reducing runtime overhead and working independently of provider-specific features.

Automated WER testing with targets below 5% catches pronunciation regressions before production deployment.

What Causes TTS Systems to Mispronounce Words in Production

TTS pronunciation errors originate from predictable pattern categories. Understanding these categories is the first step to fix TTS pronunciation errors in any production environment.

Heteronyms are words spelled identically but pronounced differently based on context. The word "read" requires the TTS engine to determine tense from surrounding context, while "lead" could represent either a metal or a verb. According to

, modern TTS implementations handle these through contextual word embeddings and part-of-speech tagging, achieving 99.1% accuracy on balanced datasets. Basic systems without these capabilities often struggle with heteronym disambiguation.

Domain terminology fails because models train on general language corpora. Medical terms like "hyperkalemia" and technical terms like "Kubernetes" appear rarely in training data, causing the model to apply incorrect pronunciation rules. Brand names with unusual spellings or mixed case patterns create consistent pronunciation failures.

Alphanumeric Sequences and Structured Data

Alphanumeric sequences represent the highest-impact enterprise challenge.

integrated Deepgram's speech recognition and achieved 2-4x accuracy improvements for alphanumeric inputs in contact center self-service interactions, directly improving authentication rates and self-service containment. A major healthcare provider using the Five9 integration doubled their user authentication rates due to improved alphanumeric transcription accuracy.

Text normalization failures occur when the TTS engine misinterprets how to verbalize non-standard text. Dates like "12/05/2024" create ambiguity between US and European conventions. Currency amounts like "$1,234.56" risk literal reading. Abbreviations like "Dr." could expand to "Doctor" or "Drive" depending on context. Fraction expressions like "1/2" might be read as "one slash two" instead of "one half."

How SSML Phoneme Tags Override Pronunciation at Runtime

SSML phoneme tags let you specify exact pronunciation using phonetic notation, bypassing the TTS engine's internal pronunciation decisions. The

defines the standard syntax that cloud TTS providers implement.

This forces the TTS engine to pronounce "pecan" with the stress pattern you specify.

or X-SAMPA notation for phoneme tags. X-SAMPA (Extended Speech Assessment Methods Phonetic Alphabet) uses only ASCII characters, making it easier to type and embed in code without Unicode handling concerns. The same "pecan" example in X-SAMPA would be written as ph='pI"kA:n'.

Choose IPA when working with linguists or when documentation requires standard phonetic notation. Choose X-SAMPA when your development workflow benefits from ASCII-only text or when your team finds the notation more readable.

Combining Phoneme Tags with Say-As for Structured Data

For structured data like dates and currency, SSML provides the <say-as> element with interpret-as attributes. This approach works well for predictable patterns where you want the TTS engine to apply standard verbalization rules rather than specifying exact phonemes.

Teams looking to fix TTS pronunciation errors systematically should evaluate their provider's SSML support first.

support standard SSML phonemes. Deepgram Aura-2 handles pronunciation through text formatting rather than SSML, which means preprocessing logic in your application layer becomes the primary mechanism for pronunciation control.

Building Pronunciation Lexicons for Persistent Corrections

When pronunciation errors affect dozens of terms, managing individual SSML tags becomes unsustainable. The

W3C PLS (Pronunciation Lexicon Specification)

provides a standardized approach for centralized pronunciation files, though support varies significantly by provider.

PLS Lexicon Structure and Required Elements

A PLS lexicon is an XML file containing lexeme entries that map graphemes (written forms) to phonemes (pronunciations):

http://www.w3.org/2005/01/pronunciation-lexicon

Some providers offer managed lexicon storage through dedicated REST APIs with lexicons stored at the account level. Each lexicon can contain up to 40,000 characters, and you can store up to 100 lexicons per account per region. Activation is explicit: you must specify lexicon names in each synthesis API call.

Other providers require developers to host lexicon files externally and reference them via URI in SSML. These providers support files up to 100KB and cache lexicons for 15 minutes. Inline SSML phoneme tags take precedence over lexicon pronunciations.

Managing Lexicons Across Languages and Locales

Group entries by domain (medical terminology, product names, geographic locations) to simplify maintenance and reduce conflicts. Implement version control for lexicon files, treating them as code artifacts with change tracking and rollback capabilities.

For teams building US English pronunciations, the

provides an excellent starting point with over 134,000 words in ARPAbet notation, which can be converted to IPA for use in PLS files.

Text Normalization Strategies That Prevent Pronunciation Errors

Text normalization converts non-standard text into speakable forms before the TTS engine processes it. This preprocessing approach catches errors systematically and operates independently of your TTS provider.

Expanding Numbers, Dates, and Currency Values

Alphanumeric sequences require explicit formatting. "ABC123" should render as "A-B-C-one-two-three" rather than "ABC one hundred twenty-three." Insert hyphens or spaces between characters to force character-by-character reading.

Currency amounts require careful preprocessing to avoid literal symbol reading. Transform "$1.50" into "one dollar and fifty cents" rather than risking "dollar sign one point five zero."

Date formats need locale-aware preprocessing. Transform "12/05/2024" into "December fifth, twenty twenty-four" for US audiences or "the fifth of December, twenty twenty-four" for UK audiences.

Handling Abbreviations and Acronyms Consistently

Phone numbers lack standardized pronunciation rules. Format them explicitly: "555-123-4567" should be preprocessed into "five five five, one two three, four five six seven" to ensure natural rhythm and clear digit separation.

Addresses contain multiple simultaneous challenges. "123 N. Main St." requires number reading mode determination, directional abbreviation expansion, and context-dependent abbreviation handling.

Deepgram Aura-2 handles entity pronunciation through text formatting. Punctuation controls pacing, and specific formatting patterns allow consistent verbalization of structured data. This means preprocessing logic in your application layer provides pronunciation control without requiring SSML support.

Testing Pronunciation Fixes Before Production Deployment

provides the primary metric for pronunciation accuracy:

Where S = Substitutions, I = Insertions, D = Deletions, and N = Total words in reference text. Target WER below 5% for production deployment.

Building Test Sets from Production Error Logs

Build regression test suites targeting your highest-risk content categories:

Alphanumeric ID pronunciation (highest-impact pattern for contact centers)

Date format ambiguity and regional conventions

Domain-specific terminology for your vertical

provides production-tested evaluation tools for measuring pronunciation accuracy. Run evaluations with:

Automated Regression Testing for Pronunciation

Integrate pronunciation testing into your deployment pipeline. Establish quality thresholds and fail builds when accuracy drops below standards. For subjective quality assessment,

evaluation has listeners rate speech samples on a 1-5 scale, with scores above 4.0 indicating near-human quality.

A/B testing pronunciation fixes in production lets teams validate improvements with real user interactions before full rollout. Deploy pronunciation changes to a subset of traffic and monitor customer satisfaction metrics, call completion rates, and escalation frequency. Continuous testing is essential to fix TTS pronunciation errors before they impact customer experience.

Selecting Fix Strategies Based on Error Patterns and Constraints

Different pronunciation errors demand different solutions based on frequency, latency tolerance, and maintenance capacity.

For low-frequency errors affecting specific words, inline SSML phoneme tags provide targeted fixes when supported by your TTS provider.

For domain vocabulary affecting multiple synthesis requests, PLS lexicons centralize corrections where provider support exists.

For systematic patterns like dates and alphanumeric sequences, text preprocessing catches errors before synthesis and operates independently of provider-specific features.

Multi-stage preprocessing with context detection

Multi-stage preprocessing with context detection

When building voice applications requiring entity-accurate pronunciation and low latency, the

delivers sub-200ms response times with domain-specific pronunciation accuracy for healthcare, finance, and legal terminology. For complete voice agent implementations, the

combines speech-to-text, LLM orchestration, and text-to-speech in a unified solution at $4.50 per hour.

Build voice applications with Deepgram's Aura-2 text-to-speech.

Create a free account in the Deepgram Console

and get $200 in credits to test TTS functionality.

How do I fix TTS pronunciation errors for words that aren't in any dictionary?

Use phonetic respelling in your source text for maximum provider compatibility. For "Kubernetes," preprocess to "koo-ber-net-eez" before sending to the TTS engine. This approach works across all providers regardless of SSML support. Test multiple respelling variations to find which produces the most natural pronunciation for your target voice. For systematic coverage, maintain a preprocessing dictionary that maps technical terms to phonetic respellings, and update it based on production error logs.

What causes TTS to pronounce numbers differently in different contexts?

Context detection algorithms classify numbers using surrounding text patterns. "Order 2024" triggers year pronunciation, while "Order number 2024" may trigger digit sequence reading. The detection fails in ambiguous contexts. Control this by reformatting before TTS processing: add explicit delimiters like hyphens for digit sequences ("2-0-2-4") or write out desired forms ("two thousand twenty-four" for year contexts). For phone numbers, use consistent delimiter patterns that signal digit-by-digit reading to your specific TTS provider.

Can I use the same pronunciation fixes across different TTS providers?

Text preprocessing works universally because it modifies input before any provider processes it. This makes preprocessing the most portable approach for multi-provider architectures. SSML support varies:

support standard SSML phonemes, while Deepgram Aura-2 requires text-based preprocessing. Build your pronunciation layer using text normalization first, then add provider-specific SSML as optimization where available. This maintains portability while allowing provider-specific enhancements when switching providers is not an option.

Voice AI telephony integration: carriers, SLAs and global rollout

Voice agent function calling: real-time data lookup during a call

The Rise of PER: A New Standard for Measuring TTS Accuracy

Voice agent testing: how to evaluate before you take real calls

Speech prosody across languages: what transfers and what breaks

Q&A with Deepgram’s New Chief Product Officer, Ed Anuff

Voice AI latency: why pauses read as hesitation

Paralanguage in voice AI: a complete guide to paralinguistic cues

Unlock voice AI at scale with an API Call

Get conversational intelligence with transcription and understanding on the world's best speech AI platform.

---

## Controlling pronunciation in TTS: SSML, phonemes, and beyond | The Voice AI Wiki

`https://soniox.com/wiki/pronunciation-control-ssml`

Controlling pronunciation in TTS: SSML, phonemes, and beyond | The Voice AI Wiki

A voice reads "Siobhan" as "see-OH-ban," "Reyes" as "rays," and your product name as something you do not recognize. The model is not malfunctioning; it is guessing, because spelling does not predict sound and these are exactly the words its

step was never going to get right. Names, brands, acronyms, and numbers are where every TTS deployment eventually has to override the model.

The tools for overriding it run from a crude rewrite to an exact phonetic spec. The sections below begin at the crude end, so the lightest tool that fixes the problem comes first.

The crudest fix rewrites the text phonetically and lets the model read the rewrite: "Reyes" becomes "rayes," "Nguyen" becomes "win." It costs nothing and sometimes works.

Respelling is also fragile. It fights spelling with more spelling, so the result varies between voices and languages, and it corrupts the real text, which causes problems wherever that string is later displayed or logged. It is a stopgap rather than a permanent fix.

is the first proper tool. It tells the voice how to

problem in reverse: is "1234" a number, a year, or digits to read one at a time?

a string is, not how a word sounds. It resolves the ambiguity that text normalization alone would have to guess.

When you want the voice to say something different from what is written,

This handles abbreviations that expand differently by context ("St." as "Street" or "Saint") and acronyms you want spoken as words or expanded, without altering the displayed text.

When you need a specific pronunciation and nothing else will do, specify the sounds directly with the

tag, using a phonetic alphabet, usually IPA or X-SAMPA.

This is the most reliable tool, because it specifies the exact sequence of sounds instead of leaving the reading to the model. It does require knowing the phonetic transcription and the alphabet the system accepts, and IPA versus X-SAMPA support varies. Phonemes suit a fixed set of names and terms that must be correct every time.

Pronunciation covers more than sounds. It also includes pacing and stress, the territory of

These tags should be used sparingly. They suit a specific line that must be delivered a particular way; good default prosody handles ordinary text.

Annotating every occurrence of a term is tedious and error-prone. A pronunciation lexicon (the W3C format is PLS) is a dictionary of terms and their pronunciations that applies across all your text at once, so "Soniox" or a drug name is said correctly everywhere without per-instance tags.

For any deployment with a stable vocabulary, a lexicon is the maintainable option, with inline SSML reserved for one-off cases.

The lightest tool that fixes the problem is preferable. Precision and required effort both rise down the list.

SSML originated with the concatenative and parametric systems of the 2000s, and it assumes a pipeline that can be instructed tag by tag. The newest

do not always work that way. Some support a subset of SSML, some ignore it, and some replace it: supplying surrounding context so the model infers the right reading, prompting with an example, or accepting a custom dictionary rather than inline phonemes.

SSML support is one of the least standardized corners of TTS: an implementation may honor a subset of tags and silently ignore the rest.

So test pronunciation against the synthesizer you actually chose, not the spec, and keep a documented way to correct names, numbers, and domain terms. Every production deployment ends up needing one.

Speech Synthesis Markup Language, a W3C XML format for annotating text with how to speak it, covering everything from interpreting numbers and dates to specifying exact phonemes.

It is the traditional vehicle for pronunciation control, but support is one of the least standardized parts of TTS, so never assume a given system honors a given tag.

How do I make a TTS voice say a name correctly?

For a one-off, reach for the lightest tool that works, ending at a

tag in IPA or X-SAMPA when nothing softer holds. For a name that recurs, put it in a pronunciation lexicon (PLS) so it is correct everywhere at once, instead of re-tagging every occurrence and getting it wrong somewhere.

Why does the same word get read two different ways?

Because it is a homograph like "read," "lead," "bass," or "live," and the model picks a reading from context, sometimes wrongly. When it guesses wrong, pin the reading with a phoneme tag or a substitution rather than hoping more context fixes it.

Do modern neural TTS systems still use SSML?

Inconsistently: some support a subset, some ignore it, some replace it with context or custom dictionaries. The need to override pronunciation stays permanent even when the syntax does not, so test your real names and numbers on your actual system rather than assuming SSML works.

Rao, K., Peng, F., Sak, H., & Beaufays, F. (2015).

Grapheme-to-phoneme conversion using long short-term memory recurrent neural networks

2015 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 4584–4588

Shirali-Shahreza, S., Luitjens, P., Morcos, N., Xiao, W., & Penn, G. (2017).

Crowdsourcing the Pronunciation of Out-of-Vocabulary Words

The AAAI-17 Workshop on Crowdsourcing, Deep Learning, and Artificial Intelligence Agents

Analysis of pronunciation learning in end-to-end speech synthesis

Proceedings of Interspeech 2019, 2070–2074

Speech Synthesis Markup Language (SSML) Version 1.1

Pronunciation Lexicon Specification (PLS) Version 1.0

Ould Ouali, N., Sani, A. H., Bueno, R., & Dauvet, J. (2025).

Improving French Synthetic Speech Quality via SSML Prosody Control

Proceedings of the 8th International Conference on Natural Language and Speech Processing (ICNLSP)

Fine-Grained Prosody Control in Neural TTS Systems

Bachelor's thesis, Karlsruhe Institute of Technology

---

## SSML for Production TTS: Complete Text-to-Speech SSML Guide in 2026

`https://picovoice.ai/blog/ssml-text-to-speech/`

SSML for Production TTS: Complete Text-to-Speech SSML Guide in 2026

SSML for Text-to-Speech: Complete Guide for Production TTS in 2026

Get dedicated support to ensure your specific needs are met.

SSML (Speech Synthesis Markup Language) is the W3C standard for controlling how text-to-speech engines render speech. It uses XML tags to specify pauses, pronunciation, pitch, speaking rate, emphasis, and number/date formatting. The core tags (

) are supported by Google Cloud TTS, Amazon Polly, and Azure Speech Service, though each provider adds proprietary extensions and restricts certain tags on newer neural voice models. This guide covers every production-relevant SSML tag with code examples, documents where the three major providers diverge, and explains alternative pronunciation control methods used by engines that do not implement SSML.

Speech Synthesis Markup Language (SSML) is an XML-based W3C standard that gives developers explicit control over how a TTS engine converts text into spoken audio. Without SSML, cloud TTS engines rely on non-deterministic inference to guess pauses, number formatting, and syllable stress. SSML overrides these defaults with structured tags, guaranteeing consistent, predictable audio output.

forces the engine to read "5" as "five" (not "fifth" or "five-point-zero"), and

inserts a 300-millisecond pause. Without these tags, the engine would infer both behaviors from context, sometimes incorrectly.

When a TTS engine receives SSML input, it parses the XML before synthesis begins. The engine extracts the plain text, then applies the markup instructions during three stages of the TTS pipeline:

tags override the engine's default rules for expanding abbreviations, numbers, dates, and other non-standard text. For example,

<say-as interpret-as="date" format="mdy">01/02/2026</say-as>

forces "January second, twenty twenty-six" rather than "one slash two slash twenty twenty-six."

tag provides an explicit phonetic transcription using IPA (

) or a provider-specific alphabet like X-SAMPA. This overrides the engine's

(G2P) model for words it mispronounces, such as proper nouns, medical terms, or foreign-language words embedded in an English sentence.

tags modify pitch, rate, and volume at the utterance or word level. The

tag inserts silence of a specified duration. These controls shape the rhythm and expressiveness of the output.

TTS engines process these instructions and generate an audio waveform (typically PCM, MP3, or Opus). SSML is not rendered in the output audio; it is consumed entirely during synthesis.

SSML Tag Reference: Examples for Production

The following tags form the production-relevant subset of SSML 1.1. Each tag is described with its attributes and a code example.

Every SSML document must be wrapped in the root element,

inserts a pause. Accepts time (e.g., "250ms", "1s") or strength ("none", "x-weak", "weak", "medium", "strong", "x-strong"). If neither is specified, the engine inserts a default medium-strength pause.

Controls how the engine interprets a text construct. The interpret-as attribute is required. Common values:

cardinal / ordinal: reads "5" as "five" vs. "fifth"

characters / spell-out: reads each character individually ("A-B-C")

date: reads as a date, with a format attribute ("mdy", "dmy", "ymd")

telephone: reads digit sequences as phone numbers

currency: reads "$42.50" as "forty-two dollars and fifty cents"

Provides a phonetic pronunciation, overriding the engine's G2P model. The alphabet attribute specifies the phonetic system ("ipa" for International Phonetic Alphabet, "x-sampa" for X-SAMPA). Amazon Polly also accepts "x-amazon-pinyin" for Mandarin. The ph attribute contains the phonetic transcription. This tag is critical for proper nouns, medical/legal terminology, and brand names.

Replaces the contained text with the alias for pronunciation. Unlike

provides a plain-text replacement rather than a phonetic transcription. Useful for acronyms and abbreviations.

Modifies pitch, rate, and volume. Accepts absolute values, relative adjustments, or named presets. Attributes: rate ("x-slow", "slow", "medium", "fast", "x-fast", or a percentage like "80%"), pitch ("x-low" through "x-high", or "+2st" / "-3st" for semitone adjustments), volume ("silent" through "x-loud", or "+6dB").

This section is read slowly at a lower pitch.

Adds or reduces emphasis on a word or phrase. Accepts a level attribute: "strong", "moderate", "reduced", or "none". The acoustic effect varies by engine (pitch change, duration stretch, or volume boost).

Mark paragraph and sentence boundaries. These tags help the engine apply appropriate prosodic phrasing (longer pauses between paragraphs, rising/falling intonation at sentence boundaries). They are optional in most cases but recommended when SSML content contains other tags that modify prosody, as wrapping content in

tags prevents unintended phrasing artifacts.

SSML Compatibility: AWS Polly vs. Google Cloud TTS vs. Azure vs. ElevenLabs

All three major cloud TTS providers support the core SSML tags (

), but each restricts specific tags on newer neural and generative voice models. Azure has the broadest SSML support; Google restricts

on Studio/Chirp voices; Amazon Polly restricts

SSML tag support by TTS provider (Azure Speech Services, Google Cloud TTS, Amazon Polly, and ElevenLabs) across break, say-as, phoneme, sub, prosody, emphasis, and paragraph/sentence tags.

Support verified against provider documentation, July 2026.

SSML Examples: Common Patterns for Production Applications

1. Reading confirmation codes and order numbers

IVR systems and order confirmation flows need alphanumeric codes read character by character, with pauses between groups for comprehension.

Financial applications need consistent currency formatting, including handling zero cents and multi-currency contexts.

Domain-specific terms that the G2P model consistently mispronounces can be corrected with

. For terms that appear repeatedly, define them once in a custom lexicon (supported by Amazon Polly and Azure) rather than repeating

4. Controlling pacing in long-form narration

For audiobook or announcement applications,

tags control pacing without editing the source text.

The quarterly results exceeded projections.

Operating expenses declined for the third consecutive quarter.

Get dedicated support to ensure your specific needs are met.

Alternatives to SSML for Pronunciation Control

, designed for on-device or streaming deployment, uses lighter-weight approaches to pronunciation control. These alternatives avoid the XML parsing overhead and can be embedded directly in the input text stream, which matters for streaming TTS pipelines where tokens arrive one at a time from an LLM.

Some engines accept pronunciation overrides as inline markup within plain text rather than XML. For example,

curly-brace notation with ARPAbet phonemes

, and IPA for other languages to embed the pronunciation directly in the text string. This approach integrates with streaming input, where the engine processes LLM tokens as they arrive without needing a complete XML document.

Amazon Polly and Azure Speech Service support custom lexicons (PLS format), which define pronunciation rules that apply to all synthesis requests without repeating

tags. Google Cloud TTS does not support custom lexicons. For applications with a large number of domain-specific terms (medical, legal, financial), lexicons reduce SSML verbosity and centralize pronunciation management.

Modern neural TTS engines handle most text normalization and prosody decisions without SSML. SSML adds value in specific scenarios: correcting mispronounced proper nouns or technical terms, enforcing exact pause timing in IVR flows, controlling number/date/currency formatting in localized applications, and adjusting pitch or rate for accessibility compliance. If the TTS engine pronounces the content correctly without markup, adding SSML increases complexity with no benefit.

Orca Streaming Text-to-Speech runs on-device across all platforms with custom pronunciation support via inline ARPAbet phonemes. Enterprise customers work with the Picovoice team for custom voice models with emotional and stylistic controls.

SSML (Speech Synthesis Markup Language) is a W3C XML standard that controls how text-to-speech engines render speech. It provides tags for inserting pauses (

), and formatting numbers, dates, and currencies (

). All major cloud TTS providers (Google Cloud TTS, Amazon Polly, Azure Speech Service) support a subset of SSML 1.1.

Do all text-to-speech engines support SSML?

No. SSML support varies by engine and by voice model within the same engine. Cloud APIs from Google, Amazon, and Microsoft support core SSML tags, though newer neural and generative voice models restrict certain tags like

, and only on specific models. On-device TTS engines like Piper TTS and Orca do not use SSML; they use alternative approaches such as inline phoneme notation or rely on their G2P models.

How do I fix mispronounced words in TTS without SSML?

Three common approaches exist. First, use the

tag if the engine supports SSML, replacing the problematic text with a phonetically spelled alias. Second, use engine-specific inline notation; Orca accepts

directly in the text. Third, define a custom pronunciation lexicon (supported by Amazon Polly and Azure) that applies corrections globally without modifying the input text.

What is the difference between <phoneme> and <sub> in SSML?

provides a phonetic transcription using IPA or X-SAMPA, giving precise control over every sound in a word.

provides a plain-text replacement that the engine then processes through its own G2P model.

is simpler but depends on the engine's pronunciation of the replacement text.

SSML parsing overhead depends on the implementation. Complex SSML documents with many tags can increase preprocessing time slightly. Generally, it is negligible relative to model inference time. For streaming TTS pipelines that process LLM tokens in real time, engines that accept inline pronunciation notation rather than SSML avoid the need to buffer and parse a complete XML document.

Custom Pronunciation in TTS: Abbreviations, Names, and Domain Terms

Learn five methods to fix TTS pronunciation for abbreviations, names, and domain terms. Compare SSML phoneme tags, custom lexicons, inline n...

How to Evaluate TTS Quality: MOS Scores, Benchmarks, and Testing

A developer guide to evaluating text-to-speech quality. Covers MOS scores, UTMOS, PESQ, POLQA, FTTS latency, RTF, and memory benchmarks with...

Nuance Text-to-Speech Alternatives and Migration to On-device TTS

Nuance Vocalizer reaches end of life in 2026-2027. Compare cloud, on-premise, and on-device TTS alternatives with deployment, latency, and c...

On-Device ElevenLabs Alternatives for Production Voice AI (2026)

Looking for an ElevenLabs alternative that runs on-device? Compare latency, cost, and quality for production voice AI proven by an open-sour...

On-device TTS Comparison: Open-source Benchmark 2026

Benchmark-driven comparison of on-device TTS engines for production deployment. Latency, memory, model size, and platform support data from ...

TTS Audio Formats: WAV, MP3, PCM, and Opus Compared

How to choose the right audio output format for text-to-speech. Compare PCM, WAV, MP3, and Opus on file size, latency, quality, and streamin...

Complete Guide to Text-to-Speech (TTS) Technology (2026)

Everything you need to know about Text-to-Speech technology: how it works, why it matters, and how to build natural-sounding voice experienc...

Text-to-Speech Latency: How to Read Vendor Claims and Minimize TTS Latency

When building conversational AI applications, TTS latency can make or break the user experience. A 3-second delay may feel like an eternity ...

---

## Custom Pronunciation in TTS: Abbreviations, Names, and Domain Terms

`https://picovoice.ai/blog/custom-pronunciation-in-tts/`

Custom Pronunciation in TTS: Abbreviations, Names, and Domain Terms

Custom Pronunciation in TTS: Abbreviations, Names, and Domain Terms

Get dedicated support to ensure your specific needs are met.

engine mispronounces something. Abbreviations like "SCSI" come out letter-by-letter instead of "scuzzy." Foreign surnames get flattened. Medical terms like "dyspnea" trip up even high-end models. The root cause is always the same: the engine's grapheme-to-phoneme (G2P) layer guessed wrong.

This guide covers five concrete methods to override G2P defaults, compares provider support across Google Cloud TTS, Amazon Polly, Azure Speech, ElevenLabs, and Orca, and walks through fixes for the most common pronunciation failures.

What Is Grapheme-to-Phoneme (G2P) Conversion?

(G2P) conversion maps written characters (graphemes) to speech sounds (phonemes). Modern TTS engines use neural G2P models trained on pronunciation dictionaries. The

, for example, contains 106,837 training words with ARPAbet transcriptions for North American English. Transformer-based G2P models achieve the highest accuracy on known words but still fail on inputs outside their training distribution.

Three categories of words consistently break G2P:

"NATO" should be spoken as a word; "FBI" should be spelled out. G2P has no reliable way to distinguish the two without context.

The surname "Ng" is a single syllable (roughly "eng"). Place names like "Worcestershire" follow historical pronunciation, not spelling.

Medical, legal, and technical vocabularies contain thousands of words absent from general dictionaries. "Apheresis," "estoppel," and "kubectl" are everyday terms in their fields but uncommon in G2P training sets.

element, which lets developers specify exact pronunciation using a phonetic alphabet. This is the most precise override available. The engine bypasses G2P entirely for the tagged word and uses the supplied phonemes.

for simple replacements, but offers no custom lexicon API. Amazon Polly supports both

and X-SAMPA in phoneme tags, plus custom lexicons via the W3C

Pronunciation Lexicon Specification (PLS)

. Azure Speech accepts IPA and SAPI phoneme alphabets alongside custom lexicon uploads.

with IPA and CMU ARPAbet on Flash v2, Turbo v2, and English v1 models. As of June 2026, V3 models have opt-in phoneme support. Phoneme tags are currently English-only on ElevenLabs.

element replaces one string with another before G2P runs. It does not specify phonemes directly; instead, it substitutes a word the engine already pronounces correctly.

This works well for abbreviations that should expand ("WHO" to "World Health Organization") and for numbers or symbols that need specific readings ("St." to "Street" vs. "Saint").

defines an XML format for mapping words to pronunciations. A lexicon file can contain hundreds of entries and applies to every synthesis call that references it.

http://www.w3.org/2005/01/pronunciation-lexicon

. Azure Speech supports custom lexicon uploads as well. Google Cloud TTS does not support PLS lexicons. ElevenLabs does not support lexicons.

Before sending text to the TTS engine, a preprocessing layer can apply regex-based or dictionary-based transformations. This is provider-agnostic and works with any engine, including those with limited SSML support. Common preprocessing tasks:

Expanding abbreviations: "Dr." to "Doctor," "vs." to "versus."

Normalizing numbers: "$3.5M" to "three point five million dollars."

Handling mixed-case acronyms: applying letter-by-letter reading for all-caps tokens under a certain length.

The downside is that preprocessing rules accumulate technical debt. A large rule set becomes hard to maintain and can introduce unexpected interactions. Rules also run before SSML parsing, so they must produce valid SSML if the output contains tags.

takes a different approach. Instead of wrapping words in XML tags, Orca uses a lightweight inline syntax:

The word goes before the pipe, ARPAbet phonemes after it. No XML parsing, no separate lexicon file. This makes inline notation a natural fit for

pipelines where SSML overhead adds latency. Orca also supports

, extending pronunciation control beyond English.

Pronunciation Override Support by TTS Providers

Comparison matrix of TTS provider support for phoneme tags, alphabets, the SSML <sub> element, custom lexicons, and inline phonetic notation.

Acronyms like "API," "SQL," and "CEO" need letter-by-letter reading. Two reliable approaches:

Insert periods or spaces between letters ("S.Q.L." or "S Q L") before sending to the engine. Less elegant, but works everywhere.

Abbreviations That Should Be Spoken as Words

"NASA," "SCSI," and "GIF" should be spoken as words, not spelled out. If the engine spells them, use

to replace them with a phonetic respelling ("scuzzy" for SCSI) or use

Names are the hardest category. "Ng" is roughly "eng" in common American usage. "Siobhan" is "shih-VAWN." No G2P model covers every name. The fix is almost always a phoneme tag with IPA or ARPAbet, stored in a custom lexicon if the application handles many names.

Domain vocabularies contain thousands of words that general G2P models have never seen. "Dyspnea" (disp-NEE-uh), "amicus" (uh-MEE-kus), and "kubectl" (cube-control) are everyday terms in their fields. Build a domain-specific lexicon or preprocessing dictionary before deployment. A healthcare TTS application might start with 500+ medical term overrides; that list will grow.

Heteronyms are words spelled the same but pronounced differently depending on meaning. "Read" (present) vs. "read" (past). "Lead" (the verb) vs. "lead" (the metal). "Bass" (the fish) vs. "bass" (the instrument). Context-aware G2P models handle common heteronyms, although it's harder for streaming text-to-speech engines, as they cannot predict the upcoming words: I read a book every day vs. I read a book yesterday.

provides inline pronunciation control with zero XML overhead, supports ARPAbet for English and IPA subsets for non-English languages, and runs on-device for privacy-sensitive deployments. Explore the

What is the best phonetic alphabet for TTS pronunciation overrides?

is the most widely supported and covers all languages. ARPAbet is simpler for English-only applications. The choice depends on provider support and whether the application needs multilingual pronunciation.

How many custom lexicon entries can a TTS provider handle?

It depends on the vendor. Amazon Polly allows up to five PLS lexicons per synthesis request. Azure Speech supports custom lexicon uploads with no published entry limit. Google Cloud TTS does not support custom lexicons. For large vocabularies (1,000+ terms), preprocessing or inline notation may be more practical than lexicon files.

Do pronunciation overrides work in real-time TTS?

SSML parsing adds some overhead. For latency-sensitive applications, inline notation (as used by Orca) avoids XML parsing entirely. Preprocessing rules also add minimal latency since they run as simple string operations before synthesis.

Can G2P models be fine-tuned for specific domains?

Some research models support fine-tuning on custom pronunciation dictionaries. However, most commercial TTS APIs do not expose G2P fine-tuning. The practical alternatives are custom lexicons, phoneme tags, and preprocessing rules.

What is the difference between IPA and ARPAbet?

IPA uses Unicode symbols to represent sounds across all human languages. ARPAbet uses ASCII character sequences to represent American English phonemes. ARPAbet is easier to type and read for English-only work. IPA is necessary for multilingual applications. The

How to Evaluate TTS Quality: MOS Scores, Benchmarks, and Testing

A developer guide to evaluating text-to-speech quality. Covers MOS scores, UTMOS, PESQ, POLQA, FTTS latency, RTF, and memory benchmarks with...

Nuance Text-to-Speech Alternatives and Migration to On-device TTS

Nuance Vocalizer reaches end of life in 2026-2027. Compare cloud, on-premise, and on-device TTS alternatives with deployment, latency, and c...

On-Device ElevenLabs Alternatives for Production Voice AI (2026)

Looking for an ElevenLabs alternative that runs on-device? Compare latency, cost, and quality for production voice AI proven by an open-sour...

On-device TTS Comparison: Open-source Benchmark 2026

Benchmark-driven comparison of on-device TTS engines for production deployment. Latency, memory, model size, and platform support data from ...

SSML for Text-to-Speech: Complete Guide for Production TTS in 2026

Complete SSML reference for production TTS, covering SSML tags with code examples to explain and SSML coverage among Google, AWS, Azure, and...

TTS Audio Formats: WAV, MP3, PCM, and Opus Compared

How to choose the right audio output format for text-to-speech. Compare PCM, WAV, MP3, and Opus on file size, latency, quality, and streamin...

Complete Guide to Text-to-Speech (TTS) Technology (2026)

Everything you need to know about Text-to-Speech technology: how it works, why it matters, and how to build natural-sounding voice experienc...

Text-to-Speech Latency: How to Read Vendor Claims and Minimize TTS Latency

When building conversational AI applications, TTS latency can make or break the user experience. A 3-second delay may feel like an eternity ...

---

## Supported SSML tags - Amazon Polly

`https://docs.aws.amazon.com/polly/latest/dg/supportedtags.html`

are supported for Standard voices. Tag availability for other voices is provided in the following table.

Amazon Polly supports the following SSML tags:

Specifying another language for specific words

Controlling volume, speaking rate, and pitch

Setting a maximum duration for synthesized speech

Controlling how special types of words are spoken

Improving pronunciation by specifying parts of speech

If you use unsupported SSML tags in standard, neural, or long-form

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

---
