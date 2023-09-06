from crypto_algorithms.RSA import RSACipher
from crypto_algorithms.AES import AESCipher

rsa = RSACipher(privateKey='LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlDWFFJQkFBS0JnUUNwWVhvVVRtL1M4V1hubEZIMVZCeFFubTNFUCtIU29hMThkdWM3OGVOVi80a2xIV2J5ClFLTkxPMkZRTnNQTWM3N1BFMWpUOTZDT1JpcDk0Q1h2ODlWOVFjWEdEOGRrRXdzRnhxKzJuNXlWUGp4clNtS04KMjZtenhOZGsyejBmZkh3VHlIRlh3RGhCaUxjRml4TUgrRmJWNll6V21KbkxPV1R0UExBTGRSQ0Rld0lEQVFBQgpBb0dBQy9HOVI2Qk9YMnc1ZU82ckp1Y3pCZlplSERnN0J2enl2SE93RTdpWGhQRjdyTnZaYmh6anh3TGRkbWdlClA1VXI3L05YMEw3R0dqSlZmY0hvT3ZjUloySDFHVWpKNkprVkdnZFIwNkdLWFBLNVNibDBmVWZabmRaNXJmSlAKS1J4VlM1dUl3dmg4ZU9pdjdxUmQ2QXRydzJackxUNytjb3RYelptYTRsb0hESUVDUVFEUU5KMUluc05pbTdyOQpnaXAreUFlc1hNQVVoSWFEaDdNbFgrUGMwSGN0QlVVM2xPL3VEZVo2NEkraWVaYXBMNUFJLzZGcVA0Vk02S0xaCk9seWI0UXo3QWtFQTBFTkthR3p2RWpoeVYwd2dqOWEyeHhEY1l0ek1CdWQvS2V2Y25XekZ6c05XQXdpakJjdU8KVDhyUFMvamozejN3VCtwZXZvZlUvUTU2QVEzdkRkZWJnUUpCQUxIdXhSdnkwbmZMTHhySHl4bGVTWEI4TTR0VgpWci9Ca05BNENyd0RURllsVXVvVlZwYlRPazE0N0VlbU1hT1ZDanNtZkFRWkZRcU5KZDhQaVdXT0IxRUNRUURFCmVTY0NPdnFUZ3VNRHpsTE52Kzh3LzR3YVRGakNqclNkMU9DTk4yZXBkd2gyMWpnTnFJcDZaa2VJVWFhUUhmdlAKT0xqbklIZmp3RHVETVNUOE54S0JBa0FRbHBEVEwxdlRWenQ1ZmZTWFFtcHB2cXdJaExDSFhkaVlwNnFyWXcrSApkLzNMb3pOWG5uZlVkVlhtb0h0czBDV1o3TlFsL3h1aDBjSy9DUXNrMW1xQwotLS0tLUVORCBSU0EgUFJJVkFURSBLRVktLS0tLQ==')

key = rsa.decrypt('IvVrnMa58ZhRraS1WT5eaTYO5ICHle0Wth2YNy7Q+u/CdKeIbmebWTMrX7iCyPNXz5gd+0iH2CSBYxJYjPNosNU4I3yu0RdY2SrOodtRZmaiCpdXTmDdi/lNnndAAiWP1o2/QzSiZQjlfJxeZ+bGtpQ8Soq1fInc6FmPSQFOYAA=')

aes = AESCipher(key)