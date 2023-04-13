document.addEventListener("DOMContentLoaded", () => {

    // generate form

    // fetch available players
    localStorage.removeItem("availablePlayers");
    
    // fetch available positions
    localStorage.removeItem("availablePositions");
  
})


function generatePositionSelection(id){
    // Thanks: https://stackoverflow.com/questions/68223406/how-to-create-select-dropdown-in-javascript-with-fetched-data-from-api
    
    const select_tag = document.querySelector(`#${id}`);
    
    // to prevent repeated creation of displayPositionOptions
    var current_options = select_tag.children;
    var array_current_options = Array.from(current_options);
    var available_options = [];
    array_current_options.forEach(e => {
        if (e.value !== "") {
            available_options.push(e.value)
        }
    })

    const getPositions = async() => {
        const data = await fetch("api/database/positions")
        .then(response => response.json())
        .then(data => {
            localStorage.setItem("availablePositions", JSON.stringify(data));
            return data
        })
        return data
    }

    const displayPositionOptions = async () => {
        // check localStorage
        if (localStorage.getItem("availablePositions") === null) {
            var options = await getPositions();
        } else {
            var options = JSON.parse(localStorage.getItem("availablePositions"));
        }
        options.forEach(position => {
            if (available_options.includes(position) === false) {
                const position_option = document.createElement('option');
                position_option.value = `${position}`;
                position_option.innerHTML = `${position}`;
                select_tag.appendChild(position_option);
            }
        })
    }

    displayPositionOptions();
}


function generatePlayerSelection(id){
    const select_tag = document.querySelector(`#${id}`);

    // to prevent repeated creation of displayPlayerOptions
    var current_options = select_tag.children;
    var array_current_options = Array.from(current_options);
    var available_options = [];
    array_current_options.forEach(e => {
        if (e.value !== "") {
            available_options.push(e.value)
        }
    })

    const getPlayers = async() => {
        const data = await fetch("api/database/players")
        .then(response => response.json())
        .then(data => {
            localStorage.setItem("availablePlayers", JSON.stringify(data))
            return data
        })
        return data
    }

    const displayPlayerOptions = async () => {
        // check localStorage
        if (localStorage.getItem("availablePlayers") === null) {
            var players = await getPlayers();
        } else {
            var players = JSON.parse(localStorage.getItem("availablePlayers"));
        }
        players.forEach(player => {
            if (available_options.includes(player) === false) {
                const player_option = document.createElement('option');
                player_option.value = `${player}`;
                player_option.innerHTML = `${player.replace('-', ' ')}`;
                select_tag.appendChild(player_option);
            }
        })
    }

    displayPlayerOptions();
}


function generateOptions(team){
    // grab the container of the team
    // for i=1 to 11 generate HTML for row of player-position inputs and then append
}


// https://stackoverflow.com/questions/1085801/get-selected-value-in-dropdown-list-using-javascript
// https://stackoverflow.com/questions/8664486/javascript-code-to-stop-form-submission
// https://www.w3schools.com/jsref/event_onsubmit.asp
// https://github.com/rinogrego/CS50-W/blob/main/4%20-%20Mail/mail/mail/static/mail/inbox1.js
// https://github.com/rinogrego/CS50-W/blob/main/4%20-%20Mail/mail/mail/views.py
// https://stackoverflow.com/questions/37487826/send-form-data-to-javascript-on-submit
// https://stackoverflow.com/questions/69861420/how-to-pass-a-json-data-from-react-to-django-using-post-request
// https://stackoverflow.com/questions/66528371/sending-post-data-from-react-to-django-rest-framework-showing-415-error
// https://stackoverflow.com/questions/53123092/how-to-send-post-request-to-django-api-from-reactjs-web-app
getPrediction = async (event) => {
    event.preventDefault();
    alert("get Prediction test");
    const data = {
        "home_player_01": document.getElementById("home-player-01").value,
        "home_player_01_position": document.getElementById("home-player-01-position").value,
        "home_player_02": document.getElementById("home-player-02").value,
        "home_player_02_position": document.getElementById("home-player-02-position").value,
        "home_player_03": document.getElementById("home-player-03").value,
        "home_player_03_position": document.getElementById("home-player-03-position").value,
        "home_player_04": document.getElementById("home-player-04").value,
        "home_player_04_position": document.getElementById("home-player-04-position").value,
        "home_player_05": document.getElementById("home-player-05").value,
        "home_player_05_position": document.getElementById("home-player-05-position").value,
        "home_player_06": document.getElementById("home-player-06").value,
        "home_player_06_position": document.getElementById("home-player-06-position").value,
        "home_player_07": document.getElementById("home-player-07").value,
        "home_player_07_position": document.getElementById("home-player-07-position").value,
        "home_player_08": document.getElementById("home-player-08").value,
        "home_player_08_position": document.getElementById("home-player-08-position").value,
        "home_player_09": document.getElementById("home-player-09").value,
        "home_player_09_position": document.getElementById("home-player-09-position").value,
        "home_player_10": document.getElementById("home-player-10").value,
        "home_player_10_position": document.getElementById("home-player-10-position").value,
        "home_player_11": document.getElementById("home-player-11").value,
        "home_player_11_position": document.getElementById("home-player-11-position").value,
        
        "away_player_01": document.getElementById("away-player-01").value,
        "away_player_01_position": document.getElementById("away-player-01-position").value,
        "away_player_02": document.getElementById("away-player-02").value,
        "away_player_02_position": document.getElementById("away-player-02-position").value,
        "away_player_03": document.getElementById("away-player-03").value,
        "away_player_03_position": document.getElementById("away-player-03-position").value,
        "away_player_04": document.getElementById("away-player-04").value,
        "away_player_04_position": document.getElementById("away-player-04-position").value,
        "away_player_05": document.getElementById("away-player-05").value,
        "away_player_05_position": document.getElementById("away-player-05-position").value,
        "away_player_06": document.getElementById("away-player-06").value,
        "away_player_06_position": document.getElementById("away-player-06-position").value,
        "away_player_07": document.getElementById("away-player-07").value,
        "away_player_07_position": document.getElementById("away-player-07-position").value,
        "away_player_08": document.getElementById("away-player-08").value,
        "away_player_08_position": document.getElementById("away-player-08-position").value,
        "away_player_09": document.getElementById("away-player-09").value,
        "away_player_09_position": document.getElementById("away-player-09-position").value,
        "away_player_10": document.getElementById("away-player-10").value,
        "away_player_10_position": document.getElementById("away-player-10-position").value,
        "away_player_11": document.getElementById("away-player-11").value,
        "away_player_11_position": document.getElementById("away-player-11-position").value
    }

    var form_data = FormData();
    form_data.append("home_player_01", document.getElementById("home-player-01").value)
    form_data.append("home_player_01_position", document.getElementById("home-player-01-position").value)
    form_data.append("home_player_02", document.getElementById("home-player-02").value)
    form_data.append("home_player_02_position", document.getElementById("home-player-02-position").value)
    form_data.append("home_player_03", document.getElementById("home-player-03").value)
    form_data.append("home_player_03_position", document.getElementById("home-player-03-position").value)
    form_data.append("home_player_04", document.getElementById("home-player-04").value)
    form_data.append("home_player_04_position", document.getElementById("home-player-04-position").value)
    form_data.append("home_player_05", document.getElementById("home-player-05").value)
    form_data.append("home_player_05_position", document.getElementById("home-player-05-position").value)
    form_data.append("home_player_06", document.getElementById("home-player-06").value)
    form_data.append("home_player_06_position", document.getElementById("home-player-06-position").value)
    form_data.append("home_player_07", document.getElementById("home-player-07").value)
    form_data.append("home_player_07_position", document.getElementById("home-player-07-position").value)
    form_data.append("home_player_08", document.getElementById("home-player-08").value)
    form_data.append("home_player_08_position", document.getElementById("home-player-08-position").value)
    form_data.append("home_player_09", document.getElementById("home-player-09").value)
    form_data.append("home_player_09_position", document.getElementById("home-player-09-position").value)
    form_data.append("home_player_10", document.getElementById("home-player-10").value)
    form_data.append("home_player_10_position", document.getElementById("home-player-10-position").value)
    form_data.append("home_player_11", document.getElementById("home-player-11").value)
    form_data.append("home_player_11_position", document.getElementById("home-player-11-position").value)
    
    form_data.append("away_player_01", document.getElementById("away-player-01").value)
    form_data.append("away_player_01_position", document.getElementById("away-player-01-position").value)
    form_data.append("away_player_02", document.getElementById("away-player-02").value)
    form_data.append("away_player_02_position", document.getElementById("away-player-02-position").value)
    form_data.append("away_player_03", document.getElementById("away-player-03").value)
    form_data.append("away_player_03_position", document.getElementById("away-player-03-position").value)
    form_data.append("away_player_04", document.getElementById("away-player-04").value)
    form_data.append("away_player_04_position", document.getElementById("away-player-04-position").value)
    form_data.append("away_player_05", document.getElementById("away-player-05").value)
    form_data.append("away_player_05_position", document.getElementById("away-player-05-position").value)
    form_data.append("away_player_06", document.getElementById("away-player-06").value)
    form_data.append("away_player_06_position", document.getElementById("away-player-06-position").value)
    form_data.append("away_player_07", document.getElementById("away-player-07").value)
    form_data.append("away_player_07_position", document.getElementById("away-player-07-position").value)
    form_data.append("away_player_08", document.getElementById("away-player-08").value)
    form_data.append("away_player_08_position", document.getElementById("away-player-08-position").value)
    form_data.append("away_player_09", document.getElementById("away-player-09").value)
    form_data.append("away_player_09_position", document.getElementById("away-player-09-position").value)
    form_data.append("away_player_10", document.getElementById("away-player-10").value)
    form_data.append("away_player_10_position", document.getElementById("away-player-10-position").value)
    form_data.append("away_player_11", document.getElementById("away-player-11").value)
    form_data.append("away_player_11_position", document.getElementById("away-player-11-position").value)

    var csrftoken = getCookie("csrftoken");
    alert(csrftoken);
    fetch("/api/predict", {
        method: "POST",
        headers: {
            // 'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            "X-CSRFToken": csrftoken,
        },
        // body: JSON.stringify(data)
        body: form_data
    })
    .then(response => response.json())
    .catch(err => { console.log(error) })
    .then(result => {
        alert("Predict success");
        alert(result);
    })

    // return false;
}

// The following function are copying from 
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
// https://stackoverflow.com/questions/43606056/proper-django-csrf-validation-using-fetch-post-request
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}