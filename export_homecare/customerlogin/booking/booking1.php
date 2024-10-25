<?php
session_start();
$id=$_SESSION['customer'];
$id1=$_SESSION['customer1'];

$_SESSION['customer']=$id;
$_SESSION['customer1']=$id1;
$caravan=$_SESSION['caravan'];
$_SESSION['caravan']=$caravan;

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
.error1 {
            color: green;
            font-size:15px;
           
           
        }
</style>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>

<script>
$(document).ready(function() {
    var mod7 = 1;
    $('#register1').click(function() {
            email2 = document.getElementById("email2").value;

            var email1 = $(this).val();
            email1 = document.getElementById("email1").value;

            if (email1>email2) {
                $('#availability').html('This is not valid date');
                $('#register').attr("disabled", true);
                            $('#register').css("background", "lightblue");
                            mod7 = 1;
            } else {
                $.ajax({
                    url: 'emaildatabase.php',
                    method: "POST",
                    data: {
                        email1: email1,
                        email2: email2
                    },
                    success: function(data) {
                      
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
                                "<span class='error1'>Avaliable</span>";
                            $('#register').attr("disabled", false);
                            $('#register').css("background", "blue");
                            mod7 = 0


                        }
                    }
                })
            }
        }),
        $('#register').click(function() {
          
            if (mod7 == 1) {
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
                              <p>  <font color="white"><h4>The caravan comes equipped with a spacious lounge area and most modern amenities like four recliner seats and a television. The kitchen area is furnished with all the necessary appliances like a refrigerator, microwave, induction cooktop, and custom-built storage for tableware to ensure they stay in place while the caravan is in motion. It is fully air-conditioned and gets double bunk beds in the bedroom and a restroom with a shower.
</h4> </p></font>
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
                                        <input class="form-control" type="text" placeholder="dd-mm-yyyy" id="email1" name="email1"required readonly>
                                    </div>


                                    <div class="form-group">
                                        <span class="form-label">End Date</span>
                                        <input class="form-control" type="text" placeholder="dd-mm-yyyy" id="email2" name="email2"readonly>
                                    </div>
                                    <div style="margin-left:250px"> <input type="button" value="check" id="register1"></div>
                                    
                                    <div style="margin-top:-20px;"><span id="availability"></span></div>
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
                                        <div style="margin-left:230px;margin-top:-40px"><a href="\mathew\miniproject-s6/caravan1.php"
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
    <head>
  <link rel="stylesheet" href="http://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
</head>
<script>
    <?php 
  
   $dates = date('d/m/Y');
    	$conn=mysqli_connect("localhost","root","","miniprojects6")or die("Connect failed: %s\n". $conn -> error);
        $query="select * from booking where caravan_id='$caravan'";
       $query1= mysqli_query($conn,$query);
        while($result=mysqli_fetch_array($query1))
        {
            $a=$result['end'];
            $b=$result['start'];


            $date = getBetweenDates1($b, $a);
            $dates.= implode(" ",$date);
        }
        function getBetweenDates($startDate, $endDate)
    {
        $rangArray = [];
            
        $startDate = strtotime($startDate);
        $endDate = strtotime($endDate);
             
        for ($currentDate = $startDate; $currentDate <= $endDate; 
                                        $currentDate += (86400)) {
                                                
            $date = date('Y-m-d', $currentDate);
            

            $rangArray[] = $date;
        }
  
        return $rangArray;
    }
            
    function getBetweenDates1($startDate, $endDate)
    {
        $rangArray = [];
            
        $startDate = strtotime($startDate);
        $endDate = strtotime($endDate);
             
        for ($currentDate = $startDate; $currentDate <= $endDate; 
                                        $currentDate += (86400)) {
                                                
            $date = date('Y-m-d', $currentDate);
            

            $rangArray[] = $date;
        }
  
        return $rangArray;
    }
            
          
           
          
 ?>
var dates = <?php echo json_encode($dates); ?>;

function DisableDates(date) {
    var string = jQuery.datepicker.formatDate('yy-mm-dd', date);
    return [dates.indexOf(string) == -1 ];
}

$(function() {
     $("#email1").datepicker({
        minDate: 0,
         beforeShowDay: DisableDates
     });
});
  </script>
<body>
<div id="email1"></div>
<script>
    <?php 

  $datas="";
    	$conn=mysqli_connect("localhost","root","","miniprojects6")or die("Connect failed: %s\n". $conn -> error);
        $query="select * from booking where caravan_id='$caravan'";
       $query1= mysqli_query($conn,$query);
        while($result=mysqli_fetch_array($query1))
        {
            $a=$result['end'];
            $b=$result['start'];
      
             

            $date = getBetweenDates($b, $a);
            $datas.= implode(" ",$date);
        }
        ?>       
         

var dates = <?php echo json_encode($datas); ?>;
function DisableDates(date) {
    var string = jQuery.datepicker.formatDate('yy-mm-dd', date);
    return [dates.indexOf(string) == -1 ];
}
       
$(function() {
     $("#email2").datepicker({
        minDate: 0,
         beforeShowDay: DisableDates,
        
     });
});
  </script>
<body>
<div id="email2"></div>
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
    $_SESSION['booking']="yes";
    //session passing//
    $_SESSION["email1"]=$a;
    $_SESSION["email2"]=$b;
    $_SESSION["tourist"]=$c;
    $_SESSION["adults"]=$d;
    $_SESSION["children"]=$e;

    //$status="pending";

    //end//
	/*$conn=mysqli_connect("localhost","root","","miniprojects6")or die("Connect failed: %s\n". $conn -> error);
    $query="select *from customer where logid='$id'";
    $result=mysqli_query($conn,$query);
    while($row=mysqli_fetch_array($result))
{
    $p=$row['id'];
}

	$insert="insert into booking(customer_id,caravan_id,start,end,adults,children,place,status,driver)values('$p','$caravan','$a','$b','$d','$e','$c','$status','pending')";
  $k=mysqli_query($conn,$insert);
*/
	?>
<script>

window.location.href='/mathew/miniproject-s6/confirm details.php';
</script>

<?php

}