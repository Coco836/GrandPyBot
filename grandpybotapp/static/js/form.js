$(document).ready(function(){
    $('form').on('submit', function(event) {
        $.ajax({
            data : {
                user_input : $('#ask-area').val()
            },
            type : 'POST', 
            url : '/'
        })
        
        .done(function(data) {
            if (!data.user_input) {
                return
            }

            else if (data.address_story) {
                $('#scroll-dialogue').append(`
                    <div>
                        <p class="margin-ask-user"><span class="user-question"> ${data.user_input} </span></p>
                        <p class="margin-response"><span class="response"> ${data.message} </span></p>
                        <div class="map"></div>
                        <p class="margin-story"><span class="story"> ${data.address_story} <a href="${data.wiki_page_url}" target="blank" class="url-wiki"> ${data.wiki_page_url} </a></span></p>
                        <p class="margin-end-quote"><span class="end-quote"> ${data.end_quote} </span></p>
                    </div>
                `);
                initMap(data);
                $('#ask-area').val('');
            }

            else {
                $('#scroll-dialogue').append(`
                    <div>               
                        <p class="margin-ask-user"><span class="user-question"> ${data.user_input} </span></p>
                        <p class="margin-response"><span class="response"> ${data.message} </span></p>
                    </div>
                `);
                $('#ask-area').val('');

            }
        });
        event.preventDefault();
    });
});

function initMap(data) {
    let location = {lat: data['latitude'], lng: data['longitude']};
    let map = new google.maps.Map($("#scroll-dialogue").find(".map").last().get(0), {
        zoom: 10, 
        center: location
    });
    let marker = new google.maps.Marker({
        position: location, 
        map: map
    });
}
