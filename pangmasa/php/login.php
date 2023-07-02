<?php 

session_start();

$errors = array();

if (isset($_POST['submit']))
{
    // Connect to database
    $conn = mysqli_connect('localhost', 'root', '', 'karenderya');

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Initialize variables
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Check if email is already taken
    $query = "SELECT * FROM accounts WHERE username = '$username' AND password = '$password'";
    $result = mysqli_query($conn, $query);

    if (mysqli_num_rows($result) > 0)
    {
        // Redirect to login page
        header('location: ../html/index.html');
        exit();
    }

    else
    {
        array_push($errors, "Username or password is incorrect");
        header('location: ../php/login.php');
        exit();
    }
}




?>