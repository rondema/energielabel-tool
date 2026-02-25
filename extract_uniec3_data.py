#!/usr/bin/env python3
"""
Energielabel Data Extractor
Extraheert data uit .uniec3 bestanden en bouwt een database voor analyse.
"""

import os
import json
import zipfile
import csv
from pathlib import Path
from datetime import datetime

# Configuratie
COMPLETED_PATH = "/Users/markrondema/Library/Mobile Documents/com~apple~CloudDocs/Desktop/COMPLETED"
OUTPUT_DIR = "/Users/markrondema/Desktop/CLAUDE PROJECTS/ENERGIELABEL BEREKENEN"

def extract_uniec3_data(uniec3_path):
    """Extraheert relevante data uit een .uniec3 bestand."""
    try:
        with zipfile.ZipFile(uniec3_path, 'r') as zf:
            # Lees summary.json voor hoofdresultaten
            summary_data = {}
            for name in zf.namelist():
                if name.endswith('summary.json'):
                    with zf.open(name) as f:
                        content = f.read().decode('utf-8-sig')
                        summary_data = json.loads(content)
                    break

            # Lees entities.json voor gedetailleerde data
            entities_data = []
            for name in zf.namelist():
                if name.endswith('entities.json'):
                    with zf.open(name) as f:
                        content = f.read().decode('utf-8-sig')
                        entities_data = json.loads(content)
                    break

            return summary_data, entities_data
    except Exception as e:
        print(f"  Fout bij lezen {uniec3_path}: {e}")
        return {}, []

def parse_entities(entities):
    """Parst entities naar bruikbare data."""
    result = {}

    for entity in entities:
        entity_id = entity.get('NTAEntityId', '')
        props = entity.get('NTAPropertyDatas', [])

        for prop in props:
            prop_id = prop.get('NTAPropertyId', '')
            value = prop.get('Value')
            if value and value != 'null':
                key = f"{entity_id}_{prop_id}"
                result[key] = value

    return result

def extract_key_values(summary, entities_parsed):
    """Extraheert de belangrijkste waarden voor analyse."""

    # Basis info uit summary
    data = {
        'adres': summary.get('GEB_OMSCHR', ''),
        'gebouwtype': summary.get('GEB_TYPEGEB', ''),
        'energielabel': summary.get('EP_ENERGIELABEL', ''),
        'ep1_beng1': summary.get('EP_BENG1', ''),
        'ep2_beng2': summary.get('EP_BENG2', ''),
        'ep3_beng3': summary.get('EP_BENG3', ''),
        'co2': summary.get('RESULT_CO2_CO2', ''),
        'tojuli': summary.get('EP_TOJULI', ''),
    }

    # Verwarming
    for key, value in entities_parsed.items():
        # Verwarmingstype
        if 'VERW-OPWEK_TYPE' in key:
            data['verwarming_type'] = value
        if 'VERW-OPWEK_TOES_NAAM' in key:
            data['verwarming_toestel'] = value
        if 'VERW-OPWEK_REND' in key and 'NON' in key:
            data['verwarming_rendement'] = value

        # Ventilatie
        if 'VENT_SYS' in key:
            data['ventilatie_systeem'] = value
        if 'VENT_VARIANT' in key:
            data['ventilatie_variant'] = value

        # Tapwater
        if 'TAPW-OPWEK_TYPE' in key:
            data['tapwater_type'] = value
        if 'TAPW-OPWEK_TOES_NAAM' in key:
            data['tapwater_toestel'] = value

        # Afgifte
        if 'VERW-AFG_TYPE_AFG' in key:
            data['afgifte_type'] = value

        # Gebruiksoppervlakte
        if 'GEB_AG' in key or 'RZFORM_AG' in key:
            data['gebruiksoppervlakte'] = value

        # Bouwjaar (als beschikbaar)
        if 'GEB_BOUWJAAR' in key or 'BOUWJAAR' in key:
            data['bouwjaar'] = value

    return data

def find_uniec3_files(base_path):
    """Zoekt alle .uniec3 bestanden in de mapstructuur."""
    uniec3_files = []

    # Gebruik glob voor snellere lookup
    from glob import glob
    pattern = os.path.join(base_path, "*", "Opname", "Van adviseur", "*.uniec3")
    uniec3_files = glob(pattern)

    # Filter op lokaal beschikbare bestanden (niet in iCloud pending)
    available_files = []
    for f in uniec3_files:
        # Check of bestand lokaal beschikbaar is (niet .icloud placeholder)
        if os.path.exists(f) and os.path.getsize(f) > 100:
            available_files.append(f)

    return available_files

def main():
    print("=" * 60)
    print("ENERGIELABEL DATA EXTRACTOR")
    print("=" * 60)
    print(f"Bron map: {COMPLETED_PATH}")
    print()

    # Zoek alle .uniec3 bestanden
    print("Zoeken naar .uniec3 bestanden...")
    uniec3_files = find_uniec3_files(COMPLETED_PATH)
    print(f"Gevonden: {len(uniec3_files)} bestanden")
    print()

    # Extraheer data
    all_data = []
    success = 0
    failed = 0

    for i, filepath in enumerate(uniec3_files):
        filename = os.path.basename(filepath)
        if i % 10 == 0:  # Print elke 10 bestanden
            print(f"[{i+1}/{len(uniec3_files)}] Verwerken...")

        try:
            summary, entities = extract_uniec3_data(filepath)

            if summary:
                entities_parsed = parse_entities(entities)
                data = extract_key_values(summary, entities_parsed)
                data['bestand'] = filename
                data['pad'] = filepath
                all_data.append(data)
                success += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  Fout bij {filename[:30]}: {e}")
            failed += 1

    print()
    print(f"Succesvol: {success}")
    print(f"Mislukt: {failed}")
    print()

    # Opslaan als JSON
    json_path = os.path.join(OUTPUT_DIR, "energielabel_database.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print(f"JSON opgeslagen: {json_path}")

    # Opslaan als CSV
    csv_path = os.path.join(OUTPUT_DIR, "energielabel_database.csv")
    if all_data:
        # Verzamel alle mogelijke velden
        all_keys = set()
        for item in all_data:
            all_keys.update(item.keys())

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            writer.writerows(all_data)
        print(f"CSV opgeslagen: {csv_path}")

    # Statistieken
    print()
    print("=" * 60)
    print("STATISTIEKEN")
    print("=" * 60)

    # Labels verdeling
    labels = {}
    for item in all_data:
        label = item.get('energielabel', 'Onbekend')
        labels[label] = labels.get(label, 0) + 1

    print("\nEnergielabels verdeling:")
    for label in sorted(labels.keys()):
        count = labels[label]
        bar = "█" * (count // 2)
        print(f"  {label:6} {count:3}x {bar}")

    # EP2 statistieken
    ep2_values = []
    for item in all_data:
        try:
            ep2 = float(item.get('ep2_beng2', '0').replace(',', '.'))
            if ep2 > 0:
                ep2_values.append(ep2)
        except:
            pass

    if ep2_values:
        print(f"\nEP2 statistieken (n={len(ep2_values)}):")
        print(f"  Gemiddeld: {sum(ep2_values)/len(ep2_values):.1f} kWh/m²")
        print(f"  Minimum:   {min(ep2_values):.1f} kWh/m²")
        print(f"  Maximum:   {max(ep2_values):.1f} kWh/m²")

    print()
    print("Klaar!")

if __name__ == "__main__":
    main()
