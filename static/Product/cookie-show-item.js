// Function to get the value of the "item_cart" cookie
function getItemCartCookie() {
    var cookies = document.cookie; // Get the cookie string
    var cookieArray = cookies.split(';'); // Split the string into an array of individual cookies

    var itemCartValue = null; // Initialize variable to store the value of the "item_cart" cookie

    // Loop through the array of cookies
    cookieArray.forEach(function (cookie) {
        var parts = cookie.split('='); // Split each cookie into its name and value
        var name = parts[0].trim(); // Get the name of the cookie and remove leading/trailing whitespace

        // Check if the cookie is "item_cart"
        if (name === 'item_cart') {
            itemCartValue = parts[1]; // Get the value of the "item_cart" cookie
        }
    });

    return itemCartValue; // Return the value of the "item_cart" cookie
}

function readCookie() {
    const csrftoken = document.qurySelector('[name=csrfmiddlewaretoken]').value;

    const itemCartValue = getItemCartCookie();

    const url = '/product-list/api/'

    const requestData = {
        mehod : 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JOSN.stringify({})
    };
    fetch(url, requestData).then(response => {
        if (response.status == 200) {
            console.log('item add to cookies successfully');
            itemCartValue.forEach(
                (item) => {
                    console.log(item);
                }
            )
        }
    })
}