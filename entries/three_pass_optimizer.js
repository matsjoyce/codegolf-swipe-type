words = read("wordlist").split("\n")

keyboard = {
  x: {},
  y: ['q   w   e   r   t   y   u   i   o   p', ' a   s   d   f   g   h   j   k   l', '  z   x   c   v   b   n   m'],
};
for (var i in keyboard.y)
  for (var y of keyboard.y[i])
    keyboard.x[y] = +i*4;
p = C => (x=keyboard.x[C],{x, y: keyboard.y[x/4].indexOf(C)})
angle = (L, C, R) => (
  p0 = p(L), p1 = p(C), p2 = p(R),
  a = Math.pow(p1.x-p0.x,2) + Math.pow(p1.y-p0.y,2),
  b = Math.pow(p1.x-p2.x,2) + Math.pow(p1.y-p2.y,2),
  c = Math.pow(p2.x-p0.x,2) + Math.pow(p2.y-p0.y,2),
  Math.acos((a+b-c) / Math.sqrt(4*a*b))
)
corner = (L, C, R, N, W) => {
  if (skip) {
    skip = false;
    return [];
  } 
  ngl = angle(L, C, R);
  if (ngl < 1.4) return [C + "{1,3}"]
  if (ngl < 2.4) {
    if (N && Math.abs(ngl - angle(C, R, N)) < 0.1) {
      skip = true;
      return ["([" + C + "]{0,3}|[" + R + "]{0,3})?"]
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
var skip = false;
SwiftKey = C => (
  C = [...C].filter((c,i)=>!C[i - 1] || C[i - 1] != c).join(""),
  skip = false, matched = [], secondPass = [], L = C.length, reg = f(C),
  words.forEach(W=>W.match(reg[0])&&matched.push(W)),
  words.forEach(W=>W.match(reg[1])&&secondPass.push(W)),
  first = matched.sort((a,b)=>Math.abs(L-a.length)>Math.abs(L-b.length))[0],
  second = secondPass.sort((a,b)=>Math.abs(L-a.length)>Math.abs(L-b.length))[0],
  second && second.length >= first.length - 1 ? second: first
)


print(SwiftKey(readline()));