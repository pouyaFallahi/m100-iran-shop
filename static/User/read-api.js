function getDataUser(user_id) {
    console.log("start");
    const url = `http://127.0.0.1:8000/api/user/panel/${user_id}`
    const csrftoken = CrfTokenRead()
    const requestData = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken

        }
    };
    inputEmail.style.display = "";
    inputAddress.style.display = "";
    inputPhoneNumber.style.display = "";
    inputUserName.style.display = "";
    btnSave.style.display = "";

    document.getElementById("btnEditProfile").style.display = "none";
    $.getJSON(url, function (data) {
        console.log(data)
    })
}

function CrfTokenRead() {
    const cookies = document.cookie.split('; ')
    for (const cookie of cookies) {
        const [name, value] = cookie.split('=')
        if (name == "csrftoken") {
            const keyValuePairs = value.split(';')
            var cartValue = '';
            for (const pair of keyValuePairs) {
                const [key, val] = pair.split('=')
                cartValue = key;

            }
            return cartValue;
        }
    }
}

function saveForm(user_id) {
    const url = `http://127.0.0.1:8000/api/user/panel/${user_id}/`
    const data = {
        'userName': inputUserName.value,
        'email': inputEmail.value,
        'address': inputAddress.value,
        'phoneNumber': inputPhoneNumber
    }
    let xhr = new XMLHttpRequest();
    const csrftoken = CrfTokenRead()
    const requestData = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    }
    fetch(url, requestData)
        .then((response)=> {
            return response.json();
        })
        .then((data) => {
    console.log('Response:', data); // Handle the response data
  })
}

const inputEmail = document.getElementById('inputEmail')
const inputUserName = document.getElementById('inputUserName')
const inputAddress = document.getElementById('inputAddress')
const inputPhoneNumber = document.getElementById('inputPhoneNumber')
const btnSave = document.getElementById('btnSave')
inputEmail.style.display = "none";
btnSave.style.display = "none";
inputUserName.style.display = "none";
inputAddress.style.display = "none";
inputPhoneNumber.style.display = "none";

