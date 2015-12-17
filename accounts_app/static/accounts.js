/*
    separate defining the initialize function from the part where its
    exported into the Superlists_Project namespace.
    Do a console.log, which like JavaScript debug-print, to look at
     what the initialize function is being called with.
*/
var initialize = function (navigator, user, token, urls) {
    $('#id_login').on('click', function () {
        navigator.id.request();
    });
    // $('#id_logout').on('click', function() {
    //     navigator.id.logout();
    // });

    navigator.id.watch({
      /*
        the watch function needs to know a couple of things from the
        global scope.

        current user’s email, to be passed in as the loggedInUser
         parameter to watch
        current CSRF token, to pass in the Ajax POST request to the
         login view
      */
      loggedInUser: user,
      onlogin: function(assertion) {
        $.post(
          urls.login,
          { assertion: assertion, csrfmiddlewaretoken: token }
        )
          .done(function () { window.location.reload(); })
          .fail(function () { navigator.id.logout(); });
      },
      onlogout: function () {}
      // onlogout: function () {
      //     $.post(
      //       urls.logout,
      //       { csrfmiddlewaretoken: token}
      //     )
      //       .done(function () { window.location.reload(); })
      //       .fail(function () { navigator.id.logout(); });
      // } // onlogout
    }); // navigator.id.watch
};

window.Superlists_Project = {
    Accounts_App: {
        initialize: initialize
    }
};