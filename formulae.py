def calculate_fft(p,g,i_max,e):
  return round((3*p*g+i_max+e)/86400, 3)


def calculate_dwf(tdv):
  return tdv


def calculate_pe(bod, population):
  if population >= 250:
    pe = bod / 0.06
  else:
    pe = population
  return round(pe, 3)