#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ***************************************
# PiFace Digital 2 Example by PIkarus
# ***************************************

import sys
sys.path.append('/storage/python/usr/lib/python2.7/site-packages')
import time
import pifacedigitalio

#***********************************
# einzelnen Eingang abfragen (0-7)
#***********************************
def input (bit):
    return (pifacedigitalio.digital_read(bit))

#***********************************
# einzelnen Ausgang einschalten (0-7)
#***********************************
def output_on (bit):
    return (pifacedigital.output_pins[bit].turn_on())

#***********************************
# einzelnen Ausgang ausschalten (0-7)
#***********************************
def output_off (bit):
    return (pifacedigital.output_pins[bit].turn_off())

#***********************************
# einzelnen Ausgang umschalten (0-7)
#***********************************
def output_toggle (bit):
    return (pifacedigital.leds[bit].toggle())
    
#***********************************
# 8 Ausgänge schreiben (0-7)
#***********************************
def write_outputs (outputs):
    for b in range(0, 8):
        if outputs[b]['bit']:
            output_on(b)
        else:
            output_off(b)

#***********************************
# Abfrage der positiven Flanke
#***********************************
def p_flanke (signal):
    flanke = False
    if signal['bit'] and signal['bit'] != signal['status']:
        flanke = True
    signal['status'] = signal['bit']
    return (flanke,  signal['status'])

#***********************************
# Abfrage der negativen Flanke
#***********************************
def n_flanke (signal):
    flanke = False
    if not signal['bit'] and signal['bit'] != signal['status']:
        flanke = True
    signal['status'] = signal['bit']
    return (flanke,  signal['status'])
    
#***********************************
# Schiebe links 1 Bit. Wird ein Bit 
# rausgeschoben, so liefert die 
# Funktion True
#***********************************
def shl (byte):
    status = byte[7]['bit']
    for b in range(6, -1, -1):
        byte[b+1]['bit'] = byte[b]['bit']
    byte[0]['bit'] = False
    return (byte, status)

#***********************************
# Schiebe rechts 1 Bit. Wird ein Bit 
# rausgeschoben, so liefert die 
# Funktion True
#***********************************
def shr (byte):
    status = byte[0]['bit']
    for b in range(0, 7):
        byte[b]['bit'] = byte[b+1]['bit']
    byte[7]['bit'] = False
    return (byte, status)

#***********************************
# 8 Eingänge abfragen (0-7)
#***********************************
def read_inputs(inputs):
    for b in range (0, 8):
        inputs[b]['bit'] = input (b)
    return (inputs)

#***********************************
# Pufffer für 8 Eing./Ausgänge anlegen
#***********************************
def init_byte(byte):
    for b in range(0, 8):
        byte.append ({
            'bit' : False, 
            'status' : False, 
        })
    return (byte)

#***********************************
# Pufffer für 16 Zeiten anlegen
#***********************************
def init_timers(ti):
    for t in range(0, 16):
        ti.append({
            'bit': False, 
            'end' : 0, 
        })
    return (ti)

#***********************************
# Bit invertieren
#***********************************
def toggle (bit):
    return (not bit)

#***********************************
# Zeit abfragen. Abgelaufen = True
#***********************************
def get_timer (ti):
    status = False
    if ti['bit'] and current_ms() >= ti['end']: status = True
    return (status)

#***********************************
# Zeit starten.
#***********************************
def start_timer(ti,  ms):
    ti['bit'] = True
    ti['end'] = current_ms() + int(ms)
    return (ti)

#***********************************
# Zeit zurücksetzen.
#***********************************
def reset_timer(ti):
    ti['bit'] = False
    return (ti)

#***********************************
# aktuelle Zeit in ms abfragen
#***********************************
def current_ms():
    return (int(round(time.time() * 1000)))

if __name__ == "__main__":
# PiFace initialisieren    
    pifacedigitalio.init()
    pifacedigital = pifacedigitalio.PiFaceDigital()

# Puffer für  8 Eingänge anlegen
    inputs = []
    inputs = init_byte(inputs)

# Pufffer für 8 Ausgänge anlegen
    outputs =[]
    outputs = init_byte(outputs)

# Pufffer für 16 Zeiten anlegen
    timers = []
    timers = init_timers(timers)

# *****************************************************    
# Hauptprogramm
# *****************************************************    
    right = False
    f1 = True
    while True: 

# Eingänge abfragen und in Eingangspuffer schreiben
        inputs = read_inputs(inputs)

# Positive Flanke von Eingang 0 abfragen        
        i, inputs[0]['ststus'] = p_flanke(inputs[0])

# steigende Flanke erkannt dann Ausgang 0 togglen und Zeit 0 starten
        if i: 
            outputs[0]['bit'] = toggle(outputs[0]['bit'])
            timers[0] = start_timer(timers[0], 50)
            
# Positive Flanke von Eingang 1 abfragen        
        i, inputs[1]['ststus'] = p_flanke(inputs[1])

# steigende Flanke erkannt dann Funktion wechseln
        if i: f1 = toggle(f1)

# Positive Flanke von Eingang 2 abfragen
        i, inputs[2]['ststus'] = p_flanke(inputs[2])

# steigende Flanke erkannt dann Ausgangspuffer löschen
        if i:
            for b in range(0, 8):
                outputs[b]['bit'] = False
        
        if f1:
# Zeit 0 abgelaufen dann Ausgang 1 ein, Zeit 0 zurücksetzen und Zeit 1 starten
            if get_timer(timers[0]):
                outputs[1]['bit'] = True
                reset_timer(timers[0])
                start_timer(timers[1], 1000)

# Zeit 1 abgelaufen dann Ausgang 1 aus und Zeit 1 zurücksetzen
            if get_timer(timers[1]):
                outputs[1]['bit'] = False
                reset_timer(timers[1])
        else:
            if get_timer(timers[0]):
                y = False
                for x in range(0, 8):
                    if outputs[x]['bit']: y = True
    
                if y :
                    timers[0] = start_timer(timers[0],  50)
                    if right:
                        outputs, st = shr (outputs)
                        if st: 
                            outputs[0]['bit']= st
                            right = False
                    else:
                        outputs, st = shl (outputs)
                        if st: 
                            outputs[7]['bit']= st
                            right = True
                else : timers[0] = reset_timer(timers[0])
            
# Augangspuffer auf Ausgänge schreiben
        write_outputs(outputs)
