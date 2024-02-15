function addRemoveToCart(pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const url = `/product/api/${pk}/`;

    const requestData = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({})
    };

    // ارسال درخواست POST به سرور
    fetch(url, requestData)
        .then(response => {
            if (response.status == 201) {
                console.log('item add to cookies successfully');
            } else if (response.status == 400) {
                alert('این محصول دیگه بیشتر از این موجود نیست');
            } else {
                console.error('ERROR in POST:', response.statusText);
            }
        })
        .catch(error => {
            console.error('ERROR:', error);
        });
}

function removeFromCart(pk) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    const url = `/product/api/${pk}/`;

    const requestData = {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({})
    };

    fetch(url, requestData)
        .then(response => {
            if (response.status == 204) {
                console.log('item remove from cookies successfully');
            } else if (response.status == 500) {
                alert('مقدار سفارشی صفر است!!');
            } else {
                console.error('ERROR in DELETE:', response.statusText);
            }
        })

}
