import requests
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

def benchmark(url: str, total_requests: int = 100, concurrency: int = 10):
    """
    Envoie `total_requests` requêtes GET à `url` avec `concurrency` requêtes simultanées.
    Mesure les temps de réponse et affiche quelques statistiques.
    """
    times = []

    def send_request(_):
        start = time.time()
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            return time.time() - start
        except Exception as e:
            return None

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        results = list(executor.map(send_request, range(total_requests)))

    successful = [r for r in results if r is not None]
    failed = len(results) - len(successful)

    print(f"URL testée         : {url}")
    print(f"Total requêtes     : {total_requests}")
    print(f"Concurrence max    : {concurrency}")
    print(f"Réussites          : {len(successful)}")
    print(f"Échecs             : {failed}")
    if successful:
        print(f"RPS (moyenne)      : {len(successful) / sum(successful):.2f}")
        print(f"Temps moyen (s)    : {statistics.mean(successful):.4f}")
        print(f"Temps médian (s)   : {statistics.median(successful):.4f}")
        print(f"Temps 95e pctile   : {statistics.quantiles(successful, n=100)[94]:.4f}")


if __name__ == "__main__":
    benchmark(
        url="http://13.36.203.126:5000/hello_world",
        total_requests=200,
        concurrency=20
    )