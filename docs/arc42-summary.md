# arc42 — Chapter Summary

1. **Introduction and Goals** — odgovara na pitanje zasto sistem postoji i sta je najvaznije, daje pregled zahtjeva (sta sistem radi, glavne fje), ciljeve kvaliteta (3-5 najvaznijih kako ne bi djelovalo da "sve ima prioritet") i pomocu stakeholder-a opisuje uloge svakog ko ima veze sa sistemom i njihova ocekivanja
2. **Constraints** — ogranicenja tj zahtjevi koji dolaze spolja (firma, klijent, zakon), postoje tri tipa: tehnicka(tehnologije, formati, platforme), organizaciona(rokovi, budzet, velicina tima) i konvencije(pravila pisanja koda, dokumentovanja, verzije)
3. **Context and Scope** — jasno odredjuje granice sistema, kaze sta pripada sistemu a sta je spolja i opisuje kako je sistem povezan sa okolinom (interfejsi) kroz dva dijela: Business Context(ko komunicira sa sistemom i koji podaci ulaze/izlaze) i Technical Context(kako podaci putuju - protokoli,formati, koji ulaz koristi koji kanal)
4. **Solution Strategy** — objasnjava kako se rjesava problem, koje su tehnoloske odluke, podjelu sistema i nacin na koji se ostvaruje svaki cilj kvaliteta
5. **Building Block View** — govori od kojih se dijelova sastoji sistem i kako su oni povezani, daje pregled hijerarhije blokova sa njihovim odgovornostima
6. **Runtime View** — kako se sistem ponasa tokom rada, kako njegovi dijelovi saradjuju, koji su najvazniji scenariji - sekvencijalni dijagrami
7. **Deployment View** — veza izmedju softvera i infrastrukture, gdje i na cemu sistem radi, infrastruktura i okruzenja
8. **Cross-cutting Concepts** — koja pravila i obrasci vaze kroz cijeli sistem (ona koja se ponavljaju opisana su jednom)
9. **Architecture Decisions** — cuva razloge donesenih odluka, kontekst, odluka, obrazlozenja i posljedice
10. **Quality Requirements** — ciljevi postaju mjerljivi zahtjevi na osnovu kojih mjerimo d ali je sistem dobar, sadrzi stablo kvaliteta (kategorije kvaliteta) i scenarije kvaliteta (kontekst, događaj, očekivani rezultat)
11. **Risks and Technical Debts** — realan spisak slabih tacaka arhitekture, govori poznate rizike i probleme te kako ih ublaziti
12. **Glossary** — zajednicki jezik tima, sadrzi tabelu strucnih termina

# Banka:

## **Introduction and Goals**
Poslovni problem: banka dobija velike količine papirnih dokumenata (pisma, uplatnice) sa brojevima računa. Mašina za skeniranje ih pretvara u fajl sa „nacrtanim“ ciframa, a službenici sada te brojeve ručno prepisuju, što je sporo i podložno greškama. Sistem treba da to automatizuje: pročita brojeve, provjeri ih i označi one koji su sumnjivi.

Zahtjevi:
F1	Pročitati fajl sa skenera i pretvoriti svaki unos u broj računa od 9 cifara
F2	Provjeriti ispravnost svakog broja pomoću kontrolne sume
F3	Napraviti izlazni fajl sa statusom svakog broja (OK, ERR, ILL)
F4	Pokušati automatsku ispravku pogrešnih ili nečitljivih brojeva

Ciljevi:
Tačnost - sistem nikada ne vrati pogrešan broj kao ispravan. Svaki broj sa nečitljivom cifrom ili lošom kontrolnom sumom mora biti označen (ILL, ERR, AMB)
Robusnost - ako je jedan unos u fajlu oštećen ili nečitljiv, ostali unosi se normalno obrade; jedan loš unos ne zaustavlja cijeli fajl
Održivost - pravila (oblik cifara, formula kontrolne sume, ispravke) su u odvojenim dijelovima, pa se svaki može promijeniti bez rizika za ostala
?performanse mogu izostaviti jer je fajl samo od 500 linija, brza je obrada

Stakeholderi: (??provjeriti da li sam dobro razumjela - ljudi koji su povezani sa sistemom: ULOGA + OCEKIVANJE)
Operater - ubacuje skenirani fajl u sistem i na kraju pregleda rezultate, ocekuje da sumnjivi brojevi budu jasno označeni, da ručno provjerava samo njih
Upravljac skenerom - odredjuje u kom formatu je fajl da bbi sistem mogao da ga obradi, ocekuje da sistem ispravno čita njihov format
Razvojni tim - pravi sistem, kod, mijenja ga, testira, dokumentuje, ocekuje jasnu podjela na dijelove, lako testiranje i mijenjanje
Bankarski sistem - rezultate koristi za uplate, ocekuje da nikad ne dobije pogrešan broj označen kao ispravan

## **Constraints**
Tehnička ograničenja:
- Ulazni format
- Broj računa ima tačno 9 cifara
- Formula kontrolne sume
- Izlazni format: jedan broj po redu, uz oznaku ERR, ILL ili AMB kad treba

Organizaciona ograničenja: nadograditi kasnije
Proces: issue → grana → PR → review instruktora → squash merge

Konvencije: nadograditi kasnije
- koristiti iz git modula nacin kreiranja issua, pr-a, grana i komita
- dokumentacija arc42 u .md fajlovima sa referencama na .puml dijagrame

## **Context and Scope**

Business Context:
Skener - ulaz:fajl sa brojevima računa „nacrtanim“ znakovima _, | i razmakom (prosledjuje operateru, nije direktno povezan na sistem ali bitan je jer proizvodi ulazni fajl i odredjuje format)
Operater - ulaz: pokreće obradu, ubacuje fajl sa skenera, izlaz: izvještaj u kome su sumnjivi brojevi označeni (ERR, ILL, AMB) za ručnu provjeru
Bankarski sistem	—	lista pročitanih brojeva računa sa statusom svakog
- Scope:
    Unutar BankOCR-a: čitanje ASCII cifara iz fajla, označavanje ERR, ILL, AMB, pokušaj automatske ispravke, pravljenje izlaznog fajla
    Izvan BankOCR-a: skeniranje papira (skener), izvršavanje uplata (bankarski sistem), ručna provjera sumnjivih brojeva (operater)

Technical Context:
Skener → BankOCR: kanal-tekstualni fajl, format - unosi od 4 reda: 3 reda po 27 znakova (_, |, razmak) i prazan red
BankOCR → Bankarski sistem:	kanal - tekstualni fajl, format -jedan broj od 9 cifara po redu, opciono sa ERR, ILL ili AMB [...]
Operater ↔ BankOCR: pokretanje obrade i čitanje izlaznog fajla
