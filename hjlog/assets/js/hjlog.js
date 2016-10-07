import figureExtension from "./figure"
import latexExtension from "./latex"
import asyncPhotoUpload from "./photoAjax"

require('../css/hjlog.scss');
require('script!showdown');
require('script!katex/dist/katex.min.js');
require('script!./highlight');


// Markdown rendering
const postBody = document.getElementsByClassName("markdown")[0];
if (postBody) {
  latexExtension(showdown);
  figureExtension(showdown);
  const md = postBody.innerText;
  const converter = new showdown.Converter({
    'extensions': ['figure', 'latex'],
    'strikethrough': true,
    'tables': true,
    'noHeaderId': true,
    'literalMidWordUnderscores': true,
    'simplifiedAutoLink': true});

  postBody.innerHTML = converter.makeHtml(md);
  postBody.style.display = "block";

  const dimmer = document.getElementsByClassName("dimmer")[0];
  dimmer.style.display = "none";

  const latex = document.getElementsByClassName("latex")
  for (let l of latex) {
    katex.render(l.innerHTML, l);
  }

  const latexDisplay = document.getElementsByClassName("latex-display")
  for (let ld of latexDisplay) {
    katex.render(ld.innerHTML, ld, {displayMode: true});
  }
}

// Syntax highlighting
hljs.initHighlightingOnLoad();

// Responsive navbar
const trigger = document.getElementsByClassName('trigger')[0];
trigger.addEventListener("click", () => {
  const nav = document.getElementsByTagName('nav')[0];

  if (nav.style.visibility === 'visible') {
    nav.style.visibility = 'hidden';
  }
  else {
    nav.style.visibility = 'visible';
  }
});

// Photo Upload
const photoUploadForm = document.getElementById("photoupload");

if (photoUploadForm) {
  photoUploadForm.addEventListener("change", asyncPhotoUpload);
}

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-73895875-1', 'auto');
ga('send', 'pageview');
