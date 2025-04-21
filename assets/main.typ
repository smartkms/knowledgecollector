#set page(
  paper: "presentation-16-9",
)
#set text(font: "Fira Sans")

#show heading.where(level: 1): set text(size: 60pt)
#show heading.where(level: 2): set text(size: 40pt)
#set text(size: 20pt)

#let liveAction = true
#let fancyGradient = if liveAction {gradient.linear(teal, aqua)} else {teal}


#let slide(body, main: false) = {
  set page(background: block(width: 100%, height: 100%, fill: if main {fancyGradient} else {white}))
  show heading: set text(fill: if main {white} else {fancyGradient})
  block(
    height: 100%,
    body
  )
}

#slide(main:true)[
  #grid(
    rows: (1fr, 1fr, 1fr),
    [], [
      = Typst
      #show heading.where(level: 2): set text(size: 30pt)
      == Kratek uvod v delovanje
    ], []
  )
]

#slide[
  == Kaj je Typst?
  #v(20pt)

  - Po besedah avtorjev: New markup-based typesetting system that is designed to be as powerful as LaTeX while being much easier to learn and use.

  - Torej:
    + Super razmerje med močjo in enostavnostjo za uporabo
    + Mogoče sprogramirati tudi zelo kompleksne stvari, ko je potrebno
    + Enostaven _templating_
    + Hitro generiranje dokumentov
    + Majhna končna velikost dokumentov

]

#slide(main:false)[
  == Razvoj
  #v(20pt)

  - Typst je dokaj mlada tehnologija, a je za mnogo primerov uporabe že stabilna
  - Open source, `Apache-2.0` licenca, pripada nemškemu podjetju
  - Trenutni release je `0.13`, nove verzije pridejo vsakih 4-5 mesecev

  - Nedavni novi featurji:
   - Font subsetting
   - Multithreading
   - Embeddanje poljubnih datotek v končni PDF (npr. XML za e-račun)
]

#let jsonData = json("data.json")
#let fonts = ("Clicker ScriptSans", "Fira Mono", "Permanent Marker")

#slide[
  == Demostracija
  #v(20pt)

  Oseba #underline[#jsonData.name], starost #jsonData.age let, ima v namišljenem informacijskem sistemu dodeljeno naslednjo kartoteko:

  #table(
    columns: (auto, auto),
    inset: 16pt,
    table.cell([*Ime in priimek*]),
    table.cell([#jsonData.name]),
    table.cell([*Starost*]),
    table.cell([#jsonData.age]),
    table.cell([*Hišni ljubljenčki*]),
    table.cell(
      grid(
        row-gutter: 12pt,
        columns: (1fr),
        ..(jsonData.pets).zip(fonts).map(x => [
          #set text(font: x.at(1))
          #x.at(0)
        ])
      )

    )
  )
]

#slide[
  == Koristni viri
  #v(20pt)

  + Typst dokumentacija: #link("https://typst.app/docs/")
  + Typst Universe: #link("https://typst.app/universe")
  + Typst Discord (link na spletni strani)
]

// #set page(paper: "us-letter")
// aaa
