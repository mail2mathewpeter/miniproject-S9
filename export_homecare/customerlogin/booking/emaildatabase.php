<?php
session_start();
$id=$_SESSION['caravan'];
$connect = mysqli_connect("localhost", "root", "", "miniprojects6"); 
if(isset($_POST["email1"]) && ($_POST["email2"]))
{
$email = mysqli_real_escape_string($connect, $_POST["email1"]);
$email2 = mysqli_real_escape_string($connect, $_POST["email2"]);

$query = "SELECT * FROM booking WHERE start between '$email' and '$email2' and caravan_id='$id'";
//$query = "SELECT start,end from booking WHERE booking_id='$id'";

$result = mysqli_query($connect, $query);
echo mysqli_num_rows($result);
}
?>