def isPerfectSqr(num):
  x = num // 2
  seen = set([x])

  while x * x != num:
    x = (x + (num // x)) // 2
    if x in seen:
      return False
    seen.add(x)

  return True

def rational_to_contfrac(e, n):
  while e:
        a = e // n
        yield a
        e, n = n, e - a * n

def contfrac_to_rational_iter(contfrac):
  n0, d0 = 0, 1
  n1, d1 = 1, 0

  for q in contfrac:
      n = q * n1 + n0
      d = q * d1 + d0
      yield n, d
      
      n0, d0 = n1, d1
      n1, d1 = n, d

def convergents_from_contfrac(contfrac):
    nn, dd = 1, 0

    for i, (n, d) in enumerate(contfrac_to_rational_iter(contfrac)):
        if i % 2 == 0:
            yield n + nn, d + dd
        else:
            yield n, d
        nn, dd = n, d

def get_private_exponent(e, n):
  for k, dg in convergents_from_contfrac(rational_to_contfrac(e, n)):
    edg = e * dg
    phi = edg // k
    x = n - phi + 1

    if x % 2 == 0 and isPerfectSqr((x//2)**2 - n):
      g = edg - phi * k
      return dg // g

  return 0


if __name__ == "__main__":
  from Crypto.Util.number import long_to_bytes
  from parametrs import N, E, C

  D = get_private_exponent(E, N)
  plainMessage = long_to_bytes(pow(C, D, N)).decode()

  print(plainMessage)
