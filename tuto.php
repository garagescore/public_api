<?php
require_once __DIR__ . '/vendor/autoload.php';
define("API_URL", 'api.garagescore.com/');
define("PROTOCOL", 'https');
use GuzzleHttp\Client;


//lancer la commande (composer require guzzlehttp/guzzle:^7.0) avant de lancer le script 
function _encodeURI($str){
    
    return urlencode($str);
}
function _sign($apiKey, $apiSecret, $method, $url, $parameters){
    
    $timestamp = time();
   
    $encodedUrl = $url;
 
    $signatureString = $apiKey . $method . $encodedUrl . $timestamp;
   
    $hashed = hash_hmac('sha1', $signatureString, $apiSecret);
    return  $hashed;
}
function generateURL($apiKey, $apiSecret, $method, $uri, $params){
    
    if ($params and count($params) > 0){
         $params = serialize($params);
    }
    $url = PROTOCOL . '://' . API_URL . $uri;
    $signature = _sign($apiKey, $apiSecret, $method, $url, $params);
    $parametersString = urlencode(serialize($params));
    if ($parametersString){
        $parametersString = '&' . $parametersString;
    }
        
    $requestURL = $url . '?' . 'signature=' . $signature . '&appId=' . $apiKey;
    
    return $requestURL;
}
function the_request($apiKey, $apiSecret, $method, $uri, $params = [], $jsonPOST = null){
    $r = "";
    $request = new Client(['verify' => false]);
    $url = generateURL($apiKey, $apiSecret, $method, $uri, $params);
    if($method == "GET"){ 
      $response =  $request->get($url);
      $r = $response->getBody()->getContents();
    }
    if($method == "POST"){ 
        $option = [
            'json' => $params
        ];
        $response = $request->post($url, $option);
        $r = $response;
       
    }
    
    var_dump($r); 
    return $r;
  
}

$apiKey = $argv[1];

$apiSecret = $argv[2];

the_request($apiKey, $apiSecret, 'GET', 'garage/59397ebf9b90721900cc1f7b/reviews', []);

?>