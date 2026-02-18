# Assetto Corsa – Documentazione Struttura Dati delle Auto

> **Scopo:** Guida di riferimento per lo sviluppo di un'applicazione che legge e modifica i dati delle auto di Assetto Corsa. Questa documentazione copre la struttura completa della cartella di un'auto, tutti i file presenti nella cartella `/data` estratta da `data.acd`, e i formati file utilizzati.

---

## 1. Struttura della Cartella di un'Auto

Ogni auto si trova in:
```
assettocorsa/content/cars/<nome_auto>/
```

### File e cartelle principali

```
<nome_auto>/
├── data.acd                  ← Archivio criptato contenente la cartella /data
├── data/                     ← Cartella estratta da data.acd (se presente)
│   └── *.ini, *.lut, *.rto  ← File di configurazione fisica e grafica
├── ui/
│   ├── ui_car.json           ← Metadati per il menu di selezione auto
│   └── badge.png             ← Icona del brand (256x256 px)
├── skins/
│   └── <nome_skin>/          ← Una cartella per ogni livrea
│       ├── ui_skin.json
│       ├── skin.ini
│       ├── preview.jpg
│       ├── livery.png
│       └── *.dds             ← Texture DDS della livrea
├── sfx/
│   └── <nome_auto>.bank      ← Audio FMOD
├── extension/
│   ├── ext_config.ini        ← Configurazione CSP (Custom Shaders Patch)
│   ├── script.lua            ← Script Lua (opzionale, per CSP)
│   ├── assets/               ← Asset grafici per CSP
│   ├── fonts/                ← Font per strumentazione CSP
│   └── sounds/               ← Suoni aggiuntivi CSP
├── animations/               ← Animazioni .ksanim
├── texture/                  ← Texture condivise del modello
├── <nome_auto>.kn5           ← Modello 3D principale
├── <nome_auto>_LOD_B.kn5     ← LOD di distanza media
├── <nome_auto>_LOD_C.kn5     ← LOD distante
├── <nome_auto>_LOD_D.kn5     ← LOD molto distante
├── collider.kn5              ← Mesh di collisione fisica
├── driver_base_pos.knh       ← Posizione base del pilota
├── logo.png                  ← Logo dell'auto (400x200 px)
├── body_shadow.png           ← Ombra statica della carrozzeria
└── tyre_N_shadow.png         ← Ombra statica dei pneumatici (0-3)
```

---

## 2. Il File `data.acd`

`data.acd` è un archivio binario proprietario che contiene tutti i file della cartella `/data`. Assetto Corsa carica i dati fisici **direttamente** da questo archivio. Se esiste anche una cartella `/data/` estratta nella stessa directory, AC la usa al posto dell'`.acd` (comportamento utile per il modding).

**Implicazione per l'applicazione:**
- Il programma estrae `data.acd` → cartella `/data/`
- I file `.ini`, `.lut`, `.rto` estratti vengono modificati
- Per applicare le modifiche, i file modificati devono essere **riconfezionati** in `data.acd` oppure la cartella `/data/` estratta deve essere lasciata presente (AC la riconoscerà)

---

## 3. Formato dei File di Dati

### 3.1 File `.ini` (INI standard)

Formato testo con sezioni `[SEZIONE]` e coppie `CHIAVE=VALORE`. I commenti iniziano con `;`.

```ini
[SEZIONE]
CHIAVE=valore        ; commento opzionale
ALTRA_CHIAVE=1.5
```

### 3.2 File `.lut` (Lookup Table)

File testo con coppie `INPUT|OUTPUT` su ogni riga. Definiscono curve di mappatura non lineari.

```
0|0
1000|120
5000|250
7500|180
```

- La prima colonna è l'ingresso (es. RPM, temperatura, usura)
- La seconda colonna è l'uscita (es. potenza in HP, coefficiente grip)
- AC interpola linearmente tra i punti

### 3.3 File `.rto` (Ratio File)

Elenco di rapporti disponibili per il setup. Ogni riga: `VALORE|VALORE` (stesso valore ripetuto).

```
4.90|4.90
4.63|4.63
4.08|4.08
```

---

## 4. File nella Cartella `/data`

### 4.1 `car.ini` – Parametri Generali dell'Auto

**Sezioni principali:**

```ini
[HEADER]
VERSION=2               ; versione formato file

[INFO]
SCREEN_NAME=Nissan Silvia PS13   ; nome visualizzato nel gioco
SHORT_NAME=PS13                  ; abbreviazione

[BASIC]
GRAPHICS_OFFSET=0.0,-0.37,-0.08 ; offset grafico X,Y,Z tra centro fisica e modello 3D
GRAPHICS_PITCH_ROTATION=-0.2    ; rotazione pitch del modello (gradi)
TOTALMASS=1270                  ; massa totale in kg (con pilota e senza carburante)
INERTIA=1.83,1.18,4.72          ; inerzia rotazionale X,Y,Z in kg·m²

[GRAPHICS]
DRIVEREYES=-0.346,0.907,-0.337  ; posizione occhi pilota X,Y,Z (per camera onboard)
ONBOARD_EXPOSURE=15             ; esposizione camera interna
OUTBOARD_EXPOSURE=30            ; esposizione camera esterna
ON_BOARD_PITCH_ANGLE=-5.3       ; angolo pitch camera onboard (gradi)
BUMPER_CAMERA_POS=0,0.04,1.97   ; posizione camera bumper X,Y,Z
BONNET_CAMERA_POS=0,0.58,0.52   ; posizione camera cofano X,Y,Z
MIRROR_POSITION=0.0,1.3,0.5    ; posizione specchietto retrovisore
USE_ANIMATED_SUSPENSIONS=0      ; 1=usa animazioni sospensioni

[CONTROLS]
FFMULT=1.8                      ; moltiplicatore forza force feedback
STEER_ASSIST=0.80               ; assistenza sterzo (0-1)
STEER_LOCK=450                  ; angolo massimo volante in gradi (totale, non metà)
STEER_RATIO=-9.8                ; rapporto sterzo (negativo = inversione lato)

[FUEL]
CONSUMPTION=0.00125             ; consumo carburante (litri per metro per 1.0 throttle)
FUEL=45                         ; carburante iniziale in litri
MAX_FUEL=50                     ; capacità serbatoio massima in litri

[PIT_STOP]
TYRE_CHANGE_TIME_SEC=10         ; secondi per cambio gomme al pit
FUEL_LITER_TIME_SEC=0.6         ; secondi per ogni litro di carburante
BODY_REPAIR_TIME_SEC=20         ; secondi per riparazione carrozzeria
ENGINE_REPAIR_TIME_SEC=2        ; secondi per riparazione motore
SUSP_REPAIR_TIME_SEC=30         ; secondi per riparazione sospensioni
```

---

### 4.2 `engine.ini` – Motore

```ini
[HEADER]
VERSION=1
POWER_CURVE=power.lut           ; file LUT curva di potenza (RPM→HP o Nm)
COAST_CURVE=FROM_COAST_REF      ; tipo curva frenata motore: FROM_COAST_REF, COAST_DATA, o file .lut

[ENGINE_DATA]
ALTITUDE_SENSITIVITY=0.1        ; perdita potenza per altitudine (0=nessuna, 1=massima)
INERTIA=0.15                    ; inerzia volano in kg·m²
LIMITER=7500                    ; giri limitatore RPM (0 = disabilitato)
LIMITER_HZ=30                   ; frequenza attivazione limitatore in Hz
MINIMUM=750                     ; RPM minimo (al minimo)
DEFAULT_TURBO_ADJUSTMENT=0.7    ; regolazione turbo predefinita se regolabile dal cockpit

[COAST_REF]                     ; usato se COAST_CURVE=FROM_COAST_REF
RPM=7600                        ; RPM di riferimento per la coppia di freno motore
TORQUE=90                       ; coppia di freno motore in Nm a quel RPM
NON_LINEARITY=0                 ; 0=lineare, 1=esponenziale

[TURBO_0]                       ; sezione turbocompressore (più turbo: TURBO_1, TURBO_2...)
LAG_DN=0.980                    ; inerzia pressione in calo (0-1, vicino a 1 = più lento)
LAG_UP=0.982                    ; inerzia pressione in salita
MAX_BOOST=1.3                   ; pressione massima in bar
WASTEGATE=1.3                   ; pressione wastegate in bar
DISPLAY_MAX_BOOST=1.3           ; valore mostrato nel cockpit
REFERENCE_RPM=2600              ; RPM a cui il boost raggiunge il massimo
GAMMA=2.7                       ; curva di risposta del turbo
COCKPIT_ADJUSTABLE=1            ; 1=regolabile dal cockpit

[DAMAGE]
TURBO_BOOST_THRESHOLD=1.5       ; soglia boost oltre cui il motore si danneggia
TURBO_DAMAGE_K=5                ; danno al secondo per (boost - threshold)
RPM_THRESHOLD=8000              ; RPM sopra cui il motore si danneggia
RPM_DAMAGE_K=1                  ; danno al secondo per RPM > soglia
```

**File `power.lut`:** Mappa `RPM|PotenzaHP` (o Nm). Esempio:
```
0|40
1000|83
5000|163
7500|120
```

---

### 4.3 `drivetrain.ini` – Trasmissione

Il comportamento varia in base alla versione del formato (`[HEADER] VERSION`) e al tipo di trazione.

```ini
[HEADER]
VERSION=3                       ; versione formato (3 = abilita AWD2, AUTO_SHIFTER, ecc.)

[TRACTION]
TYPE=RWD                        ; FWD, RWD, AWD, AWD2

[GEARS]
COUNT=6                         ; numero marce avanti
GEAR_R=-3.382                   ; rapporto retromarcia
GEAR_1=3.321                    ; rapporto 1ª marcia
GEAR_2=1.902                    ; ... fino a GEAR_N
FINAL=4.08                      ; rapporto finale (coppia conica)

[DIFFERENTIAL]                  ; differenziale posteriore (RWD/AWD)
POWER=1.0                       ; bloccaggio differenziale in trazione (0-1)
COAST=1.0                       ; bloccaggio differenziale in rilascio (0-1)
PRELOAD=200                     ; precarico differenziale in Nm

; Se TYPE=AWD aggiungere:
[DIFFERENTIAL_FRONT]
POWER=0.0
COAST=0.0
PRELOAD=5
[DIFFERENTIAL_CENTER]
POWER=0.70
COAST=0.15

; Se TYPE=AWD2 (solo con VERSION=3) — AWD avanzato con controller:
[AWD2]
FRONT_DIFF_POWER=0.10
FRONT_DIFF_COAST=0.10
FRONT_DIFF_PRELOAD=2
CENTRE_RAMP_TORQUE=1600         ; coppia rampa differenziale centrale (Nm)
CENTRE_MAX_TORQUE=2304
REAR_DIFF_POWER=0.40
REAR_DIFF_COAST=0.25
REAR_DIFF_PRELOAD=2

[GEARBOX]
CHANGE_UP_TIME=200              ; tempo cambio salita in millisecondi
CHANGE_DN_TIME=280              ; tempo cambio discesa in millisecondi
AUTO_CUTOFF_TIME=0              ; taglio automatico gas in upshift (ms, 0=disabilitato)
SUPPORTS_SHIFTER=1              ; 1=supporta cambio H-pattern
VALID_SHIFT_RPM_WINDOW=900      ; finestra RPM per ingaggio marcia
CONTROLS_WINDOW_GAIN=0.4        ; fattore rev-matching per innesto (0=difficile)
INERTIA=0.01                    ; inerzia cambio in kg·m²

[CLUTCH]
MAX_TORQUE=600                  ; coppia massima frizione in Nm

[AUTOCLUTCH]
UPSHIFT_PROFILE=NONE            ; profilo frizione automatica in salita (NONE=disabilitato)
DOWNSHIFT_PROFILE=DOWNSHIFT_PROFILE
MIN_RPM=1000                    ; RPM minimi per frizione automatica
MAX_RPM=3000                    ; RPM massimi per frizione automatica
FORCED_ON=0                     ; 1=frizione automatica forzata (non disabilitabile)

[AUTOBLIP]
ELECTRONIC=0                    ; 1=feature auto, non disabilitabile
LEVEL=0.7                       ; livello gas per il blip

; Sezioni opzionali (solo con VERSION=3):
[AUTO_SHIFTER]                  ; cambio automatico
UP=7000                         ; RPM cambio automatico salita
DOWN=3000                       ; RPM cambio automatico discesa
SLIP_THRESHOLD=0.95
GAS_CUTOFF_TIME=0.30

[DOWNSHIFT_PROTECTION]          ; protezione da overrev in scalata
ACTIVE=1
OVERREV=200                     ; RPM di tolleranza sopra il limitatore
LOCK_N=1                        ; 1=blocca il cambio se la marcia è troppo bassa

[DAMAGE]                        ; danno cambio
RPM_WINDOW_K=100                ; finestra RPM per calcolo danno cambio (Nm/RPM)
```

---

### 4.4 `suspensions.ini` – Sospensioni

```ini
[HEADER]
VERSION=2

[BASIC]
WHEELBASE=2.475                 ; passo in metri
CG_LOCATION=0.53                ; posizione CoG longitudinale (0=avantreno, 1=retrotreno)

[ARB]
FRONT=26000                     ; rigidità barra antirollio anteriore (N/m)
REAR=9000                       ; rigidità barra antirollio posteriore

[FRONT]                         ; configurazione sospensione anteriore
TYPE=STRUT                      ; tipo: STRUT (MacPherson), DWB (doppio braccio), AXLE
BASEY=-0.12                     ; altezza base sospensione in metri dal CoG
TRACK=1.50                      ; carreggiata in metri
ROD_LENGTH=0.05                 ; lunghezza bieletta di regolazione altezza
HUB_MASS=50                     ; massa del mozzo/freno in kg
RIM_OFFSET=-0.015               ; offset visuale cerchio rispetto alla posizione fisica

; Geometria punti di attacco (specifici per tipo STRUT):
STRUT_CAR=0.12,0.37,-0.04
STRUT_TYRE=0.037,-0.122,0.019
WBCAR_BOTTOM_FRONT=0.413,-0.138,0.37
; ...

TOE_OUT=-0.00015                ; convergenza (negativo=convergenza, positivo=divergenza) in radianti
STATIC_CAMBER=-4.0              ; camber statico in gradi (negativo=inclinato verso l'interno)

SPRING_RATE=79436               ; rigidità molla in N/m
PROGRESSIVE_SPRING_RATE=8000   ; componente progressiva della molla
BUMP_STOP_RATE=50000            ; rigidità bump-stop
BUMPSTOP_UP=0.09                ; corsa bump-stop estensione in m
BUMPSTOP_DN=0.03                ; corsa bump-stop compressione in m
PACKER_RANGE=0.18               ; corsa totale disponibile in m

DAMP_BUMP=10000                 ; smorzamento in compressione lenta (N·s/m)
DAMP_FAST_BUMP=9000             ; smorzamento in compressione veloce
DAMP_FAST_BUMPTHRESHOLD=0.1    ; soglia velocità per passaggio slow/fast (m/s)
DAMP_REBOUND=11000              ; smorzamento in estensione lenta
DAMP_FAST_REBOUND=13000         ; smorzamento in estensione veloce
DAMP_FAST_REBOUNDTHRESHOLD=0.1 ; soglia velocità estensione slow/fast

[REAR]                          ; stessa struttura di [FRONT] ma con TYPE=DWB
; Per DWB vengono usati:
WBCAR_TOP_FRONT=...             ; punto attacco braccio superiore (lato telaio, anteriore)
WBCAR_TOP_REAR=...              ; punto attacco braccio superiore (lato telaio, posteriore)
WBCAR_BOTTOM_FRONT=...
WBCAR_BOTTOM_REAR=...
WBTYRE_TOP=...                  ; punto attacco braccio superiore (lato mozzo)
WBTYRE_BOTTOM=...
WBCAR_STEER=...                 ; punto attacco tirante sterzo (lato telaio)
WBTYRE_STEER=...                ; punto attacco tirante sterzo (lato mozzo)

[GRAPHICS_OFFSETS]              ; offset visivi (non fisici) per allineamento grafico
WHEEL_LF=-0.01                  ; offset ruota anteriore sinistra
SUSP_LF=-0.01
; etc.
```

---

### 4.5 `tyres.ini` – Pneumatici

Definisce uno o più set di gomme (compounds). Il compound di default è indicato da `[COMPOUND_DEFAULT]`.

```ini
[HEADER]
VERSION=10

[COMPOUND_DEFAULT]
INDEX=1                         ; indice del compound predefinito (0-based)

[FRONT]                         ; compound 0 anteriore (INDEX non specificato = compound 0)
NAME=Eco
SHORT_NAME=E
WIDTH=0.225                     ; larghezza in metri
RADIUS=0.300                    ; raggio esterno in metri
RIM_RADIUS=0.242                ; raggio cerchio in metri
ANGULAR_INERTIA=1.0             ; inerzia rotazionale pneumatico in kg·m²
DAMP=500                        ; smorzamento pneumatico
RATE=263372                     ; rigidità radiale pneumatico in N/m
DY0=1.2588                      ; coefficiente grip laterale di picco
DY1=-0.050                      ; degradazione grip laterale con carico
DX0=1.2673                      ; coefficiente grip longitudinale di picco
DX1=-0.056                      ; degradazione grip longitudinale con carico
WEAR_CURVE=tyre_wear_dwg.lut    ; curva usura (distanza percorsa → grip rimanente %)
SPEED_SENSITIVITY=0.003623      ; riduzione grip ad alta velocità
RELAXATION_LENGTH=0.07253       ; lunghezza di rilassamento (risposta al cambio direzione)
ROLLING_RESISTANCE_0=9          ; resistenza al rotolamento costante
ROLLING_RESISTANCE_1=0.00099    ; resistenza al rotolamento quadratica (velocità)
ROLLING_RESISTANCE_SLIP=4698    ; componente slip della resistenza
FLEX=0.000874                   ; flessibilità del battistrada
CAMBER_GAIN=0.116               ; guadagno di grip per grado di camber
DCAMBER_0=1.1                   ; dipendenza D dal camber (lineare)
DCAMBER_1=-13                   ; dipendenza D dal camber (quadratica)
FRICTION_LIMIT_ANGLE=8.79       ; angolo limite di attrito in gradi
XMU=0.28                        ; coefficiente di aderenza combinata
PRESSURE_STATIC=32              ; pressione statica (fredda) in PSI
PRESSURE_IDEAL=37               ; pressione ottimale di esercizio in PSI
PRESSURE_SPRING_GAIN=8112       ; aumento rigidità per PSI
PRESSURE_FLEX_GAIN=0.45         ; variazione flex per PSI
PRESSURE_D_GAIN=0.004           ; variazione grip con pressione
FZ0=2274                        ; carico verticale di riferimento in N
LS_EXPY=0.8227                  ; esponente load sensitivity laterale
LS_EXPX=0.8901                  ; esponente load sensitivity longitudinale
DX_REF=1.26                     ; grip longitudinale di riferimento
DY_REF=1.25                     ; grip laterale di riferimento
FALLOFF_LEVEL=0.92              ; livello di grip quando il pneumatico scivola oltre il picco
FALLOFF_SPEED=4                 ; velocità di decadimento dopo il picco
CX_MULT=1.025                   ; moltiplicatore rigidità laterale

[REAR]                          ; stesso formato di [FRONT] per pneumatico posteriore

; Compound successivi: [FRONT_1]/[REAR_1], [FRONT_2]/[REAR_2], ecc.

[THERMAL_FRONT]                 ; parametri termici anteriori (associati al compound 0)
SURFACE_TRANSFER=0.0150         ; velocità riscaldamento dalla strada (0-1)
PATCH_TRANSFER=0.00027          ; trasferimento calore interno al pneumatico
CORE_TRANSFER=0.00035           ; trasferimento calore verso l'aria interna
FRICTION_K=0.045                ; quantità di slip che diventa calore
ROLLING_K=0.15                  ; resistenza al rotolamento che diventa calore
PERFORMANCE_CURVE=tcurve_DWG.lut ; file LUT temperatura→grip
GRAIN_GAIN=0.3                  ; tendenza alla graining (granulazione)
BLISTER_GAIN=0.33               ; tendenza alle bolle (blistering)
COOL_FACTOR=2.5                 ; velocità raffreddamento

[THERMAL_REAR]                  ; stesso formato per posteriore
```

**File `tyre_wear_*.lut`:** Mappa `distanza_km|grip_%`.  
**File `tcurve_*.lut`:** Mappa `temperatura°C|coefficiente_grip`.

> **Nota sui nomi dei file LUT:** Il nome dei file LUT per usura e termica varia a seconda del pack/autore. Esempi: `tyre_wear_dwg.lut`, `tsujigiri_300_wear_curve.lut`, `street_front.lut`, `tire_VentusR_295_35_18_lat.lut`. Fare sempre riferimento alle chiavi `WEAR_CURVE=` e `PERFORMANCE_CURVE=` nel `tyres.ini` per trovare i file effettivamente usati.

---

### 4.6 `brakes.ini` – Freni

```ini
[HEADER]
VERSION=1

[DATA]
MAX_TORQUE=2400                 ; coppia frenante massima totale in Nm
FRONT_SHARE=0.695               ; percentuale frenata all'avantreno (0-1)
HANDBRAKE_TORQUE=1600           ; coppia freno a mano in Nm
COCKPIT_ADJUSTABLE=1            ; 1=bias regolabile dal cockpit
ADJUST_STEP=0.5                 ; step di regolazione bias
```

---

### 4.7 `aero.ini` – Aerodinamica

Definisce elementi aerodinamici (`WING_N`) e pinne (`FIN_N`).

```ini
[HEADER]
VERSION=3

[WING_0]
NAME=BODY                       ; nome identificativo (BODY, FRONT, REAR)
CHORD=1                         ; corda alare in metri (profondità)
SPAN=1.73                       ; apertura alare in metri (larghezza)
POSITION=0,0.23,-0.20           ; posizione X,Y,Z dal CoG in metri
LUT_AOA_CL=wing_body_AOA_CL.lut ; LUT angolo attacco → coefficiente portanza
LUT_AOA_CD=wing_body_AOA_CD.lut ; LUT angolo attacco → coefficiente resistenza
CL_GAIN=0                       ; moltiplicatore CL
CD_GAIN=1                       ; moltiplicatore CD
ANGLE=1                         ; angolo di attacco iniziale in gradi
; Zone danno (influenza CL/CD in base al danno per zona):
ZONE_FRONT_CL=0
ZONE_FRONT_CD=0.005
ZONE_REAR_CL=0
ZONE_REAR_CD=0.005

[WING_1]                        ; ulteriori elementi: WING_1, WING_2, ...
; ...

[FIN_0]                         ; pinna laterale (genera forza laterale in yaw)
NAME=FIN
CHORD=1.35
SPAN=0.55
POSITION=0,0.22,-0.55
LUT_AOA_CL=fin_AOA_CL.lut
LUT_AOA_CD=fin_AOA_CD.lut
YAW_CL_GAIN=-0.0                ; guadagno CL per angolo di yaw
```

**File `wing_*_AOA_CL.lut`:** Mappa `angolo_attacco_gradi|CL`.
**File `wing_*_AOA_CD.lut`:** Mappa `angolo_attacco_gradi|CD`.

---

### 4.8 `electronics.ini` – Elettronica

Il file può contenere varie sezioni in base al livello di tecnologia dell'auto.

```ini
; --- ABS (due varianti, dipende dal VERSION) ---
[ABS_V2]                        ; formato moderno
SLIP_RATIO_LIMIT=0.12           ; limite slip ratio prima dell'intervento ABS
PRESENT=1                       ; 1=ABS presente sull'auto
ACTIVE=1                        ; 1=ABS attivo di default
RATE_HZ=150                     ; frequenza aggiornamento ABS in Hz

[ABS]                           ; formato legacy (auto più vecchie)
SLIP_RATIO_LIMIT=0.12
PRESENT=1
ACTIVE=1

; --- Traction Control ---
[TC]                            ; versione semplice
SLIP_RATIO=0.15
PRESENT=1
ACTIVE=1

[TRACTION_CONTROL]              ; versione avanzata (nohesituned, gmp, ecc.)
SLIP_RATIO_LIMIT=0.08
CURVE=traction_control.lut      ; (opzionale) LUT livello_TC→slip_ratio_limit
PRESENT=1
ACTIVE=1
RATE_HZ=200
MIN_SPEED_KMH=30                ; velocità minima per attivazione TC (km/h)

; --- EDL – Electronic Differential Lock ---
[EDL]                           ; differenziale elettronico (mod avanzati)
PRESENT=1
ACTIVE=1
MAX_SPIN_POWER=0.8              ; spin massimo ruota in trazione (0-1)
MAX_SPIN_COAST=0.3              ; spin massimo ruota in rilascio (0-1)
BRAKE_TORQUE_POWER=100          ; coppia frenante EDL in trazione (Nm)
BRAKE_TORQUE_COAST=600          ; coppia frenante EDL in rilascio (Nm)
DEAD_ZONE_POWER=0.21            ; zona morta in trazione (0-1)
DEAD_ZONE_COAST=0.2             ; zona morta in rilascio (0-1)

; --- DRS ---
[DRS]                           ; (se presente) Drag Reduction System
PRESENT=1
```

---

### 4.9 `setup.ini` – Parametri di Setup

Definisce tutti i parametri configurabili dal menu di setup in-game.

```ini
[DISPLAY_METHOD]
SHOW_CLICKS=1                   ; 1=mostra il numero di click

[GEARS]
USE_GEARSET=1                   ; 1=usa set di marce predefiniti; 0=slider individuali

; Ogni sezione definisce un parametro di setup:
[PRESSURE_LF]
SHOW_CLICKS=0
TAB=TYRES                       ; tab del menu (TYRES, ALIGNMENT, DAMPERS, SUSPENSION, DRIVETRAIN, GENERIC, FUEL)
NAME=Pressure LF                ; etichetta visualizzata
MIN=10                          ; valore minimo
MAX=60                          ; valore massimo
STEP=1                          ; incremento per click
POS_X=0.5                       ; posizione nel layout UI
POS_Y=2

; Parametri setup comuni:
; [PRESSURE_LF/RF/LR/RR]       - pressione gomme
; [CAMBER_LF/RF/LR/RR]         - camber
; [TOE_OUT_LF/RF/LR/RR]        - convergenza
; [DAMP_BUMP_LF/RF/LR/RR]      - smorzamento compressione
; [DAMP_REBOUND_LF/RF/LR/RR]   - smorzamento estensione
; [SPRING_RATE_LF/RF/LR/RR]    - rigidità molle
; [ROD_LENGTH_LF/RF/LR/RR]     - altezza da terra (via bieletta)
; [ARB_FRONT / ARB_REAR]       - rigidità barre antirollio
; [DIFF_POWER/COAST/PRELOAD]   - differenziale
; [FRONT_BIAS]                  - ripartizione frenata
; [FUEL]                        - litri di carburante
; [BRAKE_POWER_MULT]           - potenza freni

[GEAR_SET_0]                    ; se USE_GEARSET=1, definisce set di rapporti
NAME=OEM_S13/S14_5spd
GEAR_1=3.321
GEAR_2=1.902
; ...

[FINAL_GEAR_RATIO]
RATIOS=final.rto                ; file .rto con i rapporti finali disponibili
```

**File `final.rto`:** Lista di rapporti finali selezionabili. Formato: `VALORE|VALORE`.
**File `ratios.rto`:** Lista di rapporti cambio alternativi.

---

### 4.10 `lods.ini` – Livelli di Dettaglio

```ini
[COCKPIT_HR]
DISTANCE_SWITCH=200             ; distanza (m) oltre cui si disattiva la cockpit HR

[LOD_0]
FILE=s13.kn5                    ; file KN5 per LOD 0 (più vicino)
IN=0                            ; distanza minima (m)
OUT=1000                        ; distanza massima (m)

[LOD_1]                         ; LOD 1 (distanza media) - opzionale
FILE=s13_LOD_B.kn5
IN=40
OUT=500
```

---

### 4.11 `cameras.ini` – Telecamere Onboard

Ogni sezione `[CAMERA_N]` definisce una telecamera onboard.

```ini
[CAMERA_0]
POSITION=0.035,1.242,-0.012     ; posizione X,Y,Z relativa al CoG
FORWARD=0.021,-0.232,0.972      ; vettore direzione (normalizzato)
UP=0.005,0.972,0.232            ; vettore "su" (normalizzato)
FOV=65                          ; campo visivo in gradi
EXPOSURE=30                     ; esposizione
EXTERNAL_SOUND=1                ; 1=usa audio esterno
```

---

### 4.12 `lights.ini` – Luci

```ini
[LIGHT_N]
NAME=<nome_mesh_nel_KN5>        ; mesh da illuminare
COLOR=210,210,210               ; colore RGB (0-255) da moltiplicare per la mesh

[BRAKE_N]
NAME=<nome_mesh>
COLOR=33,0,0                    ; colore attivo
OFF_COLOR=0,0,0                 ; colore spento
```

---

### 4.13 `ai.ini` – Comportamento AI

```ini
[HEADER]
VERSION=3

[GEARS]
UP=7150                         ; RPM cambio salita AI
DOWN=4700                       ; RPM cambio discesa AI
SLIP_THRESHOLD=0.95             ; soglia slip per il controllo AI
GAS_CUTOFF_TIME=0.300           ; tempo taglio gas AI in secondi

[PEDALS]
GASGAIN=4.0                     ; aggressività pedale gas
BRAKE_HINT=1
TRAIL_HINT=1

[STEER]
STEER_GAIN=1.76                 ; fattore sterzo AI

[LOOKAHEAD]
BASE=18.6                       ; distanza lookahead base in metri
```

---

### 4.14 `sounds.ini` – Parametri Audio

```ini
[ENGINE]
POSITION=front                  ; posizione motore: front, mid, rear

[SKIDS]
ENTRY_POINT=0.35                ; soglia slip per l'attivazione suono sgommate
MIX_VOLUME=0.4                  ; volume globale
PITCH_BASE=0.50
PITCH_GAIN=0.25

[WIND]
SPEED_GAIN_0=0.0062             ; guadagno volume per km/h
SPEED_GAIN_1=0.000025           ; guadagno volume per (km/h)²
VOLUME_GAIN=0.98                ; volume massimo
PITCH_REFERENCE=95              ; velocità di riferimento pitch (km/h)
PITCH_GAIN=0.58

[TYRE_ROLLING]
SPEED_GAIN_0=0
SPEED_GAIN_1=0.000035
VOLUME_GAIN=0.95
PITCH_REFERENCE=105
PITCH_GAIN=0.45

[BACKFIRE]
MAXGAS=0.3                      ; posizione gas massima per backfire
MINRPM=1000
MAXRPM=15000
TRIGGERGAS=0.8
VOLUME_IN=0.9                   ; volume interno
VOLUME_OUT=0.7                  ; volume esterno
```

---

### 4.15 `damage.ini` – Sistema di Danno

```ini
[SCRATCHES]
MAX_SPEED=20                    ; velocità massima graffi in km/h
MIN_SPEED=0

[DAMAGE]
INITIAL_LEVEL=20                ; livello di danno iniziale (0-100)

[VISUAL_OBJECT_N]               ; oggetti visivi che si deformano con i danni
NAME=bumper_FR                  ; nome mesh nel KN5
STATIC_ROTATION_AXIS=-1,1,1    ; asse di rotazione statica dopo danno
STATIC_ROTATION_ANGLE=6        ; angolo di rotazione statica in gradi
DAMAGE_ZONE=FRONT               ; zona: FRONT, REAR, LEFT, RIGHT
MIN_SPEED=20                    ; velocità minima impatto per danno (km/h)
FULL_SPEED=50                   ; velocità per danno massimo
OSCILLATION_MIN_ANGLE=0
OSCILLATION_MAX_ANGLE=5
```

---

### 4.16 `colliders.ini` – Collisori Fisici

```ini
[COLLIDER_N]
CENTRE=0,-0.20,-0.05            ; centro del box di collisione X,Y,Z dal CoG
SIZE=1.2,0.08,3.4               ; dimensioni box X,Y,Z in metri
```

---

### 4.17 `mirrors.ini` – Specchietti

```ini
[MIRROR_N]
NAME=<nome_mesh_specchio>       ; nome del piano specchio nel KN5
```

---

### 4.18 `driver3d.ini` – Modello Pilota

```ini
[MODEL]
NAME=driver_dwg1                ; nome del modello pilota (in /content/driver/)
POSITION=0,0,0.5                ; offset posizione X,Y,Z

[STEER_ANIMATION]
NAME=steer.ksanim               ; file animazione volante
LOCK=360                        ; gradi massimi animazione volante

[SHIFT_ANIMATION]
BLEND_TIME=100                  ; durata blend animazione cambio (ms)
POSITIVE_TIME=300               ; durata fase positiva
STATIC_TIME=102
NEGATIVE_TIME=300
PRELOAD_RPM=6870                ; RPM per animazione anticipazione cambio
INVERT_SHIFTING_HANDS=1         ; 1=inverte mano per cambio

[HIDE_OBJECT_N]
NAME=DRIVER:RIG_Head            ; oggetti da nascondere nel modello pilota
```

---

### 4.19 `fuel_cons.ini` – Consumo Carburante

```ini
[FUEL_EVAL]
KM_PER_LITER=0.638364           ; chilometri per litro (autonomia stimata)
```

---

### 4.20 `flames.ini` – Fiamme di Scarico

```ini
[HEADER]
BURN_FUEL_MULT=2                ; moltiplicatore consumo durante le fiamme
FLASH_THRESHOLD=3               ; soglia luminosità flash

[FLAME_N]
POSITION=0.512,0.187,-2.282     ; posizione fiamma X,Y,Z
DIRECTION=0.206,0.113,-0.971    ; direzione unitaria fiamma
VSIZE_START=1.3                 ; dimensione verticale iniziale
VSIZE_END=0.4                   ; dimensione verticale finale
LSIZE=0.6                       ; dimensione laterale
SIZE_MULT=3                     ; moltiplicatore dimensione
IS_LEFT=1                       ; 1=scarico sinistro
GROUP=0                         ; gruppo di appartenenza
```

---

### 4.21 `ambient_shadows.ini` – Ombra Statica

```ini
[SETTINGS]
WIDTH=0.95                      ; larghezza ombra statica in metri
LENGTH=2.7                      ; lunghezza ombra statica in metri
```

---

### 4.22 `escmode.ini` – Camera Pit Lane

```ini
[SETTINGS]
POSITION=0,1.4,3.2              ; posizione camera rotazione 360° nel pit X,Y,Z
FOV=45                          ; campo visivo in gradi
```

---

### 4.23 `dash_cam.ini` – Camera Cruscotto

```ini
[DASH_CAM]
POS=-0.346,0.907,-0.337         ; posizione camera cruscotto X,Y,Z
EXP=33                          ; esposizione
```

---

### 4.24 `proview_nodes.ini` – Nodi Vista Pro

File opzionale che definisce nodi di visibilità per la modalità pro-camera. Generalmente vuoto o con configurazioni specifiche.

---

### 4.25 `digital_instruments.ini` – Strumenti Digitali

Configurazione degli strumenti digitali nel cockpit (display LCD, LED shift indicator, warning lights). Può essere vuoto (per auto senza strumenti digitali) o molto ricco. Vedi il dettaglio nella sezione §8b (Pack `gmp` → *Strumentazione digitale avanzata*).

---

### 4.26 `analog_instruments.ini` – Strumenti Analogici

Configurazione degli aghi (needle mesh) degli strumenti analogici nel cockpit. Vedi il dettaglio nella sezione §8b (*Strumentazione analogica completa*).

---

### 4.27 `suspension_graphics.ini` – Grafica Sospensioni

Definisce i nodi grafici delle sospensioni animate. Se vuoto, AC usa le impostazioni di default da `suspensions.ini`.

---

### 4.28 File `.lut` Aggiuntivi

| File | Descrizione |
|------|-------------|
| `power.lut` | `RPM\|HP` – Curva di potenza motore |
| `throttle.lut` | `input%\|output%` – Mappatura pedale gas |
| `throttle2.lut` | `input%\|output%` – Mappa gas secondaria (mappe motore alt.) |
| `tyre_wear_*.lut` | `km\|grip%` – Curva usura pneumatico (nome varia per pack) |
| `tcurve_*.lut` | `temperatura°C\|grip_coeff` – Curva termica pneumatico |
| `wing_*_AOA_CL.lut` | `angolo_gradi\|CL` – Portanza aerodinamica |
| `wing_*_AOA_CD.lut` | `angolo_gradi\|CD` – Resistenza aerodinamica |
| `analog_rpm_curve.lut` | `RPM\|gradi_ago` – Calibrazione contagiri analogico |
| `analog_speed_curve.lut` | `km/h\|gradi_ago` – Calibrazione tachimetro analogico |
| `analog_turbo_curve.lut` | `bar\|gradi_ago` – Calibrazione manometro turbo |
| `traction_control.lut` | `livello_TC\|slip_ratio` – Curva custom TC |
| `difflock_gear_mult.lut` | `marcia\|moltiplicatore` – Bloccaggio diff per marcia |
| `difflock_brake_mult.lut` | `freno_0-1\|moltiplicatore` – Bloccaggio diff per freno |
| `fuelmaps.lut` | `"Nome"\|indice` – Tipi carburante selezionabili |
| `gear_start.lut` | `marcia\|coppia_Nm` – Coppia massima al via per marcia |
| `wing_controller_speed.lut` | `km/h\|angolo_gradi` – Angolo alettone controllato da velocità |

---

## 5. File UI

### 5.1 `ui/ui_car.json`

Metadati dell'auto visualizzati nel menu di selezione.

```json
{
  "name": "Toyota GT86",
  "brand": "Toyota",
  "description": "Testo descrittivo con tag HTML (</br> per a capo)...",
  "tags": ["#small sports", "rwd", "manual", "street", "japan"],
  "class": "street",
  "specs": {
    "bhp": "200bhp",
    "torque": "205Nm",
    "weight": "1250kg",
    "topspeed": "233km/h",
    "acceleration": "7.6s 0-100",
    "pwratio": "6.25kg/hp",
    "range": 640
  },
  "torqueCurve": [
    ["0", "0"],
    ["1000", "138"],
    ["7000", "192"]
  ],
  "powerCurve": [
    ["0", "0"],
    ["7000", "200"]
  ]
}
```

**Classi auto valide:** `street`, `sport`, `race`, `gt`, `touring`, `drift`, `drag`, `open_wheel`, `rally`

---

## 6. File Skins

### 6.1 `skins/<nome_skin>/ui_skin.json`

```json
{
  "skinname": "Nome Livrea",
  "drivername": "Nome Pilota",
  "country": "IT",
  "team": "Nome Team",
  "number": "86",
  "priority": 15
}
```

### 6.2 `skins/<nome_skin>/skin.ini`

Configura gli accessori visuali del pilota per questa livrea.

```ini
[driver_no_HANS]
SUIT=\sparco\black
GLOVES=\sparco_roadcars_rg3.1\black
HELMET=\helmet_base_yellow\3

[CREW]
SUIT=\type1\yellow_white
HELMET=\yellow
BRAND=\toyota2
```

### 6.3 Texture della Skin

| File | Descrizione |
|------|-------------|
| `Skin.dds` | Texture principale carrozzeria (diffuse map) |
| `Plate_D.dds` | Texture targa (diffuse) |
| `Plate_NM.dds` | Texture targa (normal map) |
| `metal_detail.dds` | Texture dettaglio metallo |
| `ac_crew.dds` | Texture tuta meccanici |
| `livery.png` | Anteprima livrea piccola (512x512) |
| `preview.jpg` | Anteprima livrea grande per il menu |

---

## 7. Cartella `extension/` (CSP – Custom Shaders Patch)

La cartella `extension/` è utilizzata dal mod **Custom Shaders Patch** (CSP) e non è letta dalla versione base di AC.

### 7.1 `extension/ext_config.ini`

File di configurazione CSP con centinaia di opzioni. Struttura base:

```ini
[INCLUDE]
INCLUDE=common/selflighting.ini, common/materials_glass.ini  ; include file comuni CSP

[BASIC]
IS_LOW_BEAM_AVAILABLE=1
HEADLIGHTS_ARE_HEADLIGHTS=1
ENGINE_STALLED_RPM_THRESHOLD=200

[DATA]
DISABLE_LIGHTSINI=1             ; 1=disabilita lights.ini nativo, usa CSP lighting

[REAL_MIRROR_N]
FOV=14.85                       ; campo visivo specchio
FLIP=1
ASPECT_MULT=0.5

[LIGHTING]
EMISSIVE_MULT=1                 ; moltiplicatore emissività globale

[PARTICLES_FX_EXHAUST_N]
POSITION=x,y,z                  ; posizione uscita scarico per effetti particelle
DIRECTION=x,y,z

[EXHAUST_FLAMES]
LIMITER=7500                    ; RPM limitatore per fiamme
ANTILAG=0                       ; 1=abilita fiamme antilag

[SHADER_REPLACEMENT_...]        ; sostituisce shader materiali specifici
MESHES=nome_mesh
MATERIALS=nome_materiale
PROP_...=ksEmissive,2.5

[AUDIO_VOLUME]
ENGINE_EXT=1.1
ENGINE_INT=1.0
```

---

## 8. Logica di Caricamento AC

1. AC cerca prima la cartella `/data/` estratta
2. Se non trovata, carica da `data.acd`
3. **La presenza di `/data/` ha priorità su `data.acd`**

**Per modificare un'auto:**
- Estrarre `data.acd` → `/data/`
- Modificare i file `.ini`/`.lut`/`.rto` desiderati
- Lasciare la cartella `/data/` presente (AC la userà automaticamente)
- Per un'installazione "pulita", riconfezionare in `data.acd` tramite tool appositi

---

## 8b. Variazioni tra Pack di Mod

I mod per Assetto Corsa hanno storie e autori diversi. La cartella `/data` può contenere file extra o seguire convenzioni di naming differenti da pack a pack. Di seguito le differenze osservate ispezionando i principali pack installati.

---

### Pack `dthwsh` (DriftWorks/DriftHouse)
File LUT gomme con prefisso del brand del creatore:
- `tyre_wear_dwg.lut` – curva usura DWG
- `tyre_tcurve_dwg.lut` / `tcurve_DWG.lut` – curva termica DWG

---

### Pack `swarm`
File aggiuntivi rispetto alla base:
- **`blurred_objects.ini`** – Definisce mesh 3D che si sostituiscono ai cerchi ad alta velocità per simulare il blur (solitamente vuoto se non usato)
- **`flame_presets.ini`** – Preset visivi per le fiamme di scarico (posizione, dimensione, tipo texture, colore RGBA)
- **`analog_instruments.ini`** – Configurazione strumentazione analogica completa (vedi §4.31)
- **`drs.ini`** – File DRS (spesso vuoto, indica che il sistema è presente ma non attivo)

---

### Pack `nstyle`
File aggiuntivi:
- **`extra_animations.ini`** – Oggetti rotanti extra nel modello 3D (es. ventole, turbine):
```ini
[ROTATING_OBJECT_N]
NAME=nome_mesh      ; nome del mesh nel KN5
RPM=155             ; giri di rotazione visivi (non fisici)
AXIS=0,1,0          ; asse di rotazione X,Y,Z
```
- **`blurred_objects.ini`** – Blur cerchi (spesso vuoto)
- **`analog_instruments.ini`** – Strumenti analogici

---

### Pack `bw` (BW/Baku Works)
File aggiuntivi:
- **`analog_turbo_curve.lut`** – Mappa `pressione_bar|posizione_ago_tachimetro` per il manometro turbo analogico
- **`analog_speed_curve.lut`** – Mappa `velocita_kmh|posizione_ago_tachimetro` per il tachimetro analogico
- **`drs.ini`** – File DRS (spesso vuoto)
- **`cameras.ini.candidate`** – File candidato/backup per le telecamere; NON viene caricato da AC (suffisso `.candidate`)
- **LUT gomme named after brand**: es. `Zestino_front.lut`, `Zestino_rear.lut` (curve usura per marca gomma specifica)
- LUT comuni: `tsujigiri_tcurve.lut`, `tsujigiri_300_wear_curve.lut`, `tsujigiri_200_wear_curve.lut`

---

### Pack `nohesituned`
Pack con fisica avanzata e più compound. File aggiuntivi notevoli:

**Gomme con LUT separate per anteriore/posteriore:**
- `tcurve_street.lut`, `tcurve_semis.lut`, `tcurve_front.lut`, `tcurve_rear.lut`, `tcurve_p_hard.lut`, `tcurve_pslick.lut`
- `street.lut`, `street_front.lut`, `street_rear.lut`, `semislicks.lut`, `semislicks_front.lut`, ecc.
- `pslick_front.lut`, `pslick_rear.lut`, `p_hard_front.lut`, `p_hard_rear.lut`
- **`__cm_tyre_wearcurve_front_N.lut`** / **`__cm_tyre_wearcurve_rear_N.lut`** – File generati automaticamente da **Content Manager** (non usati da AC; CM li genera per le sue visualizzazioni). Il prefisso `__cm_` identifica file di CM.
- **`__cm_tyre_perfcurve_front_N.lut`** / **`__cm_tyre_perfcurve_rear_N.lut`** – Stessa origine, curva prestazioni CM.

**Elettronica avanzata** (`electronics.ini`):
```ini
[TRACTION_CONTROL]
SLIP_RATIO_LIMIT=0.08
CURVE=traction_control.lut   ; curva custom TC (slip_ratio_level→limit)
PRESENT=1
ACTIVE=1
RATE_HZ=200
MIN_SPEED_KMH=30

[EDL]                         ; Electronic Differential Lock
PRESENT=1
ACTIVE=1
MAX_SPIN_POWER=0.8
MAX_SPIN_COAST=0.3
BRAKE_TORQUE_POWER=100
BRAKE_TORQUE_COAST=600
DEAD_ZONE_POWER=0.21
DEAD_ZONE_COAST=0.2
```

**`traction_control.lut`** – Mappa `livello_TC (0-1)|slip_ratio_limit`.

**Differenziale con LUT:**
- **`difflock_gear_mult.lut`** – Mappa `marcia|moltiplicatore_bloccaggio_diff`
- **`difflock_brake_mult.lut`** – Mappa `pressione_freno (0-1)|moltiplicatore_bloccaggio_diff`

**Carburante multiplo:**
- **`fuelmaps.lut`** – Lista tipi carburante disponibili: `"Nome Carburante"|indice`. Esempio:
```
93 Octane|0
E85|1
Ignite e90|2
```

**`gear_start.lut`** – Mappa `marcia|coppia_massima_al_via` (launch control/partenza).

**`analog_speed_curve.lut`** – Calibrazione tachimetro.

**Cambio automatico** (`drivetrain.ini`):
```ini
[AUTO_SHIFTER]
UP=7000                      ; RPM cambio automatico salita
DOWN=3000                    ; RPM cambio automatico discesa
SLIP_THRESHOLD=0.95
GAS_CUTOFF_TIME=0.30
```

**`DAMAGE` nel drivetrain:**
```ini
[DAMAGE]
RPM_WINDOW_K=100             ; finestra RPM per calcolo danno cambio
```

---

### Pack `gmp` (GMP – modder con fisica di altissimo livello)
Il pack `gmp_bnr34_the_inevitable` è un esempio di mod con fisica molto avanzata, incluso AWD programmabile, ERS, freni termici e script Lua.

**Trazione AWD2** (`drivetrain.ini`):
```ini
[TRACTION]
TYPE=AWD2                    ; trazione integrale avanzata con controller programmabili

[AWD2]
FRONT_DIFF_POWER=0.10
FRONT_DIFF_COAST=0.10
FRONT_DIFF_PRELOAD=2
CENTRE_RAMP_TORQUE=1600     ; coppia rampa differenziale centrale
CENTRE_MAX_TORQUE=2304
REAR_DIFF_POWER=0.40
REAR_DIFF_COAST=0.25
REAR_DIFF_PRELOAD=2
```

**Sistema di controllo con controller** (`ctrl_*.ini`):
I file `ctrl_NomeSistema.ini` definiscono controller programmabili per differenziale AWD, ERS, freni, sterzo. Struttura:
```ini
[CONTROLLER_N]
INPUT=AXLES_DIFFERENCE_ABSOLUTE  ; input: RPMS, GAS, LATG, SPEED_KMH, CONST,
                                  ; AXLES_DIFFERENCE_ABSOLUTE, REAR_AXLE_DIFFERENCE_ABSOLUTE
COMBINATOR=ADD                    ; come combinare con il precedente: ADD, MULT
LUT=nome_file.lut                 ; LUT per trasformare l'input
FILTER=0.90                       ; filtro temporale (inerzia, 0-1)
UP_LIMIT=1772.5                   ; limite superiore output
DOWN_LIMIT=0                      ; limite inferiore output
CONST_VALUE=3.545                 ; valore costante (solo se INPUT=CONST)
```
File controller trovati: `ctrl_awd2.ini`, `ctrl_4ws.ini`, `ctrl_ebb.ini`, `ctrl_ers_0.ini`...`ctrl_ers_5.ini`, `ctrl_turbo0.ini`, `ctrl_turbo1.ini`, `ctrl_4ws_hicas_options.ini`

**Freni termici** (`brakes_temp.ini`):
```ini
[HEADER]
VERSION=2
[_EXTENSION]
ENABLE=1
USE_ADVANCED_SYSTEM=0       ; 0=solo riscaldamento, 1=sistema completo

[DATA]
MAX_TORQUE=3276
FRONT_SHARE=0.793
; ...

[TEMPS_FRONT]
COOL_TRANSFER=0.00265       ; raffreddamento da aria statica
TORQUE_K=0.60               ; fattore coppia per generazione calore
PERF_CURVE=brakes_tcurve_front_r33_brembo.lut  ; temperatura→coefficiente attrito
COOL_SPEED_FACTOR=0.00      ; raffreddamento da aria in movimento
COOL_SPEED_FACTOR_0=0.05
CORE_TRANSFER_IN=0.050      ; trasferimento calore superficie→nucleo
CORE_TRANSFER_OUT=0.800
CORE_TRANSFER_AIR=0.0005

[TEMPS_REAR]                ; stesso formato
```

**Sistema ERS** (`ers.ini`):
```ini
[HEADER]
VERSION=1

[KINETIC]
CHARGE_K=0.0001             ; coefficiente di carica cinetica
TORQUE_CURVE=LC_RPM_Torque.lut
COAST_CURVE=LC_RPM_Coast.lut
DISCHARGE_TIME=30000000     ; tempo di scarica in ms
HAS_BUTTON_OVERRIDE=1
MAX_KJ_PER_LAP=30000000
DEFAULT_CONTROLLER=0
BRAKE_REAR_CORRECTION=50

[HEAT]
CHARGE_K=0.001
TORQUE_PERC=20

[COCKPIT_CONTROLS]
RECOVERY=0
DELIVERY_PROFILE=1
MGU_H_MODE=0
```

**Script Lua nella cartella `/data`** (`script.lua`):
Alcuni mod includono uno script Lua direttamente in `/data/` (non solo in `/extension/`). Questo script viene eseguito da CSP e permette logica custom (nitrous, danno motore, ecc.):
```lua
function script.update(dt)
    local nitrousActive = car.extraA and car.speedKmh > 10
    if nitrousActive then
        ac.addForce(vec3(0,0,-2), true, vec3(0,0,nitrousForce), true)
    end
end
```

**Aerodinamica con Ground Height (GH):**
Alcune auto (gmp) usano LUT `*_GH_CL.lut` e `*_GH_CD.lut` per variare il coefficiente aerodinamico in base all'altezza da terra. I file `LUT_GH_CL` e `LUT_GH_CD` in `aero.ini` fanno riferimento a queste LUT.

**Nomi LUT gomme specifici per marca/misura:**
- `tire_VentusR_295_35_18_lat.lut` / `_long.lut`
- `tire_RE040_lat_245_40_18.lut` / `_long.lut`
- `tire_R888R_295_30_18_lat.lut` / `_long.lut`
- `tire_ccurve_road_3deg.lut`, `_4deg.lut`, `_5deg.lut` (curve camber)
- `tire_camber_spring_k_*.lut` (rigidità laterale per larghezza gomma)
- `tire_heat_road_80_mu.lut`, `_speed.lut`, `_level.lut` (modello termico)

**File multipli per varianti dello stesso modello** (es. R32/R33/R34):
- `ctrl_awd2_r32.ini`, `ctrl_awd2_r33.ini`, `ctrl_awd2_r34.ini`
- `digital_instruments_HKS.ini`, `digital_instruments_NoHKS.ini`
- `ers.ini`, `ers_r33.ini`

**`wing_controller_speed.lut`** (presente in `traffic_crown_vic`):
Mappa `velocità_kmh|angolo_alettone` per attivazione dinamica dell'alettone in funzione della velocità (usato in `wing_animations.ini` con tipo CONTROLLER).

**`throttle2.lut`** – Curva gas secondaria (usata per mappe motore alternative).

---

### Strumentazione digitale avanzata (`digital_instruments.ini`)

Nei mod più elaborati questo file può essere molto ricco:

```ini
[FUEL_WARNING_0]
OBJECT_NAME=dash_fuel         ; mesh oggetto da illuminare
EMISSIVE=100,9,0, 0.001       ; colore emissivo quando ATTIVO
DIFFUSE=0
INVERTED=0
FUEL_SWITCH=12                ; litri sotto cui si attiva

[ITEM_N]                      ; elemento testo display digitale
PARENT=DISPLAY_DATA           ; oggetto genitore nel KN5
POSITION=x,y,z
TYPE=PLACE_HOLDER             ; tipo: PLACE_HOLDER (dato numerico), CLOCK, RPM, SPEED, ecc.
TEXT=0                        ; testo statico (se TYPE non è dinamico)
SIZE=0.0090                   ; dimensione font
COLOR=1,1,1
INTENSITY=3
FONT=digital_big              ; font file nella cartella fonts/
VERSION=2
ALIGN=RIGHT                   ; RIGHT, LEFT, CENTER

[LED_N]                       ; LED shift indicator
OBJECT_NAME=rev_indicator
RPM_SWITCH=7700               ; RPM attivazione LED
EMISSIVE=20,1,1, 255          ; colore emissivo attivo
DIFFUSE=1
BLINK_SWITCH=8200             ; RPM inizio lampeggio
BLINK_HZ=8                    ; frequenza lampeggio
```

---

### Strumentazione analogica completa (`analog_instruments.ini`)

```ini
[SPEED_INDICATOR]
OBJECT_NAME=s14int_needle_speed   ; mesh dell'ago nel KN5
ZERO=0.000                        ; rotazione in gradi a velocità zero
STEP=1.222222                     ; gradi di rotazione per ogni km/h

[RPM_INDICATOR]
OBJECT_NAME=s14int_needle_tach
ZERO=0
MIN_VALUE=0
STEP=0.024                        ; gradi per RPM
OBJECT_NAME_MAX=                  ; mesh opzionale per marcatura massima

[TURBO_INDICATOR]
OBJECT_NAME=s14int_defi_needle_boost
ZERO=91
STEP=270
MIN_VALUE=0.0
USE_BAR=1                         ; 1=usa bar, 0=usa valore raw

[WATER_TEMP]
OBJECT_NAME=s14int_needle_temp
ZERO=0
STEP=-0.43
MIN_VALUE=50
LUT=(50=29|70=8|120=-28|150=-43)  ; LUT inline: temperatura|posizione_ago

[OIL_TEMP]
OBJECT_NAME=s14int_defi_needle_oiltemp
ZERO=96
MIN_VALUE=85
STEP=2.7

[FUEL_INDICATOR]
OBJECT_NAME=s14int_needle_fuel
ZERO=0
MIN_VALUE=0
STEP=1.38
```

File LUT separati per calibrazione:
- **`analog_rpm_curve.lut`** – `RPM|gradi_ago`
- **`analog_speed_curve.lut`** – `km/h|gradi_ago`
- **`analog_turbo_curve.lut`** – `pressione_bar|gradi_ago`

---

### File `flame_presets.ini`

Preset visivi per le fiamme di scarico. Definisce texture di fiamma in più fasi:

```ini
[HEADER]
SIZE_MULT=1                   ; moltiplicatore dimensione globale

[PRESET_START_N]              ; fase di avvio fiamma
TRIGGER=0                     ; indice frame
OFFSET=0.0,0.0,0.02           ; offset posizione X,Y,Z
SIZE=0.06                     ; dimensione texture
TYPE=0                        ; 0=F-type (f2.dds), 1=X-type (x0.dds), 2=altro
RGB=255,180,15,0.2            ; colore R,G,B + intensità

[PRESET_END_N]                ; fase di spegnimento fiamma

[PRESET_LOOP_N]               ; fase ciclica (fiamma continua)

[PRESET_FLASH_N]              ; flash rapido
```

---

### File `drs.ini`

Se **non vuoto**, definisce un sistema DRS (Drag Reduction System):

```ini
[SLOT_0]
WING=1                        ; indice wing in aero.ini da azionare
ACTIVATIONS_PER_LAP=99
DETECTION_ZONE=last_checkpoint
DETECTION_TIME=1.0
ACTIVATION_ZONE=drs_zone
CLOSE_ON_BRAKE=1
CLOSE_ON_GAS=0
```

Nella maggior parte dei mod è **un file vuoto** – indica che il sistema esiste ma non è configurato.

---

### File `.candidate`

File come `cameras.ini.candidate` sono file di lavoro/backup creati manualmente dai modder. **Non vengono mai letti da AC**. L'applicazione deve ignorare file con estensioni non standard (`.candidate`, `.bak`, `.old`, `.tmp`).

---

### File `__cm_*` (Content Manager)

File con prefisso `__cm_` sono generati automaticamente da **Content Manager** (il launcher alternativo per AC) per le sue funzioni di visualizzazione/editing gomme. Esempi:
- `__cm_tyre_wearcurve_front_0.lut` 
- `__cm_tyre_perfcurve_rear_2.lut`

**Non sono letti da AC** e non devono essere modificati manualmente. L'applicazione può mostrarli come file di sistema generati automaticamente.

---

## 9. Riepilogo File nella Cartella `/data`

| File | Obbligatorio | Descrizione |
|------|:---:|-------------|
| `car.ini` | ✅ | Parametri generali, massa, grafica |
| `engine.ini` | ✅ | Motore, turbo, limitatore |
| `drivetrain.ini` | ✅ | Trasmissione, differenziale, frizione |
| `suspensions.ini` | ✅ | Geometria sospensioni, molle, ammortizzatori |
| `tyres.ini` | ✅ | Pneumatici, compound, termica |
| `brakes.ini` | ✅ | Freni, hand brake |
| `aero.ini` | ✅ | Aerodinamica (wings, fins) |
| `setup.ini` | ✅ | Parametri configurabili in setup |
| `lods.ini` | ✅ | Livelli di dettaglio grafico |
| `cameras.ini` | ✅ | Telecamere onboard |
| `ai.ini` | ✅ | Comportamento AI |
| `sounds.ini` | ✅ | Parametri audio |
| `damage.ini` | ✅ | Sistema danno |
| `colliders.ini` | ✅ | Collisori fisici |
| `electronics.ini` | ⚠️ | ABS, TC, EDL, DRS |
| `lights.ini` | ⚠️ | Luci carrozzeria |
| `mirrors.ini` | ⚠️ | Specchietti retrovisori |
| `driver3d.ini` | ⚠️ | Modello pilota 3D |
| `flames.ini` | ⚠️ | Fiamme allo scarico |
| `fuel_cons.ini` | ⚠️ | Consumo carburante |
| `ambient_shadows.ini` | ⚠️ | Ombra statica auto |
| `escmode.ini` | ⚠️ | Camera modalità pit |
| `dash_cam.ini` | ⚠️ | Camera cruscotto |
| `suspension_graphics.ini` | ⚠️ | Grafica sospensioni animate |
| `digital_instruments.ini` | ⚠️ | Strumenti digitali cockpit (da vuoto a molto ricco) |
| `analog_instruments.ini` | ⚠️ | Strumenti analogici cockpit (aghi, needle mesh) |
| `proview_nodes.ini` | ⚠️ | Nodi pro-camera |
| `wing_animations.ini` | ⚠️ | Animazioni alettoni |
| `blurred_objects.ini` | ⚠️ | Blur cerchi ad alta velocità (mesh swap) |
| `flame_presets.ini` | ⚠️ | Preset visivi fiamme di scarico |
| `extra_animations.ini` | ⚠️ | Oggetti rotanti extra (ventole, turbine) |
| `drs.ini` | ⚠️ | DRS – spesso vuoto su auto da drift/strada |
| `brakes_temp.ini` | ⚠️ | Modello termico freni (mod avanzati, gmp) |
| `ers.ini` | ⚠️ | Sistema ERS/ibrido (mod avanzati, gmp) |
| `script.lua` | ⚠️ | Script Lua CSP (logica fisica custom) |
| `ctrl_*.ini` | ⚠️ | Controller programmabili AWD/ERS/boost (gmp) |
| `power.lut` | ✅ | Curva di potenza |
| `throttle.lut` | ⚠️ | Mappatura gas |
| `throttle2.lut` | ⚠️ | Mappatura gas secondaria (mappe motore) |
| `final.rto` | ⚠️ | Rapporti finali disponibili |
| `ratios.rto` | ⚠️ | Rapporti cambio disponibili |
| `tyre_wear_*.lut` | ⚠️ | Curva usura gomme (nome varia per pack) |
| `tcurve_*.lut` | ⚠️ | Curva termica gomme (nome varia per pack) |
| `wing_*_AOA_CL.lut` | ⚠️ | LUT portanza per elemento aero |
| `wing_*_AOA_CD.lut` | ⚠️ | LUT resistenza per elemento aero |
| `analog_rpm_curve.lut` | ⚠️ | Curva contagiri analogico |
| `analog_speed_curve.lut` | ⚠️ | Calibrazione tachimetro analogico |
| `analog_turbo_curve.lut` | ⚠️ | Calibrazione manometro turbo analogico |
| `traction_control.lut` | ⚠️ | Curva livello TC → slip ratio (mod avanzati) |
| `difflock_gear_mult.lut` | ⚠️ | Moltiplicatore bloccaggio diff per marcia |
| `difflock_brake_mult.lut` | ⚠️ | Moltiplicatore bloccaggio diff per freno |
| `fuelmaps.lut` | ⚠️ | Tipi carburante selezionabili |
| `gear_start.lut` | ⚠️ | Coppia massima per marcia al via (launch) |
| `wing_controller_speed.lut` | ⚠️ | Angolo alettone in funzione della velocità |
| `__cm_tyre_*.lut` | 🔵 | Generato da Content Manager – NON letto da AC |

✅ = generalmente sempre presente | ⚠️ = opzionale | 🔵 = generato da strumenti esterni (non usato da AC)

---

## 10. Note per lo Sviluppo dell'Applicazione

1. **Parsing INI:** I file `.ini` di AC ammettono commenti con `;` e possono avere righe vuote. Il formato è standard ma alcune chiavi usano caratteri speciali (es. `...` in CSP). Usare un parser che gestisca valori con spazi e virgole.

2. **Parsing LUT:** Le LUT usano `|` come separatore. Possono contenere righe vuote o righe di commento con `;`. L'interpolazione tra punti è **lineare**. Il carattere `"` può comparire nei valori di testo (es. `fuelmaps.lut`).

3. **Unità di misura:**
   - Forze: Newton (N)
   - Coppie: Newton·metro (Nm)
   - Masse: kg
   - Lunghezze/posizioni: metri
   - Angoli: gradi (salvo INERTIA in rad e alcuni parametri geometria sospensioni)
   - Pressioni gomme: PSI
   - RPM: giri/minuto

4. **Sistema di coordinate:** AC usa un sistema destrorso con Y verso l'alto. Il CoG è l'origine. Z positivo = verso il retrotreno.

5. **Backup:** Prima di modificare, fare sempre backup di `data.acd` e della cartella `/data/`.

6. **Aggiornamento in-game:** AC legge i file al caricamento della sessione; non è necessario riavviare il gioco, basta uscire e rientrare nella sessione.

7. **Gestione file non standard:**
   - Ignorare file con estensioni `.candidate`, `.bak`, `.old`, `.tmp` — non vengono letti da AC.
   - I file con prefisso `__cm_` sono generati da Content Manager e non devono essere modificati manualmente.
   - Il numero e il nome dei file `.lut` varia molto da pack a pack — scoprirli sempre tramite le chiavi `*_CURVE=`, `LUT=`, `*_LUT=` nel file `.ini` corrispondente.
   - File come `ctrl_*.ini`, `ers.ini`, `brakes_temp.ini`, `script.lua` sono presenti solo nei mod più elaborati — non assumere la loro presenza.

8. **Rilevamento versione formato:** Molti file ini hanno `[HEADER] VERSION=N`. Usare questo valore per distinguere il comportamento (es. `drivetrain.ini` con VERSION=3 abilita AWD2 e AUTO_SHIFTER).

9. **File duplicati con suffisso variante:** Alcuni pack includono più varianti dello stesso file (es. `digital_instruments_HKS.ini`, `ctrl_awd2_r34.ini`) — solo il file senza suffisso è caricato da AC; i file con suffisso sono preset alternativi da copiare/rinominare manualmente.
