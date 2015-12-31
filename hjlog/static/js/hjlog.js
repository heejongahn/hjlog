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
  });
