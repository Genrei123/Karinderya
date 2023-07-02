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
    $email = $_POST['email'];
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];

    // Check if email is already taken
    $email_check_query = "SELECT * FROM accounts WHERE email = '$email'";
    $result = mysqli_query($conn, $email_check_query);

    // Check if the password and confirm password are the same
    if ($password != $confirm_password)
    {
        array_push($errors, "Password is not the same");
        header('location: ../php/register.php');
    }

    else if (mysqli_num_rows($result) > 0)
    {
        array_push($errors, "Email is already taken");
        header('location: ../php/register.php');
    }

    else
    {
        // Insert data to database
        // Much more safer way to insert data to database
        $stmt = $conn->prepare("INSERT INTO accounts (username, email, password) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $username, $email, $password);
        $stmt->execute();

        // Redirect to login page
        header('location: ../html/index.html');
        exit();
    }
}




?>