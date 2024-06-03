<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>iPlexPlayer</title>
  <link rel="stylesheet" href="style.css">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <script src="https://content.jwplatform.com/libraries/SAHhwvZq.js"></script>  
</head>
<body>
  <div id="jwplayerDiv"></div>
  
  <?php 
  error_reporting(0);

  // Handle blocked domains
  $currentDomain = $_SERVER['HTTP_HOST'];
  $blockedDomainsJSON = 'https://sanjibweb.me/blocked.json';
  $blockedDomains = json_decode(file_get_contents($blockedDomainsJSON), true);
  
  if (in_array($currentDomain, $blockedDomains['domains'])) {
      header("Location:https://telegram.me/sanjiblive");
  } else {
      // Proceed with player setup
      $channelId = $_GET['id'];
      $channelsData = json_decode(file_get_contents('https://sanjibweb.me/TP-WEB-PUB.json'), true);
      $selectedChannel = null;
      
      foreach ($channelsData as $channel) {
        if ($channel['id'] == $channelId) {
          $selectedChannel = $channel;
          break;
        }
      }

      if (!$selectedChannel) {
        echo 'Error: Invalid channel ID';
        exit;
      }

      $videoUrl = $selectedChannel['playurl'];
      $videoTitle = $selectedChannel['title'];
      $logo = $selectedChannel['logo'];
      $id = $selectedChannel['drm_keyId'];
      $key = $selectedChannel['drm_key'];
      $group = $selectedChannel['group'];

      $jwdata =  "jwplayer(\"jwplayerDiv\").setup({
          \"mute\": false,
          \"autostart\": true,
          position: 'bottom',  
          \"Volume\": \"100\",
          \"width\": \"100%\", 
          \"stretching\": \"exactfit\",
          file: \"$videoUrl\", 
          type: \"dash\",
          drm: { \"clearkey\": { 
              \"keyId\": \"$id\",  
              \"key\": \"$key\" , 
          }}
      });";
      
      require_once 'base.php'; 
      $san = new SanjibObf($jwdata); 
      $obsfucated = $san->Obfuscate(); 
  }
  ?>

  <div class="drops">
    <div class="drop drop-1">
      <img class="logo" src="<?php echo $logo; ?>" alt="Channel Logo">
      <span class="s-n">STREAMING NOW</span>
      <span class="channel-name" style="margin-left:0px;"><?php echo $videoTitle; ?><br><span class="live-text" style="color:brown"></span></span>
      <div class="program-name">Program : <?php echo $group; ?><br>
        <div class="program-timing">
          Time : <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Clock_mini.svg/48px-Clock_mini.svg.png" style="width:25px"> <?php echo $selectedChannel['runtime']; ?> Minutes Runtime    
          <div class="program-timing">
            Date: <?php echo $selectedChannel['date']; ?>
          </div>
        </div>
      </div>
      <div class="program-description">𝐃𝐄𝐒𝐂𝐑𝐈𝐏𝐓𝐈𝐎𝐍 :<?php echo $selectedChannel['description']; ?> </div>
    </div>
  </div>

  <script>
    <?php echo $obsfucated; ?>
  </script>
</body>
</html>
