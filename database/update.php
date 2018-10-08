<?php
	include('conn.php');

	if (!empty($_POST['nrp']) && !empty($_POST['nama']) && !empty($_POST['alamat'])) {

		$user_id = $_POST['nrp'];
		$nama = $_POST['nama'];
		$kosan = $_POST['alamat'];
        $nrp_lama = $_POST['nrp_lama'];
		$queryResult = $conn->query("UPDATE `api_yemima` SET nrp = '$user_id', nama = '$nama', alamat = '$alamat' WHERE nrp ='$nrp_lama'");
        if($queryResult==true)
    		echo json_encode(array( 'flag'=>"1" ), JSON_PRETTY_PRINT);
    	else
    	    echo json_encode(array( 'flag'=>"0" ), JSON_PRETTY_PRINT);
	}

	else{
		echo json_encode(array( 'flag'=>"0" ), JSON_PRETTY_PRINT);
		// echo "data tidak ditemukan";
	}
?>