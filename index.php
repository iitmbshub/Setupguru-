<?php
// Simple PHP version for immediate deployment
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input = json_decode(file_get_contents('php://input'), true);
    $message = $input['message'] ?? '';
    
    // Load company data
    $data = [];
    if (file_exists('my_data.jsonl')) {
        $lines = file('my_data.jsonl', FILE_IGNORE_NEW_LINES);
        foreach ($lines as $line) {
            $item = json_decode($line, true);
            if ($item) {
                $data[] = $item;
            }
        }
    }
    
    // Simple response logic
    $response = findResponse($message, $data);
    
    echo json_encode([
        'response' => $response,
        'status' => 'success'
    ]);
    exit;
}

function findResponse($message, $data) {
    $message = strtolower($message);
    
    // Search in company data
    foreach ($data as $item) {
        if (stripos($item['question'], $message) !== false || 
            stripos($message, strtolower($item['question'])) !== false) {
            return $item['answer'];
        }
    }
    
    // Default business responses
    if (strpos($message, 'product') !== false || strpos($message, 'sell') !== false) {
        return "We sell premium desk setup products including laptop accessories, ergonomic items, lighting solutions, and smart gadgets. Use WELCOME code for 10% off at www.setupguru.shop";
    }
    
    if (strpos($message, 'contact') !== false || strpos($message, 'help') !== false) {
        return "Contact our support team at 9499473347 or visit www.setupguru.shop for immediate assistance.";
    }
    
    if (strpos($message, 'discount') !== false || strpos($message, 'coupon') !== false) {
        return "Use coupon code WELCOME for 10% discount on all products at www.setupguru.shop";
    }
    
    if (strpos($message, 'founder') !== false || strpos($message, 'owner') !== false) {
        return "SetupGuru.shop was founded by Rao Jatin and Aryan Soni. Contact us at 9499473347.";
    }
    
    // Default response
    return "I can help you with SetupGuru.shop products and services. Our desk setup accessories improve productivity significantly. Use WELCOME code for 10% off. Visit www.setupguru.shop or call 9499473347.";
}
?>