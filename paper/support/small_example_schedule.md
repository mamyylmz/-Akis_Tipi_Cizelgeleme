# 5×3 PFSP Doğrulama Örneği

Kaynak, ders sorumlusunun Problem 7 belgesindeki doğrulama örneğidir. Bu dosya final Taillard Gantt sonucu değildir; model doğrulama desteğidir.

| İş | M1 | M2 | M3 |
| --- | ---: | ---: | ---: |
| J1 | 3 | 4 | 2 |
| J2 | 2 | 3 | 4 |
| J3 | 4 | 1 | 3 |
| J4 | 1 | 4 | 2 |
| J5 | 3 | 2 | 3 |

Doğrulama permütasyonu: **J4 → J2 → J1 → J5 → J3**.

`S[i,j] = max(C[i-1,j], C[i,j-1])`  
`C[i,j] = S[i,j] + p[pi[i],j]`

| Sıra | İş | Makine | Süre | Başlangıç | Bitiş |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | J4 | M1 | 1 | 0 | 1 |
| 1 | J4 | M2 | 4 | 1 | 5 |
| 1 | J4 | M3 | 2 | 5 | 7 |
| 2 | J2 | M1 | 2 | 1 | 3 |
| 2 | J2 | M2 | 3 | 5 | 8 |
| 2 | J2 | M3 | 4 | 8 | 12 |
| 3 | J1 | M1 | 3 | 3 | 6 |
| 3 | J1 | M2 | 4 | 8 | 12 |
| 3 | J1 | M3 | 2 | 12 | 14 |
| 4 | J5 | M1 | 3 | 6 | 9 |
| 4 | J5 | M2 | 2 | 12 | 14 |
| 4 | J5 | M3 | 3 | 14 | 17 |
| 5 | J3 | M1 | 4 | 9 | 13 |
| 5 | J3 | M2 | 1 | 14 | 15 |
| 5 | J3 | M3 | 3 | 17 | 20 |

Son hücre `C[5,3]=20`; dolayısıyla **Cmax=20**.

Bu tablodan üretilecek Gantt'ta her makinede çakışma olmamalı ve her iş M1→M2→M3 önceliğini korumalıdır. Final makaledeki büyük örnek Gantt'ı final `results/` verisinden ayrıca üretilecektir.
