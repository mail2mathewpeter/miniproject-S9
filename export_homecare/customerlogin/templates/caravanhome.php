<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link href="https://fonts.googleapis.com/css?family=Poppins:100,200,300,400,500,600,700,800,900&display=swap" rel="stylesheet">

    <title></title>

    <!-- Bootstrap core CSS -->
    <link href="caravan/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- Additional CSS Files -->
    <link rel="stylesheet" href="caravan/assets/css/fontawesome.css">
    <link rel="stylesheet" href="caravan/assets/css/style.css">
    <link rel="stylesheet" href="caravan/assets/css/owl.css">
  </head>
<style>
   .k {
        border-radius: 100%;
    }
    .n9 {
        color: black;
        text-decoration: none;
        margin-top: -10px;
        margin-bottom: 10px;

        padding: 10 21;
        text-transform: uppercase;
        float: left;

    }

    .n9:hover {

        text-decoration: none;
        font-weight: bold;
        color: green;
    }

    .dropdown:hover .dropdown-content {
        display: block;
    }

   


    .desc {
        padding: 15px;
        text-align: center;

    }

    .dropdown {
        position: relative;
        display: inline-block;
        margin-top: -10px;
        margin-left: 40px;
    }

    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #f9f9f9;
        min-width: 190px;
        box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
        z-index: 1;
    }
    .dropdown:hover .dropdown-content {
        display: block;
    }

    </style>
  <body>

    <!-- ***** Preloader Start ***** -->
    <div id="preloader">
        <div class="jumper">
            <div></div>
            <div></div>
            <div></div>
        </div>
    </div>  
    <!-- ***** Preloader End ***** -->

    <!-- Header -->
   

    <header class="">
      <nav class="navbar navbar-expand-lg">
        <div class="container">
          <img src="https://www.keralatourism.org/images/caravan-tourism/caravan-kerala-logo.png" alt=""width="200"height="60">
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarResponsive">
            <ul class="navbar-nav ml-auto">
              <li class="nav-item ">
                <a class="nav-link" href="index.html#top">Home
                  <span class="sr-only"></span>
                </a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="index.html#about">About</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="index.html#projects">About</a>
              </li>
              <li class="nav-item active">
                <a class="nav-link" href="caravanhome.php">Caravan</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="index.html#contact-usl">Contact Us</a>
              </li>
            <li>  <a href="login.php"><img src="img/23.png "width="40"height="35"></a> </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>

    <!-- Page Content -->
    <!-- Banner Starts Here -->
    <div class="main-banner header-text" id="top">
        <div class="Modern-Slider">
          <!-- Item -->
          <div class="item item-1">
            <div class="img-fill">
                <div class="text-content">
                  <h6>Welcome Caravan Booking website</h6>
                 
                  <p>Caravan Tourism policy is unique for many reasons. For one, it facilitates travellers to embark on a once-in-a-lifetime-experience involving the luxury of caravans, the idyllic setting of caravan parks and Village Life Experience (VLE) packages powered by Kerala Responsible Tourism Mission.</p>
                  <a href="index.html#about" class="filled-button">About</a>
                </div>
            </div>
          </div>
          <!-- // Item -->
          <!-- Item -->
          <div class="item item-2">
            <div class="img-fill">
              <div class="text-content">
                <h6>Welcome Caravan Booking website</h6>
               
                <p>Caravan Tourism policy is unique for many reasons. For one, it facilitates travellers to embark on a once-in-a-lifetime-experience involving the luxury of caravans, the idyllic setting of caravan parks and Village Life Experience (VLE) packages powered by Kerala Responsible Tourism Mission.</p>
                <a href="index.html#about" class="filled-button">About</a>
              </div>
            </div>
          </div>
          <!-- // Item -->
          <!-- Item -->
          <div class="item item-3">
            <div class="img-fill">
              <div class="text-content">
                <h6>Welcome Caravan Booking website</h6>
               
                <p>Caravan Tourism policy is unique for many reasons. For one, it facilitates travellers to embark on a once-in-a-lifetime-experience involving the luxury of caravans, the idyllic setting of caravan parks and Village Life Experience (VLE) packages powered by Kerala Responsible Tourism Mission.</p>
                <a href="index.html#about" class="filled-button">About</a>
              </div>
            </div>
          </div>
          <!-- // Item -->
        </div>
    </div>
    <!-- Banner Ends Here -->

    
    <div class="services">
      <div class="container">
        <div class="row">
          <div class="col-md-12">
            <div class="section-heading">
              <h2>Featured <em>Caravans</em></h2>
          
            </div>
          </div>
          <?php
					        $conn=mysqli_connect("localhost","root","","miniprojects6");
							$query="select *from caravan where status='Active'";
							$result=mysqli_query($conn,$query);
while($row=mysqli_fetch_array($result))
{
							?>
          <div class="col-md-4">
            <div class="service-item">
              <img src="admin/uploads/<?php echo $row['caravan_image'];?>"width="200"height="200">
              <div class="down-content">
                <h4><?php echo $row['caravan_name']?></h4>
                <h5><?php echo $row['caravan_model']?></h5><br>
                <h5> <?php echo $row['caravan_type']?></h5><br>
              
              
                <div style="margin-bottom:40px;">
                  <span>
                  <h5>  <sup>$</sup> <?php echo $row['amount']?>  </h5>
                  </span>
                </div>

                <font size="5"color="red"> <div style="margin-left:45px"> <?php echo "<a href='carvandetail.php?id=$row[id]'class='btn btn-primary'><div class='filled-button'>view more</div></a>"?></div></font>
             
              </div>
            </div>
            
            <br>
          </div>
          <?php
          }
          ?>
         

    

    <!-- Bootstrap core JavaScript -->
    <script src="caravan/vendor/jquery/jquery.min.js"></script>
    <script src="caravan/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Additional Scripts -->
    <script src="caravan/assets/js/custom.js"></script>
    <script src="caravan/assets/js/owl.js"></script>
    <script src="caravan/assets/js/slick.js"></script>
    <script src="caravan/assets/js/accordions.js"></script>

    <script language = "text/Javascript"> 
      cleared[0] = cleared[1] = cleared[2] = 0; //set a cleared flag for each field
      function clearField(t){                   //declaring the array outside of the
      if(! cleared[t.id]){                      // function makes it static and global
          cleared[t.id] = 1;  // you could use true and false, but that's more typing
          t.value='';         // with more chance of typos
          t.style.color='#fff';
          }
      }
    </script>

  </body>
</html>