/* Verifies passwords match before submitting form */
// https://stackoverflow.com/questions/58150828/how-can-i-verify-form-passwords-match-using-javascript //

function verifyPassword () {
    let password1 = document.getElementById('password1').value
    let password2 = document.getElementById('password2').value
    let match = true;

    if (password1 != password2) {
        alert('Password does not match');
        match = false; 
    }

    else {
        alert('Password match');
    }

    return match;

}

document.getElementById('register').onsubmit = verifyPassword;