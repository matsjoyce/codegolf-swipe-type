words = read("wordlist").split("\n");
keyboard = {
  x: {},
  y: ['  q      w      e      r      t      y      u      i      o      p',
      '    a      s      d      f      g      h      j      k      l',
      '        z      x      c      v      b      n      m'],
};
for (var i in keyboard.y)
  for (var y of keyboard.y[i])
    keyboard.x[y] = +i*7;
p = C => (x=keyboard.x[C],{x, y: keyboard.y[x/7].indexOf(C)})
angle = (L, C, R) => (
  p0 = p(L), p1 = p(C), p2 = p(R),
  a = Math.pow(p1.x-p0.x,2) + Math.pow(p1.y-p0.y,2),
  b = Math.pow(p1.x-p2.x,2) + Math.pow(p1.y-p2.y,2),
  c = Math.pow(p2.x-p0.x,2) + Math.pow(p2.y-p0.y,2),
  Math.acos((a+b-c) / Math.sqrt(4*a*b))/Math.PI*180
)
corner = (L, C, R, N, W) => {
  if (skip) {
    skip = false;
    return [];
  } 
  ngl = angle(L, C, R);
  if (ngl < 80) return [C + "{1,3}"]
  if (ngl < 115 && p(L).x != p(R).x && p(L).x != p(C) && p(R).x != p(C).x && Math.abs(p(L).y - p(R).y) < 5) return [C + "{0,3}"]
  if (ngl < 138) {
    if (N && Math.abs(ngl - angle(C, R, N)) < 6) {
      skip = true;
      return [L + "{0,3}", "([" + C + "]{0,3}|[" + R + "]{0,3})?", N + "{0,3}"]
    }
    return [C + "{0,3}"]
  }
  return ["([" + L + "]{0,3}|[" + C + "]{0,3}|[" + R + "]{0,3})?"]
}
f = S => {
  for (W = [S[0] + "{1,2}"],i = 1; i < S.length - 1; i++)
    W.push(...corner(S[i - 1], S[i], S[i + 1], S[i + 2], W))
  return [
    new RegExp("^" + W.join("") + S[S.length - 1] + "{1,3}$"),
    new RegExp("^" + W.filter(C=>!~C.indexOf("[")).join("") + S[S.length - 1] + "{1,3}$")
  ]
}
thirdPass = (F, C) => {
  if (!F[0]) return null
  F = F.filter((s,i)=>!F[i - 1] || F[i - 1] != s)
  FF = F.map(T=>[...T].filter((c,i)=>!T[i - 1] || T[i - 1] != c).join(""))
  if (FF.length == 1) return F[0];
  if (FF.length < 6 && FF[0][2] && FF[1][2] && FF[0][0] == FF[1][0] && FF[0][1] == FF[1][1])
    if (Math.abs(F[0].length - F[1].length) < 1)
      for (i=0;i<Math.min(F[0].length, FF[1].length);i++) {
        if (C.indexOf(FF[0][i]) < C.indexOf(FF[1][i])) return F[0]
        else if (C.indexOf(FF[0][i]) > C.indexOf(FF[1][i])) return F[1]
      }
  return F[0]
}
var skip = false;
SwiftKey = C => (
  C = [...C].filter((c,i)=>!C[i - 1] || C[i - 1] != c).join(""),
  skip = false, matched = [], secondPass = [], L = C.length, reg = f(C),
  words.forEach(W=>W.match(reg[0])&&matched.push(W)),
  words.forEach(W=>W.match(reg[1])&&secondPass.push(W)),
  matched = matched.sort((a,b)=>Math.abs(L-a.length)>Math.abs(L-b.length)),
  secondPass = secondPass.sort((a,b)=>Math.abs(L-a.length)>Math.abs(L-b.length)),
  first = matched[0], second = secondPass[0], third = thirdPass(secondPass.length? secondPass: matched, C),
  second && second.length >= first.length - 1? first != third ? third: second: third.length >= first.length ? third: first
)

// For use by js shell of latest firefox
print(SwiftKey(readline()));