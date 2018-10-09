<?php
	include('conn.php');
    
    if (isset($_POST['nrp'])) {
        $user_id = $_POST['nrp'];
        
        if($result = mysqli_query($conn, "DELETE FROM `api_yemima` where nrp=".$user_id)) 
            echo json_encode(array('flag'=>"1"), JSON_PRETTY_PRINT);    
        else
            echo json_encode(array('flag'=>"0"), JSON_PRETTY_PRINT);
        
    }

?>