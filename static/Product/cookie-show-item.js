function getItemCartCookie() {
    const cookies = document.cookie.split('; ')
    for (const cookie of cookies){
        const [name, value] = cookie.split('=')
        if  (name == "item_cart"){
            const keyValuePairs = value.split(';')
            const cartValue = {};
            for (const pair of keyValuePairs) {
                const [key, val] = pair.split('=')
                cartValue[key] = val;

            }
            return cartValue

        }

    }
}

function sendToServer() {
    var xhr = new XMLHttpRequest();
    var cookieItem = getItemCartCookie()

    xhr.open("POST", "http://127.0.0.1:8000/product-list/api/", true);
    xhr.setRequestHeader('Content-Type', 'application/json')
    xhr.send(cookieItem)
}


sendToServer()