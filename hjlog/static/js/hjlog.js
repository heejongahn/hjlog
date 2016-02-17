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

  var trigger = document.getElementsByClassName('trigger')[0];

  trigger.onclick = navToggle;
  });

var navToggle = function() {
  var nav = document.getElementsByTagName('nav')[0];

  if (nav.style.display === 'block') {
    nav.style.display = 'none';
  }
  else {
    nav.style.display = 'block';
  }
}

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

ga('create', 'UA-73895875-1', 'auto');
ga('send', 'pageview');
