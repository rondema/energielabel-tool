#!/usr/bin/env python3
"""
Energielabel Tool Server
Proxy server voor BAG en EP-Online APIs (vermijdt CORS problemen)
+ Lokale SQLite database voor buurt labels (6M+ records)
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import sqlite3
import os

# EP-Online API key
EP_ONLINE_API_KEY = 'MUE0NkFCNzg0MjI3NzAzOTU2M0QxRUU1OTNBRTU2QUZGNDJGRkU1OTM5NDMxQTJEODE5QUM5ODUxMUY4RTE0RkEwMjZCNDlDN0RGMTY2NDlCNEE5RTA3QTIzQzVFODAw'

# Lokale energielabel database (gefilterd voor regio Amsterdam/Amstelveen/Aalsmeer/Hoofddorp)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "energielabels_regio.db")

class ProxyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        # Redirect root naar de tool
        if self.path == '/' or self.path == '':
            self.send_response(302)
            self.send_header('Location', '/energielabel-tool-v5.html')
            self.end_headers()
            return
        # API proxy endpoints (volgorde is belangrijk!)
        if self.path.startswith('/api/bag'):
            self.handle_bag_api()
        elif self.path.startswith('/api/ep-online-buurt'):
            self.handle_ep_online_buurt_api()
        elif self.path.startswith('/api/ep-online'):
            self.handle_ep_online_api()
        else:
            # Serve static files
            super().do_GET()

    def handle_bag_api(self):
        """Proxy voor BAG (PDOK) API"""
        try:
            # Parse query parameters
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            postcode = params.get('postcode', [''])[0]
            huisnummer = params.get('huisnummer', [''])[0]

            if not postcode or not huisnummer:
                self.send_json_response({'error': 'postcode en huisnummer zijn verplicht'}, 400)
                return

            # Stap 1: Zoek adres via locatieserver
            query = f"{postcode} {huisnummer}"
            url = f"https://api.pdok.nl/bzk/locatieserver/search/v3_1/free?q={urllib.parse.quote(query)}&fq=type:adres&rows=1"

            data = self.fetch_url(url)
            if not data or 'response' not in data or len(data['response']['docs']) == 0:
                self.send_json_response({'error': 'Adres niet gevonden'}, 404)
                return

            adres = data['response']['docs'][0]
            result = {
                'adres': adres.get('weergavenaam', ''),
                'postcode': adres.get('postcode', ''),
                'huisnummer': adres.get('huisnummer', ''),
                'woonplaats': adres.get('woonplaatsnaam', ''),
                'bouwjaar': None,
                'oppervlakte': None,
                'woningtype': None
            }

            # Stap 2: Haal bouwjaar en oppervlakte op via BAG WFS service (gratis!)
            verblijfsobject_id = adres.get('adresseerbaarobject_id', '')
            if verblijfsobject_id:
                wfs_url = f"https://service.pdok.nl/lv/bag/wfs/v2_0?service=WFS&version=2.0.0&request=GetFeature&typeName=bag:verblijfsobject&outputFormat=json&filter=%3CFilter%3E%3CPropertyIsEqualTo%3E%3CPropertyName%3Eidentificatie%3C/PropertyName%3E%3CLiteral%3E{verblijfsobject_id}%3C/Literal%3E%3C/PropertyIsEqualTo%3E%3C/Filter%3E"
                try:
                    bag_data = self.fetch_url(wfs_url)
                    if bag_data and 'features' in bag_data and len(bag_data['features']) > 0:
                        props = bag_data['features'][0].get('properties', {})
                        result['bouwjaar'] = props.get('bouwjaar')
                        result['oppervlakte'] = props.get('oppervlakte')
                        print(f"  >> BAG WFS data: bouwjaar={result['bouwjaar']}, oppervlakte={result['oppervlakte']}")
                except Exception as e:
                    print(f"  >> BAG WFS error: {e}")

            print(f"  >> Adres gevonden: {result['adres']}")

            self.send_json_response(result)

        except Exception as e:
            print(f"BAG API error: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def handle_ep_online_api(self):
        """Proxy voor EP-Online API"""
        try:
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            postcode = params.get('postcode', [''])[0]
            huisnummer = params.get('huisnummer', [''])[0]
            toevoeging = params.get('toevoeging', [''])[0].upper()

            if not postcode or not huisnummer:
                self.send_json_response({'error': 'postcode en huisnummer zijn verplicht'}, 400)
                return

            url = f"https://public.ep-online.nl/api/v5/PandEnergielabel/Adres?postcode={postcode}&huisnummer={huisnummer}"

            headers = {
                'Authorization': EP_ONLINE_API_KEY,
                'Accept': 'application/json'
            }

            data = self.fetch_url(url, headers=headers)

            if data and len(data) > 0:
                # Als er een toevoeging is, zoek de juiste match
                label = data[0]  # default: eerste resultaat
                if toevoeging:
                    for item in data:
                        huisletter = (item.get('Huisletter') or '').upper()
                        huisnr_toev = (item.get('Huisnummertoevoeging') or '').upper()
                        if huisletter == toevoeging or huisnr_toev == toevoeging:
                            label = item
                            break
                result = {
                    'gevonden': True,
                    'labelLetter': label.get('Energieklasse'),
                    'ep2': label.get('PrimaireFossieleEnergie'),
                    'registratiedatum': label.get('Opnamedatum') or label.get('Registratiedatum'),
                    'berekeningsmethode': label.get('Berekeningstype'),
                    'geldigTot': label.get('Geldig_tot'),
                    # Bonus: BAG data uit EP-Online response
                    'bouwjaar': label.get('Bouwjaar'),
                    'oppervlakte': label.get('Gebruiksoppervlakte_thermische_zone'),
                    'woningtype': label.get('Gebouwtype')
                }
                self.send_json_response(result)
            else:
                self.send_json_response({'gevonden': False})

        except urllib.error.HTTPError as e:
            if e.code == 404:
                self.send_json_response({'gevonden': False})
            else:
                print(f"EP-Online API error: {e}")
                self.send_json_response({'error': str(e)}, 500)
        except Exception as e:
            print(f"EP-Online API error: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def handle_ep_online_buurt_api(self):
        """Buurt labels uit lokale SQLite database (5.7M records)"""
        try:
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)

            postcode = params.get('postcode', [''])[0].upper().replace(' ', '')

            if not postcode:
                self.send_json_response({'error': 'postcode is verplicht'}, 400)
                return

            # Check of database bestaat
            if not os.path.exists(DB_PATH):
                print(f"Database niet gevonden: {DB_PATH}")
                self.send_json_response({
                    'error': 'Energielabel database niet gevonden',
                    'totaal': 0,
                    'labels': {},
                    'adressen': []
                }, 500)
                return

            # Query lokale database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Haal alle labels voor deze postcode (compacte database)
            cursor.execute("""
                SELECT postcode, huisnummer, huisletter, huisnummertoevoeging,
                       energieklasse, bouwjaar, ep2, berekeningstype
                FROM energielabels
                WHERE postcode = ?
                ORDER BY huisnummer, huisletter, huisnummertoevoeging
            """, (postcode,))

            rows = cursor.fetchall()
            conn.close()

            if rows:
                # Tel labels per klasse
                label_telling = {}
                adressen = []

                for row in rows:
                    postcode_r, huisnummer, huisletter, toevoeging, energieklasse, \
                    bouwjaar, pfe, berekeningstype = row

                    # Tel energieklasse
                    if energieklasse:
                        label_telling[energieklasse] = label_telling.get(energieklasse, 0) + 1

                    # Bouw adres string
                    adres = f"{huisnummer}"
                    if huisletter:
                        adres += huisletter
                    if toevoeging:
                        adres += f"-{toevoeging}"

                    # Bepaal of het een nieuw label is (NTA 8800 = heeft EP2)
                    is_nieuw_label = pfe is not None and pfe > 0

                    adressen.append({
                        'huisnummer': adres,
                        'energieklasse': energieklasse,
                        'bouwjaar': bouwjaar,
                        'ep2': round(pfe) if pfe else None,
                        'isNieuwLabel': is_nieuw_label
                    })

                print(f"  >> Buurt labels voor {postcode}: {len(rows)} adressen gevonden")

                self.send_json_response({
                    'postcode': postcode,
                    'totaal': len(rows),
                    'labels': label_telling,
                    'adressen': adressen
                })
            else:
                print(f"  >> Geen labels gevonden voor postcode {postcode}")
                self.send_json_response({
                    'postcode': postcode,
                    'totaal': 0,
                    'labels': {},
                    'adressen': []
                })

        except Exception as e:
            print(f"Buurt labels error: {e}")
            self.send_json_response({'error': str(e)}, 500)

    def fetch_url(self, url, headers=None):
        """Fetch URL and return JSON data"""
        try:
            req = urllib.request.Request(url)
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)

            # SSL context
            ctx = ssl.create_default_context()

            with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            raise
        except Exception as e:
            print(f"Fetch error for {url}: {e}")
            return None

    def send_json_response(self, data, status=200):
        """Send JSON response with CORS headers"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.address_string()}] {args[0]}")


def run_server(port=8892):
    server_address = ('0.0.0.0', port)  # Bind to all interfaces for production
    httpd = HTTPServer(server_address, ProxyHandler)
    print(f"🏠 Energielabel Tool Server draait op http://localhost:{port}")
    print(f"   Open: http://localhost:{port}/energielabel-tool-v5.html")
    print(f"   Stop: Ctrl+C")
    httpd.serve_forever()


if __name__ == '__main__':
    # Use PORT environment variable if set (for cloud hosting like Render)
    port = int(os.environ.get('PORT', 8892))
    run_server(port)
