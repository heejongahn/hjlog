(function( $ ){

  $.fn.fitText = function( kompressor, options ) {

    // Setup options
    var compressor = kompressor || 1,
        settings = $.extend({
          'minFontSize' : Number.NEGATIVE_INFINITY,
          'maxFontSize' : Number.POSITIVE_INFINITY
        }, options);

    return this.each(function(){

      // Store the object
      var $this = $(this);

      // Resizer() resizes items based on the object width divided by the compressor * 10
      var resizer = function () {
        $this.css('font-size', Math.max(Math.min($this.width() / (compressor*10), parseFloat(settings.maxFontSize)), parseFloat(settings.minFontSize)));
      };

      // Call once to set.
      resizer();

      // Call on resize. Opera debounces their resize by default.
      $(window).on('resize.fittext orientationchange.fittext', resizer);

    });

  };

})( jQuery );

(function() {
  today = new Date();
  count = new Date("May 8,2015 00:00:00"); // D-Day
  calc = Math.ceil((count - today) / 1000 / 24 / 60 / 60);
  console.log(calc);
  if (calc < 0) calc = -1 * calc;
  result = '<span class="fit" id="dday"><span id="dplus">D+</span>'+ calc + '</span>';
  document.write(result, "");

   jQuery(".fit").fitText();
})();
