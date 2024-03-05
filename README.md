# Description

Framework with indicators 

# Naming

`IN_M(P|P)[D|D]`

IN - Indicator name in CammelCase
M - metioc of indicator (optional value if indicator has several values)
P|P - parameters of indicator splitted by '|'
D|D - dependency columns splitted by '|'

Example:
- `EMA(7)[CLOSE]`
- `BB_H(120|2)[HIGH|LOW]` + `BB_L(120|2)[HIGH|LOW]`
