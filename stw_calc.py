def calculate_fft(p,g,i_max,e):
  fft = []
  dwf = calculate_dwf(p,g,i_max,e)
  fft.append(3*dwf)
  tmp = round((3*p*g+i_max+e)/86400, 3)
  fft.append(tmp)
  return fft


def calculate_dwf(p,g,i_dwf,e):
  # 20-percentile of TDV data provides good estimate of DWF
  return p*g + i_dwf + e


def calculate_pe(bod, population):
  if population > 249:
    pe = bod / 0.06
  else:
    pe = population
  return round(pe, 3)

