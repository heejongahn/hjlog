import figureExtension from "./figure"

require('../css/hjlog.scss');
require('script!showdown');
require('script!jquery');
require('script!./highlight');
require('./photoAjax');


// Markdown rendering
const postBody = document.getElementsByClassName("markdown")[0];
if (postBody) {
  figureExtension(showdown);
  const md = $(".markdown").text();
  const converter = new showdown.Converter({
    'extensions': ['figure'],
    'strikethrough': true,
    'tables': true,
    'noHeaderId': true});
  const html = converter.makeHtml(md);

  postBody.innerHTML = converter.makeHtml(md);
  postBody.style.display = "block";

  const dimmer = document.getElementsByClassName("dimmer")[0];
  dimmer.style.display = "none";
}

// Syntax highlighting
hljs.initHighlightingOnLoad();

// Responsive navbar
const trigger = document.getElementsByClassName('trigger')[0];
trigger.addEventListener("click", () => {
  const nav = document.getElementsByTagName('nav')[0];

  if (nav.style.display === 'block') {
    nav.style.display = 'none';
  }
  else {
    nav.style.display = 'block';
  }
});
