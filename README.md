# WebVN - Pure CSS+HTML5 Visual Novels

WebVN is a format and processor for building visual novels using pure HTML and CSS for modern browsers. WebVN is focused on mostly-linear stories with minimal user interaction. This is a work-in-progress and its featureset is tailored specifically for the upcoming Megatokyo: Endgames omake.

In its current form, WebVN supports:
- Linear storylines
- Up to three on-screen characters
- Music with simple cues
- Visual transitions (fades)
- Flexible styling for dialogue

## How does it work?

WebVN reads in a simple script format inspired by the one used by Renpy. It outputs a series of HTML documents describing scenes based on audio cues. Each scene contains multiple frames for each text event and character pose change. Frame nvigation is bound to hidden HTML `<button>` elements allowing for navigation to arbitrary points in the story. CSS effects ensure the correct frame is displayed and provide transitions and animations.

## What browsers does it work with?

Full support has been verified on Firefox 38, Chrome 42, Internet Explorer, Safari, and Firefox for Android. The CSS and HTML elements used for WebVN output have been supported by browsers for several years, but support for older browsers is not guaranteed.

Music does not work properly on iOS due to platform limitations. Javascript intervention can be used to correct this.
