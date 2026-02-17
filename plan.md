# Assetto Corsa Car Modifier - Piano di Implementazione

## Obiettivo
Creare un'applicazione desktop Windows in Python con PyQt5/6 che permetta di modificare facilmente le auto di Assetto Corsa, con supporto per:
- Unpacking di file data.acd non criptati
- Modifica di componenti auto (motore, sospensioni, differenziali, peso, trazione, ecc.)
- Libreria di componenti pre-built gestibile tramite GUI
- Path: `C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\content\cars`

## Approccio Tecnico
- **Linguaggio**: Python 3.x
- **GUI Framework**: PyQt5/PyQt6
- **Gestione File**: Parsing di file .ini/.lut per dati auto
- **Storage Componenti**: JSON per libreria componenti pre-built
- **Unpacking**: Supporto per data.acd non criptati (formato QuickBMS)

## Workplan

### Fase 1: Setup Progetto e Struttura
- [ ] Inizializzare progetto Python con struttura modulare
- [ ] Configurare requirements.txt (PyQt5/6, configparser, json, matplotlib/pyqtgraph per grafici)
- [ ] Creare struttura cartelle: `/src`, `/gui`, `/core`, `/data`, `/components`
- [ ] Setup file di configurazione per path Assetto Corsa

### Fase 2: Core - File Manager e Parser
- [ ] Implementare classe CarFileManager per navigare cartella cars
- [ ] Implementare parser per file .ini (engine.ini, suspensions.ini, tyres.ini, etc.)
- [ ] Implementare parser per file .lut (lookup tables con coppie X|Y)
- [ ] Implementare writer per file .lut (mantenendo formato originale)
- [ ] Implementare classe LUTCurve per gestire curve (add/remove/edit points, interpolazione)
- [ ] Implementare funzione unpack data.acd non criptato (ricerca tool QuickBMS o implementazione custom)
- [ ] Implementare backup automatico prima delle modifiche
- [ ] Implementare validazione dati per evitare corruzioni

### Fase 3: Sistema Componenti Pre-Built
- [ ] Creare schema JSON per componenti (engine, suspension, differential, etc.)
- [ ] Implementare ComponentLibrary per gestire CRUD componenti
- [ ] Creare componenti di default (motori comuni, sospensioni, differenziali)
- [ ] Implementare sistema import/export componenti
- [ ] Implementare sistema di tag/categorie per componenti

### Fase 4: GUI - Finestra Principale
- [ ] Creare MainWindow con menu e toolbar
- [ ] Implementare browser auto (lista auto installate)
- [ ] Implementare ricerca/filtro auto (barra di ricerca rapida, filtri per potenza/peso/tipo)
- [ ] Implementare preview info auto (nome, marca, potenza, peso)
- [ ] Implementare selezione cartella Assetto Corsa custom
- [ ] Implementare barra di stato per feedback operazioni

### Fase 5: GUI - Editor Componenti Auto
- [ ] Creare tab "Motore" (potenza, coppia, limitatore, turbo, etc.)
- [ ] Creare tab "Sospensioni" (molle, ammortizzatori, geometria)
- [ ] Creare tab "Differenziale" (tipo, coast, power, preload)
- [ ] Creare tab "Trazione" (4WD, RWD, FWD con percentuali)
- [ ] Creare tab "Peso e Bilanciamento" (peso totale, distribuzione)
- [ ] Creare tab "Pneumatici" (composti, dimensioni)
- [ ] Creare tab "Aerodinamica" (downforce, drag)
- [ ] Implementare apply/reset per ogni sezione

### Fase 6: GUI - Libreria Componenti
- [ ] Creare finestra Component Library Manager
- [ ] Implementare lista componenti filtrabili per tipo
- [ ] Implementare anteprima dettagli componente
- [ ] Implementare form aggiungi/modifica componente
- [ ] Implementare eliminazione componente con conferma
- [ ] Implementare drag&drop o apply button per applicare componenti

### Fase 6.5: GUI - Editor Grafico Curve .lut ✅ COMPLETED
- [x] Creare widget CurveEditor con matplotlib/pyqtgraph integrato
- [x] Implementare visualizzazione grafica curve .lut (power.lut, coast.lut, etc.)
- [x] Implementare selezione e modifica punti esistenti (drag&drop su grafico)
- [x] Implementare aggiunta nuovi punti (click su grafico o form manuale)
- [x] Implementare eliminazione punti (selezione + delete key)
- [x] Implementare zoom e pan del grafico
- [x] Implementare griglia e labels assi (es: RPM vs kW per power.lut)
- [x] Implementare anteprima valori numerici tabella affianco al grafico
- [ ] Implementare smooth curve (interpolazione spline opzionale) - Future enhancement
- [x] Implementare import/export curve da altri file .lut
- [x] Implementare preset curve comuni (lineare, turbo lag, NA, etc.)
- [x] Integrare editor curve nel tab "Motore" per power.lut e coast.lut
- [ ] Supportare altri .lut (turbo.lut, ctrl.lut per elettronica, etc.) - Future enhancement

### Fase 7: Features Avanzate
- [ ] Implementare sistema confronto auto (side-by-side comparison)
- [ ] Implementare export configurazione auto custom
- [ ] Implementare import configurazione da altre auto
- [ ] Implementare ricerca/filtro auto per caratteristiche
- [ ] Implementare sistema undo/redo modifiche
- [ ] Investigare gestione sound motore (bank files, GUIDs)

### Fase 8: Testing e Refinement
- [ ] Testare su varie auto Assetto Corsa (stock e mod)
- [ ] Testare unpacking data.acd su file non criptati
- [ ] Verificare modifiche applicate correttamente in-game
- [ ] Implementare error handling robusto
- [ ] Ottimizzare performance caricamento auto
- [ ] Creare documentazione utente (README con screenshot)

### Fase 9: Packaging e Distribuzione
- [ ] Configurare PyInstaller per creare .exe standalone
- [ ] Testare .exe su sistema Windows pulito
- [ ] Creare installer (opzionale - Inno Setup)
- [ ] Preparare file README con istruzioni

## Note Tecniche

### Struttura File Assetto Corsa
```
assettocorsa/content/cars/
├── [car_name]/
│   ├── data.acd (criptato o non criptato)
│   ├── data/ (cartella unpacked)
│   │   ├── engine.ini
│   │   ├── suspensions.ini
│   │   ├── tyres.ini
│   │   ├── drivetrain.ini
│   │   ├── aero.ini
│   │   ├── car.ini
│   │   ├── electronics.ini
│   │   ├── brakes.ini
│   │   └── [altri .ini e .lut]
│   └── ui/
```

### File Chiave da Modificare
- **engine.ini**: Potenza, coppia, limitatore, turbo
- **suspensions.ini**: Molle, ammortizzatori, geometria
- **drivetrain.ini**: Differenziale, trazione (TRACTION_TYPE)
- **car.ini**: Peso, distribuzione peso, screen_name
- **tyres.ini**: Compound gomme, dimensioni
- **aero.ini**: Downforce, drag coefficient

### File .lut (Lookup Tables)
I file .lut contengono curve di dati con formato:
```
X_VALUE|Y_VALUE
```
Esempi comuni:
- **power.lut**: RPM|kW (curva di potenza motore)
- **coast.lut**: RPM|Nm (freno motore)
- **turbo.lut**: RPM|boost pressure
- **ctrl.lut**: Vari controlli elettronici
- **damage.lut**: Curve di danneggiamento componenti

L'editor grafico permetterà di visualizzare e modificare queste curve visualmente invece che editare valori numerici manualmente.

### Data.acd Unpacking
- File .acd non criptati sono archivi compressi
- Tool QuickBMS con script AC può unpackarli
- Alternativa: implementare unpacker custom se formato è semplice
- Verificare signature/header file per determinare se criptato

### Sound Motore
- File audio in formato .bank (FMOD)
- GUIDs in file sfx/ folder
- Modifica sound complessa, richiede tool esterni (FMOD Studio)
- Suggerimento: lasciare per versione futura

## Considerazioni di Sicurezza
- Sempre creare backup prima di modifiche
- Validare tutti i valori input (range sensati)
- Non modificare file criptati (rischio corruzione)
- Permettere ripristino da backup facilmente

## Estensioni Future
- Supporto per setup auto (track-specific configurations)
- Online repository componenti condivisi
- Integrazione con Content Manager (se possibile)
- Support per mod auto custom
- Export/import setup racing league
