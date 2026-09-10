km = float(input("Dĺžka cesty (km): "))
start = float(input("Odchod z domu (hodina): "))
end = float(input("Príchod do hotela (hodina): "))

time = end - start
speed = km / time

print("Auto pôjde priemernou rýchlosťou", speed, "km/h.")
