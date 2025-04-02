from nicegui import ui
import sqlite3
from datetime import date, datetime

# Configurazione del database
def setup_database():
    conn = sqlite3.connect('clienti.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clienti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        email TEXT,
        telefono TEXT,
        indirizzo TEXT,
        citta TEXT,
        cap TEXT,
        data_nascita DATE,
        note TEXT,
        data_registrazione DATE DEFAULT CURRENT_DATE
    )
    ''')
    conn.commit()
    conn.close()

# Funzione per salvare un nuovo cliente
def salva_cliente(nome, cognome, email, telefono, indirizzo, citta, cap, data_nascita, note):
    conn = sqlite3.connect('clienti.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO clienti (nome, cognome, email, telefono, indirizzo, citta, cap, data_nascita, note)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, cognome, email, telefono, indirizzo, citta, cap, data_nascita, note))
    conn.commit()
    conn.close()
    return cursor.lastrowid

# Funzione per convertire la data dal formato italiano (DD/MM/YYYY) a formato ISO
def converti_data_italiana(data_str):
    if not data_str:
        return None
    try:
        return datetime.strptime(data_str, "%d/%m/%Y").date().isoformat()
    except ValueError:
        return None

# Inizializzazione del database
setup_database()

def maximize():
    dialog.props('maximized')
    card.classes('w-screen h-screen')

with ui.dialog().props('auto-close') as dialog:
    dialog.card.classes('bg-gray p-16')


# Definizione del form modale che verrà attivato dal bottone
def apri_form_cliente():
    with ui.dialog().classes('w-full max-w-9/10') as dialog, ui.card():
    # with ui.dialog() as dialog, ui.card().classes('w-full max-w-9/10'):
    
        ui.label('Inserimento Nuovo Cliente').classes('text-h5 q-mb-md')
        
        # Contenitore principale diviso in due colonne
        with ui.row().classes('w-full'):
            # Colonna sinistra
            with ui.column().classes('w-1/2 pr-2'):
                nome = ui.input('Nome *').props('outlined').classes('w-full q-mb-sm')
                email = ui.input('Email', validation={'Invalid email': lambda value: '@' in (value or '')}).props('outlined').classes('w-full q-mb-sm')
                indirizzo = ui.input('Indirizzo').props('outlined').classes('w-full q-mb-sm')
                cap = ui.input('CAP').props('outlined').classes('w-full q-mb-sm')
                
                # Campo data con formato italiano
                ui.label('Data di Nascita').classes('q-mb-xs')
                with ui.row().classes('w-full items-center q-mb-sm'):
                    data_nascita_input = ui.input('').props('outlined placeholder="GG/MM/AAAA"').classes('w-3/4')
                    
                    # Funzione per aprire il calendario
                    def apri_calendario():
                        with ui.dialog() as date_dialog, ui.card():
                            ui.label('Seleziona la data di nascita')
                            
                            # Componente data che aggiorna direttamente l'input
                            calendario = ui.date()
                            
                            with ui.row().classes('justify-end'):
                                ui.button('Annulla', on_click=date_dialog.close).props('flat')
                                
                                def conferma_data():
                                    if calendario.value:
                                        # Converti la data in formato italiano
                                        data_selezionata = calendario.value
                                        formatted_date = datetime.fromisoformat(data_selezionata).strftime("%d/%m/%Y")
                                        data_nascita_input.value = formatted_date
                                    date_dialog.close()
                                    
                                ui.button('Conferma', on_click=conferma_data).props('color=primary')
                            
                        date_dialog.open()
                    
                    # Pulsante per aprire il calendario
                    ui.button(icon='event').props('flat').on('click', apri_calendario).classes('w-1/4')
            
            # Colonna destra
            with ui.column().classes('w-1/2 pl-2'):
                cognome = ui.input('Cognome *').props('outlined').classes('w-full q-mb-sm')
                telefono = ui.input('Telefono').props('outlined').classes('w-full q-mb-sm')
                citta = ui.input('Città').props('outlined').classes('w-full q-mb-sm')
                note = ui.textarea('Note').props('outlined').classes('w-full')
        
        # Pulsanti di azione
        with ui.row().classes('justify-end q-mt-md'):
            ui.button('Annulla', on_click=dialog.close).props('flat')
            
            def on_submit():
                # Validazione campi obbligatori
                if not nome.value or not cognome.value:
                    ui.notify('Nome e Cognome sono campi obbligatori', color='negative')
                    return
                
                # Conversione della data dal formato italiano a ISO
                data_nascita_str = converti_data_italiana(data_nascita_input.value)
                
                # Salvataggio del cliente
                cliente_id = salva_cliente(
                    nome.value, 
                    cognome.value, 
                    email.value, 
                    telefono.value, 
                    indirizzo.value, 
                    citta.value, 
                    cap.value, 
                    data_nascita_str, 
                    note.value
                )
                
                # Notifica e chiusura del dialogo
                ui.notify(f'Cliente {nome.value} {cognome.value} salvato con successo!', color='positive')
                dialog.close()
            
            ui.button('Salva', on_click=on_submit).props('color=primary')
        
        dialog.open()

# Applicazione principale con una pagina semplice e un bottone centrale
def main():
    # Stile CSS personalizzato per una pagina di sfondo pulita
    ui.add_head_html('''
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }
        .page-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .button-container {
            text-align: center;
        }
        .app-title {
            margin-bottom: 30px;
            text-align: center;
        }
    </style>
    ''')

    fullscreen = ui.fullscreen()
    fullscreen.enter
    # Container principale che occupa l'intera pagina
    with ui.column().classes('page-container'):
        with ui.column().classes('app-title'):
            ui.label('Sistema Gestione Clienti').classes('text-h3')
            ui.label('Premi il pulsante per aggiungere un nuovo cliente').classes('text-subtitle1')
        
        # Contenitore del bottone centrale
        with ui.column().classes('button-container'):
            ui.button('Aggiungi Nuovo Cliente', icon='person_add', on_click=apri_form_cliente).classes('text-xl p-4').style('font-size: 20px')
            ui.button('Enter Fullscreen', on_click=fullscreen.enter)
            ui.button('Exit Fullscreen', on_click=fullscreen.exit)
            ui.button("open", on_click=dialog.open)



# Chiamata alla funzione main per impostare l'interfaccia
main()

# Avvio dell'applicazione
ui.run(title="Sistema Gestione Clienti")
