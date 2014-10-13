keyboard = {
  x: {},
  y: ['q w e r t y u i o p', ' a s d f g h j k l', '  z x c v b n m'],
};
for (var i in keyboard.y)
  for (var y of keyboard.y[i])
    keyboard.x[y] = i;
p = C => (x=keyboard.x[C],{x, y: keyboard.y[x].indexOf(C)})
angle = (L, C, R) => (
  p0 = p(L), p1 = p(C), p2 = p(R),
  a = Math.pow(p1.x-p0.x,2) + Math.pow(p1.y-p0.y,2),
  b = Math.pow(p1.x-p2.x,2) + Math.pow(p1.y-p2.y,2),
  c = Math.pow(p2.x-p0.x,2) + Math.pow(p2.y-p0.y,2),
  Math.acos((a+b-c) / Math.sqrt(4*a*b))
)
corner = (L, C, R, W) => {
  ngl = angle(L, C, R);
  if (ngl < 2.2) return [C + "{0,2}"]
  else if (ngl < 2.7) {
    if (t = W[W.length - 1].match(/^\[([^\]]+)\]/)) {
      if (t[1].indexOf(L) + t[1].indexOf(C) > -2) {
        W.pop();
        t = new Set([...t[1].split(""), L, C]);
        return [["[", ...t,"]{0," + (t.size + 1) + "}"].join("")]
      }
    }
    return ["[" + L + "]{0,2}", C + "{0,3}"]
  } else return ["[" + R + C + L + "]{0,2}"]
}
f = S => {
  for (W = [S[0] + "{1,2}"],i = 1; i < S.length - 1; i++)
    W.push(...corner(S[i - 1], S[i], S[i + 1], W))
  return [
    new RegExp("^" + W.join("") + S[S.length - 1] + "{1,3}$"),
    new RegExp("^" + W.filter(C=>!~C.indexOf("[")).join("") + S[S.length - 1] + "{1,3}$")
  ]
}
SwiftKey = C => (
  matched = [], secondPass = [], reg = f(C),
  words.forEach(W=>W.match(reg[0])&&matched.push(W)),
  words.forEach(W=>W.match(reg[1])&&secondPass.push(W)),
  first = matched.sort((a,b)=>a.length<b.length)[0],
  second = secondPass.sort((a,b)=>a.length<b.length)[0],
  second && second.length >= first.length? second: first
)