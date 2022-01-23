**Głosowanie elektroniczne**

Mateusz Hojda, Jan Zych

**Kryptosystem Pailliera** to algorytm kryptografii asymetrycznej
wykorzystujący DCRA (decisional composite residuosity assumption) -
założenie, że mając daną liczbę złożoną $n$ i liczbę całkowitą $z$,
trudno jest znaleźć odpowiedź na pytanie, czy istnieje takie $y$, że
$z \equiv y^{n}\text{\ mod\ }n^{2}$.

Szyfr ten posiada własność homomorficzną - znając $E(m_{1})$, $E(m_{2})$
oraz klucz publiczny, można obliczyć $E(m_{1} + m_{2})$.

Algorytm generuje różne szyfrogramy dla takich samych tekstów jawnych,
dzięki wykorzystaniu liczby losowej $r$ podczas szyfrowania.

**Generowanie kluczy:**

1.  wybierz dwie (duże) liczby pierwsze $p$ i $q$ równej długości

2.  oblicz $n = pq$

3.  oblicz $g = n + 1$, $\lambda = \varphi(n)$,
    > $\mu = \varphi(n)^{- 1}\text{\ mod\ n}$, gdzie
    > $\varphi(n) = (p - 1)(q - 1)$

4.  klucz publiczny to $(n,\ g)$, klucz prywatny to $(\lambda,\ \mu)$

**Szyfrowanie:**

1.  niech $m$ będzie wiadomością, $0 \leq m < n$

2.  wybierz losowe $r$, $0 < r < n$

3.  oblicz szyfrogram $c = g^{m}r^{n}\text{\ mod\ }n^{2}$

**Deszyfrowanie:**

1.  niech $L(x) = \frac{x - 1}{n}$

2.  oblicz wiadomość
    > $m = L(c^{\lambda}\text{\ mod\ }n^{2}) \cdot \text{μ\ mod\ n}$

**Wykorzystanie w głosowaniu elektronicznym:**

Traktujemy głos każdego z głosujących jako listę zer i jedynek,
szyfrujemy je przy użyciu klucza publicznego, dzięki własności szyfru
Pailliera wygenerowane szyfrogramy różnią się od siebie, zapewnia to
anonimowość głosów - nie da się poznać głosu innej osoby porównując jej
szyfrogram z innymi w puli głosów, a także osoba głosująca, która nie
zna wartości losowej $r$ nie może ponownie odtworzyć szyfrogramu, dzięki
czemu nie może udowodnić na kogo oddała głos - uniemożliwia to
sprzedawanie głosów.

System umożliwia także weryfikację wyników głosowania, w sposób
nieujawniający poszczególnych głosów. Odbywa się to poprzez
udostępnienie wraz z wynikami głosowania listy zaszyfrowanych głosów,
klucza publicznego, a także iloczynu wszystkich wartości
$\text{r\ mod\ n}$ - dzięki temu każdy z głosujących może sprawdzić, czy
jego głos znajduje się w puli głosów uwzględnionych przy obliczaniu
wyników oraz korzystając z własności szyfru homomorficznego obliczyć
sumę udostępnionych szyfrogramów i porównać ją z wynikiem szyfrowania
udostępnionego wyniku (wykorzystuje się wtedy klucz publiczny i iloczyn
wszystkich wartości $\text{r\ mod\ n}$).

**Uruchomienie serwera (python flask):**

-   Instalacja wirtualnych środowisk: pip install venv

-   Utworzenie wirtualnego środowiska: python -m venv ./venv

-   Włączenie środowiska: linux - venv/bin/activate, windows -
    > .\\venv\\Scripts\\activate

-   Instalacja wymaganych pakietów: pip install wheel flask flask-login
    > flask-wtf mysql-connector-python bcrypt pycryptodome

-   Uruchomienie serwera:

    -   cd \<folder z aplikacją\>

    -   windows - set FLASK\_APP=run.py && set FLASK\_DEBUG=1, linux -
        > export FLASK\_APP=run.py; export FLASK\_DEBUG=1

    -   flask run \--host=0.0.0.0

    -   strona dostępna pod adresem
        > [[http://localhost:5000]{.underline}](http://localhost:5000)

**Użytkownicy w bazie danych:**

Konfiguracja połączenia z bazą mysql znajduje się w pliku bcrypt.py.

Tabela "users" powinna zawierać kolumny (pesel, salt, password). Hasła
są hashowane bcryptem z solą.
