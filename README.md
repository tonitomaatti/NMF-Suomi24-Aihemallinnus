# NMF-Suomi24-Aihemallinnus

Ohjelma mallintaa Suomi24 -foorumin tekstejä [NMF](https://en.wikipedia.org/wiki/Non-negative_matrix_factorization) 
-koneoppimisen tekniikalla. Ohjelma ryhmittelee tekstit sanaryppäisiin ja painoihin, jonka jälkeen käyttäjä tulkitsee 
sanaryppäille aihealueen käyttäen apuna oikeita mahdollisia aihealueita.

Aihealueiden tulkinnan jälkeen ohjelma arvioi ryhmittelyn toimivuutta vertaamalla tekstin oikeaa aihealuetta siihen
tulkittuun aihealueeseen jolle painotusmatriisi ankaa isoimman painon tekstin kohdalla.

Vertauksesta annetaan osumaprosentti, joka on oikealle aihealueelle osuvien tekstien osuus kaikista teksteistä. Osumisprosentista tulostetaan myös kumulatiivinen osumaprosentti, lähtien heikoimmin tyypittyneestä tekstistä vahvimmin tyypittyneeseen (painojen
varianssi).

## Käyttö

Ohjelma toimii ajamalla run.py tiedosto. Ohjelma ottaa "aineisto" -hakemistosta [korp kielipankista](https://korp.csc.fi/) 
ladattuja json tiedostoja, jotka sisältävät suomi24 foorumin tekstejä.

Aineistossa on mukana esimerkkitiedostoja, mutta materiaalista tulee nopeasti varsin kookasta. Suomi24 materiaalia voi ladata
itse json -muodossa käyttämällä [Korp Web Service APIa](https://www.kielipankki.fi/support/korpapi/). Latauskoodia.txt sisältää
esimerkkejä sopivista latauspyynnöistä. Kohtaan "end=" annetaan haluttujen tekstien lukumäärä. Kohtaan "_.text_sub" taas annetaan
haluttu aihealue.
