# prolog-parser

prolog-parser is a recursive-descent parser (syntax analyzer and lexical analyzer) for a simplified version of prolog, it determines whether a given prolog program is correct, or whether it contains errors.<br>
The simplified grammar is shown below<br>

### Grammar in BNF (Backus-Naur Form)

- `<program>` -> `<clause-list> <query>` | `<query>`
- `<clause-list>` -> `<clause>` | `<clause> <clause-list>`
- `<clause>` -> `<predicate> .` | `<predicate> :- <predicate-list> .`
- `<query>` -> `?- <predicate-list> .`
- `<predicate-list>` -> `<predicate>` | `<predicate> , <predicate-list>`
- `<predicate>` -> `<atom>` | `<atom> ( <term-list> )`
- `<term-list>` -> `<term>` | `<term> , <term-list>`
- `<term>` -> `<atom>` | `<variable>` | `<structure>` | `<numeral>`
- `<structure>` -> `<atom> ( <term-list> )`
- `<atom>` -> `<small-atom>` | `' <string> '`
- `<small-atom>` -> `<lowercase-char>` | `<lowercase-char> <character-list>`
- `<variable>` -> `<uppercase-char>` | `<uppercase-char> <character-list>`
- `<character-list>` -> `<alphanumeric>` | `<alphanumeric> <character-list>`
- `<alphanumeric>` -> `<lowercase-char>` | `<uppercase-char>` | `<digit>`
- `<lowercase-char>` -> a | b | c | ... | x | y | z
- `<uppercase-char>` -> A | B | C | ... | X | Y | Z | \_
- `<numeral>` -> `<digit>` | `<digit> <numeral>`
- `<digit>` -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
- `<string>` -> `<character>` | `<character> <string>`
- `<character>` -> `<alphanumeric>` | `<special>`
- `<special>` -> + | - | \* | / | \ | ^ | ~ | : | . | ? | | # | $ | &

### Prerequisites

Input: Code Files to be parsed must be in the same directory named "1.txt", "2.txt".. (any number of files)<br>
Output: Output of the parser will be in a text file called parser_output.txt

### Credits

This has been developed by myself [_Ak_](https://www.akvn.xyz/), [_Yasir_](https://github.com/yaserAmmarJabar) , and [_Muath_](https://github.com/MuathZahir)
as part of our Programming Languages Course Project for Fall 2023
