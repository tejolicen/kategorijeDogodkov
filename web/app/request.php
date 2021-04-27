<?php
    session_start();
    $action = $_REQUEST["action"];
    if ($action == "predict") {
        predict();
    }
    function predict() {    
        $search = $_REQUEST["s"];
        $url = 'https://kategorije-dogodkov.herokuapp.com/predict';

        // use key 'http' even if you send the request to https://...
        $options = array(
            'http' => array(
                'header'  => "Content-type: text/plain\r\n",
                'method'  => 'POST',
                'content' => $search
            )
        );
        $context  = stream_context_create($options);
        $result = file_get_contents($url, false, $context);
        if ($result === FALSE) { /* Handle error */ }
        
        echo json_encode($result);
    }
?>
