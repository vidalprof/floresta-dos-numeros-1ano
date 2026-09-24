# 🔎 Pesquisa: motores-de-video-no-navegador

> Busca: `WebCodecs VideoEncoder browser support Chrome version ffmpeg.wasm SharedArrayBuffer requirement mp4-muxer webm-muxer browser video editor library`

> Trazido pelo `pesquisar.yml` (a internet do GitHub). **Isto e MATERIA-PRIMA,
> nao regra.** So vira regra da casa depois de eu destilar em `_pesquisa/` e o
> Marcos aprovar. Texto de terceiro: ler com juizo.

---

## VideoEncoder - Web APIs | MDN

`https://developer.mozilla.org/en-US/docs/Web/API/VideoEncoder`

This feature is not Baseline because it does not work in some of the most widely-used browsers.

Want more browser support for this feature?

An integer representing the number of encode queue requests.

Represents the state of the underlying codec and whether it is configured for encoding.

Returns a promise indicating whether the provided

Asynchronously prepares the encoder to accept video frames for encoding with the specified parameters.

Returns a promise that resolves once all pending encodes have been completed.

Cancels all pending encodes and callbacks.

Ends all pending work and releases system resources.

---

## GitHub - ffmpegwasm/ffmpeg.wasm: FFmpeg for browser, powered by WebAssembly · GitHub

`https://github.com/ffmpegwasm/ffmpeg.wasm`

GitHub - ffmpegwasm/ffmpeg.wasm: FFmpeg for browser, powered by WebAssembly · GitHub

You signed in with another tab or window.

You switched accounts on another tab or window.

You must be signed in to change notification settings

ffmpeg.wasm is a pure Webassembly / Javascript port of FFmpeg. It enables video & audio record, convert and stream right inside browsers.

Please sponsor ffmpeg.wasm to make it sustainable. ❤️

FFmpeg for browser, powered by WebAssembly

You can’t perform that action at this time.

---

## GitHub - Vanilagy/mp4-muxer: MP4 multiplexer in pure TypeScript with support for WebCodecs API, video & audio. · GitHub

`https://github.com/Vanilagy/mp4-muxer`

GitHub - Vanilagy/mp4-muxer: MP4 multiplexer in pure TypeScript with support for WebCodecs API, video & audio. · GitHub

You signed in with another tab or window.

You switched accounts on another tab or window.

You must be signed in to change notification settings

mp4-muxer has been deprecated in favor of

, which entirely supersedes it. Mediabunny ships with an even better, easier-to-use, faster and more feature-rich MP4 multiplexer, as well as muxers for many other formats, demuxers, WebCodecs abstractions and more, while keeping the bundle size tiny thanks to a tree-shakable design.

mp4-muxer is no longer being maintained and will not receive any new features or bug fixes.

has got you covered. Refer to the following documents to jump right in:

My code already uses mp4-muxer. What should I do?

If you still need the docs for mp4-muxer, you can find them

MP4 multiplexer in pure TypeScript with support for WebCodecs API, video & audio.

You can’t perform that action at this time.

---

## WebCodecs vs ffmpeg.wasm — browser video encoding — BurnSub

`https://www.burnsub.com/blog/webcodecs-vs-ffmpeg-wasm/`

WebCodecs vs ffmpeg.wasm — browser video encoding — BurnSub

If you want to process a video in a browser without uploading it to a server, you have exactly two real options in 2026:

. They look superficially similar — both run in the browser, both handle MP4. They are fundamentally different technologies with different performance profiles, different scope, and different use cases.

This post is a technical breakdown of how each works, where each is the right tool, and why a narrow-scope tool like BurnSub fits the WebCodecs model.

is the FFmpeg C codebase compiled to WebAssembly. When you call it from JavaScript, you are running the full FFmpeg binary inside a WebAssembly virtual machine. The video frames, the encoder, the decoder, the muxer — all of it lives inside the JS engine’s WebAssembly sandbox.

. Every filter, every codec, every container, every quirk of 25 years of FFmpeg development. If you can write an

command line for your job, ffmpeg.wasm can run it in the browser.

The cost is the execution model. WebAssembly is not direct hardware access. Every operation — decoding a frame, applying a filter, encoding a frame — happens in software inside the WASM runtime. Modern CPUs have dedicated silicon for H.264 and H.265 encoding (Intel Quick Sync, AMD VCE, Apple VideoToolbox). ffmpeg.wasm cannot use any of it. WebAssembly is sandboxed and cannot reach the underlying hardware encoders.

The result is that ffmpeg.wasm is substantially slower than running the same FFmpeg binary natively. The ffmpeg.wasm project’s own

acknowledges the constraint, and benchmarks across the community consistently show software encoding running roughly an order of magnitude slower than hardware-accelerated paths on the same machine. The exact gap depends on the codec, the resolution, and the host CPU.

For short clips that gap is bearable. For a longer recording at 4K, it becomes the dominant cost of the operation.

hardware-accelerated video encoders and decoders to JavaScript. It is not a virtual machine. It is a direct binding to the same encoder Chrome uses to play YouTube and the same decoder Safari uses to display a Twitter video.

is the line that matters. The browser checks your GPU, your OS, and your driver, then routes the work to whatever hardware path is fastest. On a laptop with Intel Quick Sync, the encoder runs on dedicated silicon. On an M-series Mac, it goes through VideoToolbox. On Android, it uses MediaCodec. The JavaScript API surface is identical across platforms; only the underlying acceleration changes.

. No filters. No subtitle muxing. No format conversion magic. You get encoding, decoding, and the raw bytes between them. Everything else — drawing subtitles on a frame, muxing into MP4, syncing audio — you build yourself in JavaScript.

This is exactly the trade-off a subtitle burner needs. The job is narrow. The narrow API fits.

I will not invent benchmark numbers. Here is what is widely accepted in the public record:

(Quick Sync / VCE / VideoToolbox) typically encodes 1080p H.264 at hundreds of frames per second on a desktop GPU, per the FFmpeg documentation and broad community benchmarks.

uses the same underlying hardware paths. Throughput on the same machine is in the same order of magnitude as native FFmpeg, with overhead in the binding layer rather than the encoding itself.

has been benchmarked by the community to run roughly an order of magnitude slower than the same FFmpeg binary natively, because of the WebAssembly software-encoding constraint.

for the burn-subtitles workload, WebCodecs is fast enough that the encode step is no longer the bottleneck

— follows from those three facts. On a modern machine, the slow step is no longer “encode the frames”; it is “draw the captions” and “wait for I/O on the input.”

Anyone running these tools today can measure the difference themselves. The community benchmarks are public, and individual users can validate them with a short script and a test clip. The hedged statement above is conservative; specific milliseconds depend on your machine and your codec settings.

This is how a WebCodecs-based subtitle burner like BurnSub processes a video, end to end, in the browser. Every step uses standard APIs documented at MDN.

The browser parses the MP4 container and extracts the encoded video and audio tracks. There are several JavaScript libraries for this job —

is the most established. The output is a stream of

objects (the encoded H.264 NAL units) plus an audio track.

is a raw bitmap that lives in GPU memory by default. You can draw it to a canvas or read it back to CPU memory. Drawing to canvas is dramatically faster because the data never leaves the GPU.

Looks up which subtitle cue is active at this frame’s timestamp.

Renders the cue using the chosen style (font, color, stroke, animation, position) via canvas text drawing.

Captures the composited canvas as the input for the next step.

The canvas drawing step is where caption styling lives. In BurnSub’s case, every preset is a JSON configuration that maps to canvas drawing instructions. The rendering itself is plain

, and similar calls — well-documented Canvas 2D API, no exotic technology.

consumes the composited frame and emits a new

({ output: handleChunk, error: console.error });

This is the step where WebCodecs earns its keep. The encode runs on hardware. For 1080p H.264 it is typically real-time or faster on a modern machine — a 60-second clip is in the same ballpark as 30–60 seconds of total encode time, depending on hardware and bitrate.

The encoded chunks need to be wrapped back into an MP4 container with the audio track. Open-source JavaScript muxers exist for this — the

project is one well-maintained option. The output is a

plus an anchor click. The user gets the MP4. The file never left the browser, which is verifiable in the DevTools network tab.

That is the entire pipeline. Six steps, all using documented browser APIs, all hardware-accelerated where possible, all running on the user’s machine.

Pretending WebCodecs is universally better than ffmpeg.wasm would be dishonest. The trade-offs are real.

WebCodecs guarantees H.264 and VP9 in modern browsers. AV1 encoding support is patchy. HEVC encoding is essentially unavailable outside Safari. ffmpeg.wasm can do all of these because it carries its own codec implementations as part of the WASM bundle.

, no built-in subtitle filter. If you want to scale a video, you do it yourself by drawing to a smaller canvas. If you want to apply a color filter, you write the shader yourself or use canvas operations.

Firefox 147+ (added the encoder relatively late in the cycle)

Older browsers cannot encode. ffmpeg.wasm works on any browser with WebAssembly, which is essentially every browser shipped since 2017.

but the API treats audio and video as parallel, symmetric tracks. You manage the audio separately and mux it manually. ffmpeg.wasm handles audio transparently within an

Both demuxing (parsing the input MP4) and muxing (writing the output MP4) are

the WebCodecs API. You bring your own parser and muxer. ffmpeg.wasm includes muxers for every container FFmpeg supports.

narrow, fast, hardware-accelerated codec API

. If your job fits the narrow API, WebCodecs wins on speed and architecture. If you need filters, exotic codecs, or older-browser support, ffmpeg.wasm wins on capability.

Why a subtitle burner fits the narrow path

A subtitle burner is the canonical case for WebCodecs. The job has exactly two pipeline stages that are codec-heavy: decode the input, encode the output. Everything between — drawing the caption — is plain canvas work, which is fast in any browser.

There is no need for color grading, no need for de-noising, no need for resampling beyond what canvas already does. The “filter graph” is a single text overlay.

The instinct for someone new to browser video processing is to reach for ffmpeg.wasm first, because FFmpeg is the universal video toolkit. For a narrow-scope tool, that instinct produces a slower tool than necessary. The correct question is not “how do I make ffmpeg.wasm fast enough?” but “do I actually need everything FFmpeg provides?”

For a subtitle burner, the answer is no. For a full video editor with color grading and B-roll, the answer is probably yes.

If your tool has any of these properties, use ffmpeg.wasm:

It needs to do color filtering, sharpening, scaling, frame-rate conversion, or any of FFmpeg’s filter operations.

It needs to support browsers older than Chrome 94 / Safari 17.

It needs to work with exotic codecs (HEVC, AV1 in older Chrome, ProRes, DNxHD).

The pipeline involves multiple stages that FFmpeg already chains together natively.

If your tool is closer to a narrow, single-purpose profile, use WebCodecs:

One codec-heavy operation per frame (encode or decode), with non-codec work in between.

Sub-second latency targets where the WASM overhead would hurt.

A clear willingness to write your own demuxer and muxer.

Both are real options. Both are production-ready in 2026. They are not enemies — they are different solutions to different sub-problems of the same broader problem of browser-local video processing.

The thing that will make this trade-off less stark is

. WebGPU gives direct shader access for video processing on the GPU, with much better performance than canvas drawing. It already runs the Whisper speech-recognition model that tools like BurnSub use for auto-captioning, via

A future version of the BurnSub pipeline will likely move the caption rendering step into a WebGPU shader. The encode and decode stay on WebCodecs. The shader handles the per-frame compositing work. That is the path to truly real-time processing, including for 4K content.

For anyone building or evaluating browser-local video processing:

mp4-muxer — JavaScript MP4 muxer for WebCodecs output

transformers.js — run ML models in the browser

The architecture choice between WebCodecs and ffmpeg.wasm is one of the more consequential decisions in browser-local video work. The right answer depends on what your tool needs to do, not on which API is more popular at the moment. For narrow tools, WebCodecs is the better fit. For everything else, ffmpeg.wasm remains the default.

---

## WebCodecs API - Web APIs | MDN

`https://developer.mozilla.org/en-US/docs/Web/API/WebCodecs_API`

enables web developers to encode and decode video and audio in the browser efficiently (using hardware acceleration) and with very low-level control (processing on a per-frame basis).

It is useful for web applications that do heavy media processing, or which require low-level control over the way media is encoded.

This includes browser-based video and audio editing, as well as live-streaming and video conferencing.

The WebCodecs API provides browser-native interfaces to represent raw video frames, encoded video frames, as well as raw and encoded audio.

Likewise, the WebCodecs API also introduces the

Generally there is a 1:1 correspondence between the raw and encoded versions of each media type. Decoding a number of

objects (and this is also true for audio).

represents a video frame, and is tied to actual pixel data on the device's graphics memory, as well as metadata such as the timestamp and duration (in microseconds), format and resolution. A

can be constructed from any image source, and can also be rendered to a

using any of the canvas rendering methods.

represents the encoded (compressed) version of the same frame, tied to binary data in regular memory and the same metadata.

The only difference is that it has one additional field:

, which can be "key" or "delta", representing whether or not it corresponds to a

typically stores 10 to 100 times less data than its corresponding raw

object represents a number of individual audio samples (1024 is a typical number). Audio sample data can be extracted as a

method. There is no direct integration with the

represents the encoded (compressed) version of an

object, containing compressed audio sample data.

. Each instance of an encoder or decoder maintains an internal, independent processing queue. When queueing a substantial number of encoded chunks for decoding or frames/samples for encoding, it's important to keep this model in mind.

operate asynchronously by appending control messages to the end of the queue, while methods named

synchronously abort all pending work and purge the processing queue. After

, more work may be queued following a call to

is a permanent operation. These methods work for both Audio and Video decoders/encoders.

method can be used to wait for the completion of all work that was pending at the time

was called. However, it should generally only be called once all desired work is queued â it is not intended to force progress at regular intervals. Calling it unnecessarily will affect encoder quality and cause decoders to require the next input to be a key frame.

A codec is a specific algorithm for encoding (compressing) and decoding (decompressing) video and audio. There are several industry standard codecs for video, and a separate set of codecs for audio. Here are the major ones supported by the WebCodecs API:

The most widely supported video codec. Most MP4 files use H.264.

Open source, developed by Google. Better compression than H.264. Commonly used on YouTube and in WebM files.

The newest open source codec, with better compression than VP9. Broad decoder support; hardware encoder support is still limited.

Better compression than H.264, but with significant gaps in browser support outside of Apple platforms.

Open source, low-latency. The recommended choice for most WebCodecs audio encoding.

Broadly supported for decoding, but not available as an encoder in WebCodecs.

Uncompressed audio. No quality loss, but large file sizes.

The WebCodecs specification supports a particular set of codecs, and individual devices and browsers may only support a subset of those. Encoders and decoders must be configured with fully specified codec strings (such as

for H.264) instead of ambiguous codec names like

provides guidance on choosing an appropriate codec string (see the

(webcodecsfundamentals.org) for a complete list of codec strings and their browser support).

The WebCodecs API only deals with encoding and decoding, with encoded chunks just representing binary data. It does not provide a built-in way to read

objects from a video file, or write them to a playable video file.

Reading encoded chunks from a video file is a completely different process called demuxing, and to fetch

objects from a video file, you will need to use a demuxing library such as

These libraries will follow the video container specifications (e.g., webm, mp4) to extract the track data and byte offsets for each encoded chunk, and provide methods for extracting the actual chunks from the raw file.

Likewise, to write to a playable video file, you will need a muxing library, with

being the primary option. Muxing libraries handle formatting the binary encoded data, and placing it in the correct byte position in the output file stream according to the container specification, so that the output video is playable.

You can find more information on muxing and demuxing in the

A brief primer on video processing, covering codecs and containers, muxing and demuxing, and conceptual information that explains how the WebCodecs API implements these concepts.

In depth guide to how to actually use the WebCodecs API, including how to instantiate and configure encoders and decoders, how to create and consume video frames, and how to extract samples from

The WebCodecs API requires codec strings â precise identifiers that specify not just the codec family but also the profile, level, and other parameters. This guide explains how codec strings work and how to choose the right codec for common use cases.

Represents codec-specific encoded audio bytes.

Represents codec-specific encoded video bytes.

Represents a frame of unencoded video data.

Represents the color space of a video frame.

Unpacks and decodes image data, giving access to the sequence of frames in an animated image.

Represents the list of tracks available in the image.

, we pass an object that specifies a callback function that will be called when

instances are available for processing, and an error function that will be called if there are errors.

// Do something with chunk, typically send to muxing library

You then need to configure the encoder with the codec parameter and various other fields.

codec: "vp09.00.40.08.00", // See codec selection guide

You can then start encoding frames to the encoder. You can construct a

const frame = new VideoFrame(canvas, { timestamp: (i * 1e6) / 30 }); // 30 fps, in microseconds

encoder.encode(frame, { keyFrame: i % 60 === 0 });

Real-Time Video Processing with WebCodecs and Streams: Processing Pipelines

Video Frame Processing on the Web â WebAssembly, WebGPU, WebGL, WebCodecs, WebNN, and WebTransport

---

## ⚠️ Paginas que NAO deram texto

- `https://caniuse.com/webcodecs` — bloqueada ou vazia
- `https://caniuse.com/sharedarraybuffer` — bloqueada ou vazia
- `https://caniuse.com/mdn-api_mediarecorder` — bloqueada ou vazia
