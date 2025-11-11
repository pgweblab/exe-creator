# EXE Creator Pro - Virtual Environment Edition

<div align="center">

### 🚀 Converti Script Python in EXE Windows in Pochi Click

**Interfaccia Moderna | Tema Scuro Professionale | Automazione Completa**

[🇮🇹 Italiano](#-descrizione-italiana) • [🇬🇧 English](#-english-description)

</div>

---

## 🇮🇹 Descrizione Italiana

**EXE Creator Pro** è un'applicazione desktop professionale che semplifica la conversione di script Python in eseguibili Windows (.exe). Grazie a un'interfaccia moderna con tema scuro, gestisce automaticamente l'ambiente virtuale isolato, le dipendenze Python e la compilazione con PyInstaller.

Perfetta per sviluppatori che vogliono distribuire script Python come programmi eseguibili standalone, senza richiedere Python installato nei sistemi degli utenti finali.

### Funzionalità Principali

- 🔧 **Gestione Automatica Ambiente** - Crea e mantiene un ambiente virtuale isolato
- 🔍 **Analisi Intelligente Dipendenze** - Rileva automaticamente tutti gli import necessari
- 🧹 **Pulizia Smart** - Rimuove automaticamente pacchetti problematici e backport obsoleti
- 📄 **Supporto requirements.txt** - Carica dipendenze direttamente da file esterno
- 🎨 **Tema Moderno Scuro** - Interfaccia professionale e piacevole da usare
- ⚡ **Real-time Logging** - Feedback visivo immediato di tutti i processi
- 🎯 **Icone Personalizzate** - Aggiungi icona .ico al tuo eseguibile
- ⚙️ **Compilazione Flessibile** - Console opzionale, nome custom, build pulite

---

## 🇬🇧 English Description

**EXE Creator Pro** is a professional desktop application that simplifies converting Python scripts into Windows executables (.exe). With a modern dark-themed interface, it automatically manages isolated virtual environments, Python dependencies, and compilation using PyInstaller.

Perfect for developers who want to distribute Python scripts as standalone executable programs without requiring Python installation on end-user systems.

### Key Features

- 🔧 **Automatic Environment Management** - Creates and maintains isolated virtual environment
- 🔍 **Smart Dependency Analysis** - Automatically detects all required imports
- 🧹 **Intelligent Cleanup** - Automatically removes problematic packages and obsolete backports
- 📄 **requirements.txt Support** - Load dependencies directly from external file
- 🎨 **Modern Dark Theme** - Professional and pleasant-to-use interface
- ⚡ **Real-time Logging** - Immediate visual feedback of all processes
- 🎯 **Custom Icons** - Add .ico icon to your executable
- ⚙️ **Flexible Compilation** - Optional console, custom name, clean builds

---

## ✨ Caratteristiche | Features

- **Ambiente Virtuale** - Creazione e gestione automatica dell'ambiente virtuale isolato | Automatic creation and management of isolated virtual environment
- **Analisi Intelligente** - Rileva automaticamente tutte le dipendenze Python richieste | Automatically detects all required Python dependencies
- **Pulizia Ambiente** - Rimozione automatica di pacchetti problematici e backport obsoleti | Automatic removal of problematic packages and obsolete backports
- **Requirements Management** - Carica direttamente da file requirements.txt | Load directly from requirements.txt file
- **Installazione Dipendenze** - Installazione con progresso visivo e cancellazione in tempo reale | Installation with visual progress and real-time cancellation
- **Compilazione EXE** - Supporto console opzionale e icone personalizzate | Optional console support and custom icons
- **Interfaccia Moderna** - Tema scuro professionale con feedback visivo immediato | Professional dark theme with immediate visual feedback
- **Log in Tempo Reale** - Output dettagliato di tutti i processi | Detailed output of all processes

## 📋 Requisiti | Requirements

- Python 3.6+
- Windows (testato su Windows 10/11 | tested on Windows 10/11)
- Spazio disco: ~500MB per ambiente virtuale + dipendenze | Disk space: ~500MB for virtual environment + dependencies

## 🚀 Installazione | Installation

```bash
# Clone the repository | Clona il repository
git clone https://github.com/pgweblab/exe-creator.git
cd exe-creator

# Run the application | Esegui l'applicazione
python exe_creator.py
```

## 💡 Utilizzo | Usage

### Workflow Standard | Standard Workflow

1. **Configura Ambiente** / **Setup Environment** → Crea l'ambiente virtuale e installa PyInstaller
2. **Nome Software** / **Software Name** → Specifica il nome dell'eseguibile
3. **Seleziona Script** / **Select Script** → Scegli il file Python da convertire
4. **Analizza Dipendenze** / **Analyze Dependencies** → Rileva automaticamente i pacchetti richiesti
5. **Opzioni Build** / **Build Options** → Console opzionale, icona personalizzata
6. **Installa Dipendenze** / **Install Dependencies** → Installa tutti i pacchetti necessari
7. **Crea EXE** / **Create EXE** → Genera l'eseguibile nella cartella `dist`

## ⚙️ Opzioni Disponibili | Available Options

| Opzione / Option | Descrizione / Description |
|---------|------------|
| Nome Software / Software Name | Nome dell'eseguibile (.exe) generato / Name of generated executable (.exe) |
| Mostra Console / Show Console | Visualizza finestra console durante l'esecuzione / Display console window during execution |
| Icona Personalizzata / Custom Icon | Aggiungi icona .ico all'eseguibile / Add .ico icon to executable |
| Analizza Dipendenze / Analyze Dependencies | Estrae automaticamente import da script / Automatically extracts imports from script |
| Carica requirements.txt / Load requirements.txt | Importa dipendenze da file esterno / Import dependencies from external file |
| Pulisci Ambiente / Clean Environment | Rimuove pacchetti problematici / Remove problematic packages |

## 📦 Pacchetti Problematici Rimossi Automaticamente | Problematic Packages Automatically Removed

- typing, pathlib, enum34, functools32 (backport obsoleti / obsolete backports)
- importlib-metadata (conflitti con PyInstaller / conflicts with PyInstaller)
- backports.functools-lru-cache (backport obsoleto / obsolete backport)

## 🎨 Interfaccia | Interface

- **Tema Scuro** - Tema moderno e professionale / Modern and professional dark theme
- **Feedback Visivo** - Colori diversi per successo, errore, warning / Different colors for success, error, warning
- **Barra Progresso** - Visualizzazione dello stato di installazione / Installation status visualization
- **Output Dettagliato** - Log completo di tutte le operazioni / Complete log of all operations

## 📝 Licenza | License

Creato da **Piergiorgio Concari** (AI-Creative-Studio.com)  
Licenza di condivisione libera con obbligo di mantenimento dell'autore  
Free sharing license with obligation to maintain the author

Created by **Piergiorgio Concari** (AI-Creative-Studio.com)  
Free sharing license with obligation to maintain author attribution
