<?php
session_start();
$id=$_SESSION['customer'];
$_SESSION['customer']=$id;
$caravan=$_SESSION['caravan'];
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <title>Booking Form HTML Template</title>

    <!-- Google font -->
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet">

    <!-- Bootstrap -->
    <link type="text/css" rel="stylesheet" href="css/bootstrap.min.css" />

    <!-- Custom stlylesheet -->
    <link type="text/css" rel="stylesheet" href="css/style.css" />

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
		  <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
		  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		<![endif]-->

</head>
<link href="vendor/select2/select2.min.css" rel="stylesheet" media="all">
<link href="vendor/datepicker/daterangepicker.css" rel="stylesheet" media="all">
<style>
nav1 {
    background: white;
    width: 100%;
    height: 75px;
    overflow: hidden;

    z-index: 1000;
    position: fixed;
    top: 0;
    left: 0px;
}
</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script>
    <?php 
    	$conn=mysqli_connect("localhost","root","","miniprojects6")or die("Connect failed: %s\n". $conn -> error);
        $query="select start from booking";
       $query1= mysqli_query($conn,$query);
        while($result=mysqli_fetch_array($query1))
        {
            $a=$result['start'];
           
          
 ?>

  var dates = ["<?php echo $a?>"];
  <?php
}
?>
function DisableDates(date) {
    var string = jQuery.datepicker.formatDate('dd-mm-yy', date);
    return [dates.indexOf(string) == -1 ];
}

$(function() {
     $("#email1").datepicker({
         beforeShowDay: DisableDates
         alert("mathew")
     });
});
  </script>
<script>
$(document).ready(function() {
    var mod7 = 0;
    $('#register1').click(function() {
            email2 = document.getElementById("email2").value;

            var email1 = $(this).val();
            email1 = document.getElementById("email1").value;

            if (email1>email2) {
                $('#availability').html('This is not valid date');
            } else {
                $.ajax({
                    url: 'emaildatabase.php',
                    method: "POST",
                    data: {
                        email1: email1,
                        email2: email2
                    },
                    success: function(data) {
                        alert(data);
                        if (data != '0') {

                            //  $('#availability').html('<span class="text-danger">Username Already exist</span>');
                            document.getElementById("availability").innerHTML =
                                "<span class='error'>Already Booked the date</span>";

                            $('#availability').css("color", "red");
                            $('#register').attr("disabled", true);
                            $('#register').css("background", "lightblue");
                            mod7 = 1;


                        } else {


                            document.getElementById("availability").innerHTML =
                                "<span class='error'>Avaliable</span>";
                            $('#register').attr("disabled", false);
                            $('#register').css("background", "blue");
                            mod7 = 0


                        }
                    }
                })
            }
        }),
        $('#register').click(function() {
          
            if (mod7 == 0) {
                $('#register').attr("disabled", true);
                $('#register').css("background", "lightblue");
            }
        });

});
</script>

<body>

    <form action="" method="POST">

        <div id="booking" class="section">
            <div class="section-center"><br>
                <div class="container">
                    <div class="row">
                        <div class="col-md-7 col-md-push-5">
                            <div class="booking-cta">
                                <h1>Make your reservation</h1>
                                <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Animi facere, soluta magnam
                                    consectetur molestias itaque
                                    ad sint fugit architecto incidunt iste culpa perspiciatis possimus voluptates
                                    aliquid consequuntur cumque quasi.
                                    Perspiciatis.
                                </p>
                            </div>
                        </div>
                        <?php
    $conn=mysqli_connect("localhost","root","","miniprojects6");
							$query="select *from place";
							$result=mysqli_query($conn,$query);
?>
                        <div class="col-md-4 col-md-pull-7">
                            <div class="booking-form">
                                <form>
                                    <div class="form-group">
                                        <span class="form-label">Your Destination</span>
                                        <select name="tourist" class="form-control">
                                            <?php
                                    while($row=mysqli_fetch_array($result))
{
					
?>
                                            <option class="form-control" value="<?php echo $row['place_name'];?>">
                                                <?php echo $row['place_name'];?></option>
                                            <?php
                                }
                                ?>

                                        </select>
                                        <span class="select-arrow"></span>
                                    </div>

                                    <div class="form-group">
                                        <span class="form-label">Start Date</span>
                                        <input class="form-control" type="date" id="email1" name="email1">
                                    </div>


                                    <div class="form-group">
                                        <span class="form-label">End Date</span>
                                        <input class="form-control" type="date" id="email2" name="email2">
                                    </div>
                                    <div style="margin-left:250px"> <input type="button" value="check" id="register1">
                                    </div>
                                    <div style="margin-top:1px;"><span id="availability"></span></div>
                                    <div class="row">

                                        <div class="col-sm-4">
                                            <div class="form-group">
                                                <span class="form-label">Adults</span>
                                                <select class="form-control" name="adults">
                                                    <option value="2">1</option>
                                                    <option value="2">2</option>
                                                    <option value="3">3</option>
                                                    <option value="4">4</option>
                                                    <option value="5">5</option>
                                                    <option value="6">6</option>
                                                    <option value="7">7</option>

                                                </select>
                                                <span class="select-arrow"></span>
                                            </div>
                                        </div>
                                        <div class="col-sm-4">
                                            <div class="form-group">
                                                <span class="form-label">Children</span>
                                                <select class="form-control" name="children">
                                                    <option value="0">0</option>
                                                    <option value="1">1</option>
                                                    <option value="2">2</option>
                                                    <option value="3">3</option>
                                                    <option value="4">4</option>
                                                    <option value="5">5</option>
                                                    <option value="6">6</option>
                                                    <option value="7">7</option>
                                                </select>
                                                <span class="select-arrow"></span>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-btn">
                                        <input type="submit" value="book" name="check" id="register" class="submit-btn">
                                        <div style="margin-left:230px;margin-top:-40px"><a href="caravan2.php"
                                                class="submit-btn" style="text-decoration:none">cancel</a> </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>
    <nav1>
        <div style="margin-left:50px">
            <font color="white" size="5"><i><img
                        src="https://www.keralatourism.org/images/caravan-tourism/caravan-kerala-logo.png" alt=""
                        width="200" height="60"></i></font>
        </div>


        </div>
        </div>
        </div>
    </nav1>
  

</body>

</html>
<?php 
if(isset($_POST["check"]))
{
   
	$a=$_POST["email1"];
	$b=$_POST["email2"];
	$c=$_POST["tourist"];
	$d=$_POST["adults"];
	$e=$_POST["children"];
	$conn=mysqli_connect("localhost","root","","miniprojects6")or die("Connect failed: %s\n". $conn -> error);
	$insert="insert into booking(customer_id,caravan_id,start,end,adults,children,place)values('$id','$caravan','$a','$b','$d','$e','$c')";
  $k=mysqli_query($conn,$insert);

	?>
<script>
alert("Already booked the dates");
</script>

<?php

}