$(document).ready(function() {

    $body = $("body");

    $(document).on({
        //ajaxStart: function() { $body.addClass("loading"); },
        ajaxStop: function() { 
            $body.removeClass("loading"); 
            $( ".res" ).html( "<p>Application Deployed</p>" );
        }
    });
    $('#btnSignUp').click(function() {
         $body.addClass("loading"); 
        setTimeout(func, 4000);
        function func(){
            $.ajax({
                url: '/newapp',
                data: $('form').serialize(),
                type: 'POST',
                success: function(response) {
                    setTimeout(function(){}, 6000);
                    console.log(response);
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    });
});
