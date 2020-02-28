// $(document).ready(function(){
//     $('form').on('submit', function(event) {
//         $.ajax({
//             data : {
//                 user_input : $('#ask-area').val()
//             },
//             type : 'POST', 
//             url : '/'
//         })
//         .done(function(data) {
//             $('#user-question').text(data.user_input).show();
//         });
//         event.preventDefault();
//     });
// })
$(document).ready(function(){

    $('form').on('submit', function(e){
        e.preventDefault();
        const user_input = $('#ask-area').val()
        // return if the user does not enter any text
        if (!user_input) {
        return
        }

        $('#scroll-dialogue').append(`
            <p id="margin-ask-user"><span id="user-question"></span>
                ${user_input}
            </p>
        `);

        // clear the text input 
        $('#ask-area').val('')

        // send the message
        submit_message(user_input)
    })});