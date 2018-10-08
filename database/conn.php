<?php
     $host = "185.224.138.56";
     $user = "u670067699_rpl";
     $password = "adminadmin";
     $dbname = "u670067699_rpl";
     $conn = mysqli_connect($host, $user, $password, $dbname);
    
     if (!$conn) {
      die("error in connection");
     }
     else{
            echo("mashok");
     }
?>