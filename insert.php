<?php
	include('conn.php');

	if (!empty($_POST['nrp']) && !empty($_POST['nama']) && !empty($_POST['alamat'])) {

		$user_id = $_POST['nrp'];
		$nama = $_POST['nama'];
		$alamat = $_POST['alamat'];
        
        
		$queryResult = $conn->query("INSERT INTO `api_yemima` (nrp, nama, alamat) VALUES ('$user_id', '$nama', '$alamat')");

		echo json_encode(array( 'flag'=>"1" ), JSON_PRETTY_PRINT);
	}

	else{
		echo json_encode(array( 'flag'=>"0" ), JSON_PRETTY_PRINT);
		// echo "data tidak ditemukan";
	}
	
?>