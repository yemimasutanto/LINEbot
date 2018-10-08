<?php
	include('conn.php');

	if (!empty($_POST['nrp']) && !empty($_POST['nama']) && !empty($_POST['kosan'])) {

		$user_id = $_POST['nrp'];
		$nama = $_POST['nama'];
		$kosan = $_POST['kosan'];
        
        
		$queryResult = $conn->query("INSERT INTO `api-hafid` (nrp, nama, kosan) VALUES ('$user_id', '$nama', '$kosan')");

		echo json_encode(array( 'flag'=>"1" ), JSON_PRETTY_PRINT);
	}

	else{
		echo json_encode(array( 'flag'=>"0" ), JSON_PRETTY_PRINT);
		// echo "data tidak ditemukan";
	}
	
?>