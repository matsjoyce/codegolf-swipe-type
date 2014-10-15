<?php
function get_dir($a, $b){
    $c = [0, 0];
    if($a[0] - $b[0] < -1.4) $c[0] = 1;
    else if($a[0] - $b[0] > 1.4) $c[0] = -1;
    if($a[1] < $b[1]) $c[1] = 1;
    else if($a[1] > $b[1]) $c[1] = -1;
    return $c;
}
function load_dict(){
    return explode(PHP_EOL, file_get_contents('wordlist'));
}

$coord = [];
$f = fopen('keypos.csv', 'r');
while(fscanf($f, "%c, %f, %f", $c, $x, $y)){
    $coord[$c] = [$x, $y];  
}
fclose($f);

$dict = load_dict();
$in = $argv[1];
$possib = [];

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

$dir = [[0, 0]];
$cdir = [0, 0];
$check = '/^' . $in[0] . '.*?';
$olst = []; $p = 1;

$len = strlen($in);
for($i = 1; $i < $len; ++$i){
    $dir[$i] = get_dir($coord[$in[$i - 1]], $coord[$in[$i]]);
    $olddir = $cdir;
    $newdir = $dir[$i];
    $xc = $olddir[0] && $newdir[0] && $newdir[0] != $olddir[0];
    $yc = $olddir[1] && $newdir[1] && $newdir[1] != $olddir[1];
    if($xc || $yc){ // separate dir from current dir
        if($yc && !$xc && $dir[$i - 1][1] == 0){
            $tmp = '';
            for($j = $i - 1; $j >= 0 && $dir[$j][1] == 0; --$j){
                $tmp = '(' . $in[$j-1] . '.*?)?' . $tmp;
            }
            $olst[] = range($p, $p + (($i - 1) - $j));
            $p += ($i - 1) - $j + 1;
            $check .= $tmp . '(' . $in[$i - 1] . '.*?)?';
        }else{
            $check .= $in[$i - 1] . '.*?';
        }
        $cdir = $dir[$i];
    }else{
        if(!$cdir[0]) $cdir[0] = $dir[$i][0]; 
        if(!$cdir[1]) $cdir[1] = $dir[$i][1]; 
    }
}
$check .= substr($in, -1) . '$/';
$olstc = count($olst);
$res = [];
foreach($possib as $p){
    if(preg_match($check, $p, $match)){
        if($olstc){
            $chk = array_fill(0, $olstc, 0);
            for($i = 0; $i < $olstc; ++$i){
                foreach($olst[$i] as $j){
                    if(isset($match[$j]) && $match[$j]){
                        ++$chk[$i];
                    }
                }
                // give extra weight to the last element of a horizontal run
                if(@$match[$olst[$i][count($olst[$i])-1]])
                    $chk[$i] += 0.5;
            }
            if(!in_array(0, $chk)){
                $res[$p] = array_sum($chk);
            }
        }else{
            $res[$p] = 1;
        }
    }
}
$possib = array_keys($res, @max($res));
$newlong = '';
foreach($possib as $p){
    if(strlen($p) > strlen($newlong))
        $newlong = $p;
}
if(strlen($newlong) == 0) echo $longest;
else echo $newlong;