<?php
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $inputString = isset($_POST['userInput']) ? $_POST['userInput'] : '';
    $file = 'storedString.txt';

    if (file_exists($file)) {
        $storedString = trim(file_get_contents($file));

        if ($inputString === $storedString) {
            echo json_encode(['match' => true]);
        } else {
            echo json_encode(['match' => false]);
        }
    } else {
        http_response_code(404);
        echo json_encode(['match' => false, 'error' => 'File not found']);
    }
} else {
    http_response_code(405);
    echo json_encode(['match' => false, 'error' => 'Invalid request method']);
}
?>
