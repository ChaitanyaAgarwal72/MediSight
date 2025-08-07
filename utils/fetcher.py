import requests

def fetch_medical_data(query: str) -> list:
    url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": query,
        "format": "json",
        "pageSize": 5
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()['resultList']['result']
        output = []
        for result in results:
            title = result.get("title", "No title available")
            year = result.get("pubYear", "No publication year available")
            pmcid = result.get("pmcid")
            doi = result.get("doi")
            
            if pmcid:
                link = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/"
            elif doi:
                link = f"https://doi.org/{doi}"
            else:
                link = "No link available"
            
            output.append({
                "title": title,
                "pubYear": year,
                "link": link
            })
        return output
    
    else:
        print(f"Error fetching data: {response.status_code}")
        return []
