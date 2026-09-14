dlzka=float(input("Zadajte dĺžku mietnosti (cm):"))
sirka=float(input("Zadajte šírku mietnosti (cm):"))
vyska=float(input("Zadajte výšku mietnosti (cm):"))

sirka_okna=float(input("Zadajte širku okna (cm):"))
vyska_okna=float(input("Zadajte výška okna (cm):"))

vydatnost=float(input("Zadajte výdatnosť farby (m^2/kg):"))
if vydatnost > 0: 

    stena=2dlzkavyska + 2vyskasirka + sirkadlzka
    okno=sirka_oknavyska_okna
    namalovana_stena= stena - okno
    farba=namalovana_stena / vydatnost

    print(f"Maľovať budeš plochu {namalovana_stena:.2f} m^2")
    print(f"Kúp {farba: .2f} kg farby")
else:
    print("Nesprávna výdatnosť farby")
