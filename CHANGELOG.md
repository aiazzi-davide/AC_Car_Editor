# Changelog

## [0.1.0] - 2026-02-20

Prima versione pubblica di AC Car Editor.

### Funzionalità

- **Browser auto**: elenco di tutte le auto installate in Assetto Corsa con filtro/ricerca e preview immagine
- **Unpacking automatico** di file `data.acd` non criptati tramite quickBMS
- **Editor auto** con 7 schede:
  - **Engine**: RPM limits, limiter frequency, turbo boost, wastegate, soglie di danno motore
  - **Suspension**: spring rate, damper fast/slow bump/rebound, rod length, camber, toe
  - **Drivetrain**: tipo trazione (RWD/FWD/AWD/AWD2), differenziale, gearbox, clutch
  - **Weight & Fuel**: massa totale, inerzia, CG, sterzo, carburante
  - **Aerodynamics**: sezioni WING dinamiche con CD/CL e angolo
  - **Brakes**: coppia massima, bilanciamento, handbrake, regolazione cockpit
  - **Pneumatici**: selezione compound, dimensioni (width/radius/rim), grip (DX0/DY0), pressione ideale
- **Editor grafico curve .lut** (power.lut, coast.lut):
  - Grafico matplotlib interattivo con zoom/pan
  - Drag-and-drop punti
  - Aggiunta/rimozione punti via form o tastiera
  - Preset curve (Linear, Turbo Lag, NA, V-Shape Coast)
  - Import/export verso altri file .lut
- **Calcolatore Potenza/Coppia** in tempo reale con effetto turbo boost visualizzato
- **Gear Ratio Editor**: spinbox per ogni marcia (R, 1-10) con stima velocità massima per marcia e 4 preset (Street 5-speed, Sport 6-speed, Race 6-speed, Drift 6-speed)
- **RTO File Manager**: gestione `final.rto` e `ratios.rto` con import da libreria (3 preset finali, 3 preset rapporti) e stima velocità
- **UI Metadata Editor**: modifica `ui_car.json` (nome, brand, classe, tags, specs, autore)
- **Stage Tuning**: upgrade con un click Stage 1/2/3, logica differenziata NA vs Turbo
- **Setup Manager**: salvataggio/caricamento preset setup per tracciato specifico
- **Component Library**: libreria di componenti riutilizzabili (motori, sospensioni, gomme, rapporti) con CRUD via GUI
- **Restore Backup**: pulsante per ripristinare l'ultima modifica dai file `.bak`
- **Layout 2 colonne** con pulsanti +/- dedicati per ogni campo numerico
- **Tema grafico moderno** con palette blu/slate, toast notifications, collapsible groups
- **Disclaimer di compatibilità** all'avvio (con opzione "Non mostrare più")
- **Apertura cartella backup** dal menu File
