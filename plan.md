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

### Fase 1: Setup Progetto e Struttura ✅ COMPLETED
- [x] Inizializzare progetto Python con struttura modulare
- [x] Configurare requirements.txt (PyQt5/6, configparser, json, matplotlib/pyqtgraph per grafici)
- [x] Creare struttura cartelle: `/src`, `/gui`, `/core`, `/data`, `/components`
- [x] Setup file di configurazione per path Assetto Corsa

### Fase 2: Core - File Manager e Parser ✅ COMPLETED
- [x] Implementare classe CarFileManager per navigare cartella cars
- [x] Implementare parser per file .ini (engine.ini, suspensions.ini, tyres.ini, etc.)
- [x] Implementare parser per file .lut (lookup tables con coppie X|Y)
- [x] Implementare writer per file .lut (mantenendo formato originale)
- [x] Implementare classe LUTCurve per gestire curve (add/remove/edit points, interpolazione)
- [x] Implementare funzione unpack data.acd con quickBMS
- [x] Implementare eliminazione automatica data.acd dopo modifica
- [x] Implementare backup automatico prima delle modifiche

### Fase 3: Sistema Componenti Pre-Built ✅ COMPLETED
- [x] Creare schema JSON per componenti (engine, suspension, differential, etc.)
- [x] Implementare ComponentLibrary per gestire CRUD componenti
- [x] Creare componenti di default (motori comuni, sospensioni, differenziali)
- [x] Implementare sistema import/export componenti
- [x] Implementare sistema di tag/categorie per componenti

### Fase 4: GUI - Finestra Principale ✅ COMPLETED
- [x] Creare MainWindow con menu e toolbar
- [x] Implementare browser auto (lista auto installate)
- [x] Implementare preview info auto (nome, marca, potenza, peso)
- [x] Implementare selezione cartella Assetto Corsa custom
- [x] Implementare barra di stato per feedback operazioni

### Fase 5: GUI - Editor Componenti Auto ✅ COMPLETED
- [x] Creare tab "Motore" (potenza, coppia, limitatore, turbo, etc.)
- [x] Creare tab "Sospensioni" (molle, ammortizzatori, geometria)
- [x] Creare tab "Drivetrain" (differenziale, trazione)
- [x] Creare tab "Peso e Bilanciamento" (peso totale, distribuzione)
- [x] Creare tab "Pneumatici" (composti, dimensioni)
- [x] Creare tab "Aerodinamica" (downforce, drag)
- [x] Implementare apply/reset per ogni sezione
- [x] aggiunta tasto open folder auto in explorer

### Fase 6: GUI - Libreria Componenti ✅ COMPLETED
- [x] Creare finestra Component Library Manager
- [x] Implementare lista componenti filtrabili per tipo
- [x] Implementare anteprima dettagli componente
- [x] Implementare form aggiungi/modifica componente
- [x] Implementare eliminazione componente con conferma
- [x] Implementare apply button per applicare componenti alle auto
- [x] Integrare import componenti nell'editor auto (bottoni "Import from Library")

### Fase 6.5: GUI - Editor Grafico Curve .lut ✅ COMPLETED
- [x] Creare widget CurveEditor con matplotlib/pyqtgraph integrato
- [x] Implementare visualizzazione grafica curve .lut (power.lut, coast.lut, etc.)
- [x] Implementare selezione e modifica punti esistenti (drag&drop su grafico)
- [x] Implementare aggiunta nuovi punti (click su grafico o form manuale)
- [x] Implementare eliminazione punti (selezione + delete key)
- [x] Implementare zoom e pan del grafico
- [x] Implementare griglia e labels assi (es: RPM vs HP per power.lut)
- [x] Implementare anteprima valori numerici tabella affianco al grafico
- [x] Implementare import/export curve da altri file .lut
- [x] Implementare preset curve comuni (lineare, turbo lag, NA, etc.)
- [x] Integrare editor curve nel tab "Motore" per power.lut e coast.lut

### Fase 6.7: Revisione Documentazione ✅ COMPLETED
- [x] Revisione progetto in base alla documentazione `assettocorsa_car_data_documentation.md`
- [x] Correzione unità di misura power.lut da kW a HP (§4.28, §10.3)
- [x] Correzione range STEER_RATIO per valori negativi (§4.1)
- [x] Aggiunta tipo trazione AWD2 al dropdown drivetrain (§4.3)
- [x] Fix parser LUT per commenti `;` e commenti inline (§10.2)
- [x] Aggiunta campi LIMITER_HZ e DEFAULT_TURBO_ADJUSTMENT al tab motore (§4.2)
- [x] Aggiunta sezione DAMAGE al tab motore (§4.2)
- [x] Aggiunta campo ADJUST_STEP al tab freni (§4.6)
- [x] Aggiornamento documentazione (README.md, plan.md)

### Fase 7: Features Avanzate
- [ ] implementare preview immagine dell'auto
- [ ] Implementare ricerca/filtro auto
- [ ] Implementare sistema undo/redo modifiche
- [ ] implementare calcolatore potenza/coppia in tempo reale basato su curve .lut e sul moltiplicatore turbo
- [ ] Implementare supporto per setup auto (track-specific configurations)
- [ ] implementare modifiche a cartella ui/ (nome auto in menu, icone, etc.)
- [ ] Supportare altri .lut, implementare un editor generico di lut per altri tipi di curve specifici per ogni macchina (es. traction_control.lut throttle.lut) ci deve essere quindi un selettore di lut disponibili e una sezione per modificarli - Future enhancement
- [ ] Implementare smooth curve (interpolazione spline opzionale) - Future enhancement
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

## Cartella Examples
La cartella `examples/` contiene dati reali di un'auto di Assetto Corsa per testing e reference:
- `examples/data/`: Cartella completa con tutti i file .ini e .lut di una vera auto AC
- `examples/data.acd`: File data.acd originale (per testing unpack)
- Utilizzata per testare parsing, modifica e validazione dei file
- Riferimento per struttura corretta dei file AC

## Estensioni Future
- Supporto per setup auto (track-specific configurations)
- Online repository componenti condivisi
- Integrazione con Content Manager (se possibile)
- Support per mod auto custom
- Export/import setup racing league
