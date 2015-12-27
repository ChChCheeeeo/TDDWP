jQuery(document).ready(function ($) {
    /*
        find all the input elements, and for each of them, attach an even
         listener which reacts on keypress events. The event listener is
          the inline function, which hides all elements that have the class
           .has-error.
    */
    $('input').on('keypress', function () {
       $('.has-error').hide();
    });
});