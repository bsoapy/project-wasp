def calculate_fft(p,g,i_max,e):
  return 3*p*g+i_max+e


def calculate_dwf(p,g,i_dwf,e):
  return p*g + i_dwf + e


def calculate_pe(bod):
  if bod > 100:
    bod = bod / 0.6
  return bod

