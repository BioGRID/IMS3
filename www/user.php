<?php
require_once('ims/ims.php');
$cfg=new IMS\config('ims.json');

// Header to use if we fail.
const FAIL='HTTP/1.1 403 Forbidden';

if('POST'==$_SERVER['REQUEST_METHOD']){
  // Only check password if we are POSTed to.

  $pass=md5($_POST['pass']); // hurry up and code the password
  unset($_POST['pass']); // is there a better way to scrub?
  $pdos=$cfg->user($_POST['name']); // fetch an User object
  $user=$pdos->fetch(); // there can be only one
  if($pass==$user['user_password']){
    // Yea, we successfully authenicated!

    $cookie=md5($user['user_name'].$_SERVER['REMOTE_ADDR'].time());
    setcookie('name',$user['user_name'],$cfg->expires());
    setcookie('auth',$cookie,$cfg->expires());
    $pdos->update
      ($user['user_id'],
       [
	'user_cookie'    =>$cookie,
	'user_lastaccess'=>$cfg->now()
	]);
  }else{
    // tried to auth, but it failed
    header(FAIL);
    exit(1);
  }
}else{
  $user=$cfg->verify_user();
  if($user){
  }else{
    // either not logged in, or the cookie was wrong.
    header(FAIL);
    exit(1);
  }
}

// This will evetually return data about what papers it wants the
// user to work on.
print json_encode($user);
