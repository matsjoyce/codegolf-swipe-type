<?php
function get_dir($a, $b){
    $c = [0, 0];
    if($a[0] < $b[0]) $c[0] = 1;
    else if($a[0] > $b[0]) $c[0] = -1;
    if($a[1] < $b[1]) $c[1] = 1;
    else if($a[1] > $b[1]) $c[1] = -1;
    return $c;
}
function load_dict(){
    return explode(PHP_EOL, file_get_contents('wordlist'));
}

$coord = [];
$f = fopen('keypos.csv', 'r');
while(fscanf($f, "%c, %f, %f", $c, $x, $y))
    $coord[$c] = [$x, $y];
fclose($f);

$dict = load_dict();
$in = $argv[1];
$possib = [];
$dupl = ['aa','bb','cc','dd','ee','ff','gg','hh','ii','jj','kk','ll','mm','nn','oo','pp',
         'qq','rr','ss','tt','uu','vv','ww','xx','yy','zz'];
$repl = str_split('abcdefghijklmnopqrstuvwxyz');
foreach($dict as $c){
    if($c[0] == $in[0]){
        $q = strlen($c);
        $r = strlen($in);
        $last = '';
        $fail = false;
        $i = $j = 0;
        for($i = 0; $i < $q; ++$i){
            if($last == $c[$i]) continue;
            if($j >= $r){
                $fail = true;
                break;
            }
            while($c[$i] != $in[$j++])
                if($j >= $r){
                    $fail = true; 
                    break;
                }
            if($fail) break;
            $last = $c[$i];
        }
        if(!$fail) 
            $possib[] = $c;
    }
}

$longest = '';
foreach($possib as $p){
    if(strlen($p) > strlen($longest))
        $longest = $p;
}

$cpos = $coord[$in[0]];
$dir = [0, 0];
$chars = str_split($in); unset($chars[0]);
$check = $in[0];
$oldc = $in[0];
foreach($chars as $c){
    $newdir = get_dir($cpos, $coord[$c]);
    if(($dir[0] && $newdir[0] && $newdir[0] != $dir[0])
    || ($dir[1] && $newdir[1] && $newdir[1] != $dir[1])){
        $check .= $oldc;
        $dir = $newdir;
    }else{
        if(!$dir[0]) $dir[0] = $newdir[0];
        if(!$dir[1]) $dir[1] = $newdir[1];
    }
    $cpos = $coord[$c];
    $oldc = $c;
}
$check .= substr($in, -1);
$r = '/^' . implode('.*', str_split(str_replace($dupl,$repl,$check))) . '$/';
foreach($possib as $k=>$p){
    if(!preg_match($r, $p))
        unset($possib[$k]);
}
$newlong = '';
foreach($possib as $p){
    if(strlen($p) > strlen($newlong))
        $newlong = $p;
}
if(strlen($newlong) == 0) echo $longest;
else echo $newlong;