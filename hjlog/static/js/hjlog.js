$(document).ready(function() {
  // Markdown rendering
  var md = $(".markdown.postbody").text();
  var converter = new showdown.Converter({
    'strikethrough': true,
    'tables': true,
    'noHeaderId': true});
  var html = converter.makeHtml(md);
  $(".markdown.postbody").html(html);
  $(".markdown.postbody").show();
  $(".dimmer").hide();

  // Syntax highlighting
  hljs.initHighlightingOnLoad();

  var trigger = document.getElementById('trigger');

  trigger.onclick = navToggle;
  });

var navToggle = function() {
  var nav = document.getElementsByTagName('nav')[0];

  if (nav.style.display === 'block') { nav.style.display = 'none'; }
  else { nav.style.display = 'block'; }
}
