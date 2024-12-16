from waybackpy import WaybackMachineCDXServerAPI
from datetime import datetime, timedelta
import requests


class HistoricalSearch:
    def __init__(self, url, user_agent):
        self.url = url
        self.user_agent = user_agent

    def search_snapshot(self, years_ago=10, filename="snapshot.html"):
        """Busca y guarda una captura cerca de una fecha específica."""
        target_date = datetime.now() - timedelta(days=365 * years_ago)
        year, month, day = target_date.year, target_date.month, target_date.day

        cdx_api = WaybackMachineCDXServerAPI(self.url, self.user_agent)
        snapshot = cdx_api.near(year=year, month=month, day=day)
        if snapshot:
            print(f"Fecha: {snapshot.timestamp}, URL: {snapshot.archive_url}")
            self.download_snapshot(snapshot.archive_url, filename)
        else:
            print("No se encontró ninguna captura para la fecha especificada.")

    def download_snapshot(self, archive_url, filename):
        """Descarga y guarda el contenido de un snapshot en disco."""
        response = requests.get(archive_url)
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Documento guardado exitosamente en {filename}")
        else:
            print("Error al descargar la página.")

    def search_snapshot_by_extensions(self, year_ago=4, days_interval=7, extensions=None, match_type="domain"):
        """Busca capturas por extensiones específicas en un intervalo de tiempo."""
        if extensions is None:
            extensions = ["pdf", "doc", "docx", "ppt", "xls", "xlsx", "txt"]

        # Calcular las fechas para el período especificado
        today = datetime.now()
        start_period = (today - timedelta(days=365 * year_ago)).strftime('%Y%m%d')
        end_period = (today - timedelta(days=(365 * year_ago) - days_interval)).strftime('%Y%m%d')
         
        cdx_api = WaybackMachineCDXServerAPI(
            url=self.url,
            user_agent=self.user_agent,
            start_timestamp=start_period,
            end_timestamp=end_period,
            match_type=match_type
        )
        # Aplicar un filtro por expresiones regulares
        regex_filter = "(" + "|".join([f".*\\.{ext}$" for ext in extensions]) + ")"
        cdx_api.filters = [f"urlkey:{regex_filter}"]

        # Realizar la consulta a Wayback Machine
        snapshots = cdx_api.snapshots()
        for snapshot in snapshots:
            print(f"Fecha: {snapshot.timestamp}, URL: {snapshot.archive_url}")


# Uso de la clase
user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
url = "github.com"
hsearch = HistoricalSearch(url, user_agent)
# hsearch.search_snapshot()  # Para buscar un snapshot específico

hsearch.search_snapshot_by_extensions()
