# Kulki

Program symulujący zachowanie się gazu doskonałego w szczelnie zamkniętym zbiorniku.

## Informacje wstępne

Główny interfejs programu jest konsolowy. Z jego poziomu możliwe jest uruchomienie komend, które wykonają określone zadania związane z symulacją. Na chwilę obecną wspierane są trzy komendy:

- **simulation** - uruchamia pojedynczą symulację
- **multisimulation** - uruchamia serię symulacji, według ustawień zawartych w pliku konfiguracyjnym; wyniki tych symulacji zapisywane są do pliku
- **plot** - rysuje wykresy na podstawie wyników wygenerowanych przez komendę *multisimulation*

## Dokładniejsze omówienie poszczególnych komend

### simulation

Każda symulacja może zostać uruchomiona na dwa sposoby: jako zwyczajna, matematyczna symulacja, lub jako wizualizacja - domyślną jest pierwsza z nich. Wizualizacja tym różni się od zwyczajnej symulacji, że pozwala zaobserwować lot atomów *na żywo*, odbywa się to niestety kosztem szybkości. Aby włączyć wizualizację, należy użyć parametru `--visual`.

Symulacje są wysoce konfigurowalne. Program zawiera pewną domyślną konfigurację, którą można jednak rozszerzyć (lub też przysłonić pewne domyślne opcje) przy pomocy własnego pliku konfiguracyjnego. W tym celu należy użyć parametru `--config <plik>`.

Domyślnie, pozycje oraz prędkości początkowe poszczególnych atomów są losowane przy uruchomieniu każdej kolejnej symulacji. Możliwe jest jednak zapisanie którejś z nich, a następnie odtworzenie. Służą do tego podkomendy `load <plik>` oraz `save [plik]`. W przypadku podkomendy load, argument `<plik>` jest obligatoryjny, a w przypadku save niekoniecznie - jeżeli nie zostanie podany, wtedy symulacja zostanie zapisana do pliku z aktualną datą i godziną w nazwie. Nie należy stosować opcji `--config` w przypadku podkomendy `load` - zostanie ona zwyczajnie zignorowana.

Po zakończeniu każdej symulacji na standardowe wyjście wypisywane są jej wyniki. Domyślna postać jest czytelna dla człowieka, a niekoniecznie dla komputera. Możliwe jest wypisanie tych wyników w formacie JSON. Aby to zrobić, należy skorzystać z parametru `--json`.

#### Przykłady

- `kulki simulation --config config.json --json`
- `kulki simulation --visual --config config.json save`
- `kulki simulation --visual save plik.json`
- `kulki simulation load plik.json`

### multisimulation

W przypadku komendy simulation podanie pliku konfiguracyjnego było obcjonalne - w tym przypadku jest jednak inaczej. Należy skonfigurować przynajmniej dwie opcje: 

- `simulation_max_frames` - czas trwania symulacji w klatkach - jest to potrzebne, ponieważ symulacje są uruchamiane w trybie wsadowym i użytkownik nie ma możliwości ich przerwania w trakcie działania; istotne jest również, aby te symulacje trwały tyle samo,
- `multisimulation_balls_number_sequence` - trzyelementowa lista, która określa ile kulek będzie pojawiało się w kolejnych symulacjach; pierwszy element oznacza wartość początkową, drugi element to krok, natomiast trzeci to całkowita liczba symulacji wykonywana w ramach trybu wsadowego.

Poza konfiguracją należy podać jako argument ścieżkę do pliku, w którym mają zostać zapisane wyniki symulacji.

#### Przykłady

Plik config.json

```json
{
    "simulation_max_frames": 3000,
	"multisimulation_balls_number_sequence": [10, 10, 10]
}
```

`kulki multisimulation --config config.json wyniki.json`

### plot

Jedynym argumentem, jaki należy podać, jest ścieżka do pliku z wynikami symulacji.

#### Przykłady

`kulki plot wyniki.json`

## Okno wizualizacji

Podczas uruchomienia komendy `simulation` z parametrem `--visual` wyświetlane jest okno wizualizacji. Cała jego przestrzeń jest odwzorowaniem przestrzeni symulacji, nie posiada innych elementów interfejsu. Okna nie można rozszerzać - jego rozmiar musi zostać określony w konfiguracji, przed uruchomieniem symulacji.

Okno zamknąć można, standardowo, poprzez przycisk *X* na belce tytułowej okna. Można to również zrobić wciskając klawisz `Esc`. Zamknięcie okna skutkuje zakończeniem symulacji i wypisaniem jej wyników.

Symulację można zapauzować (i analogicznie, powrócić do jej wykonania) wciskając klawisz `P` (*pause*).

Jeżeli uznaliśmy obecną symulację za interesującą, a nie wywołaliśmy komendy z parametrem `save`, nie wszystko stracone. Można to zrobić także w trakcie działania symulacji (pod warunkiem, że jest to symulacja z wizualizacją). Wystarczy wcisnąć klawisz `S` (*save*).

Symulację można również przewijać do przodu oraz do tyłu. W tym celu służą odpowiednio klawisze `F` (*forward*) i `B` (*back*).
