# Lokalt lager för Google Merchant Center

Varje kväll (ca kl 19) hämtar en GitHub Action produktfeeden från mobilcenter.nu och skriver
`lokalt-lager.tsv` (butikskod, produkt-id, lagerstatus) för butiken Mobilcenter.
Merchant Center-kontot 539903714 hämtar filen varje natt till lagerkällan
"Mobilcenter Jönköping AB" för kostnadsfria lokala listningar.

Filens adress:
https://raw.githubusercontent.com/mobilcenter/lokalt-lager/main/lokalt-lager.tsv
