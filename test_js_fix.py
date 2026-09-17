import urllib.request

with urllib.request.urlopen('http://localhost:8080/index.html') as resp:
    html = resp.read().decode('utf-8')
    print("Fetched index.html len:", len(html))
    
    # Check syntax fixes
    print("1. Bracket access for patients.csv:", "liveCache.hospital['patients.csv']" in html)
    print("2. Bracket access for appointments.csv:", "liveCache.hospital['appointments.csv']" in html)
    print("3. openProjectDash function present:", "function openProjectDash(" in html)
    print("4. loadHospitalDashboard function present:", "async function loadHospitalDashboard(" in html)
    print("5. loadRetailDashboard function present:", "async function loadRetailDashboard(" in html)
    print("6. loadEtlDashboard function present:", "async function loadEtlDashboard(" in html)
    print("7. loadSuperstoreDashboard function present:", "async function loadSuperstoreDashboard(" in html)
    print("8. loadBookstoreShowcase function present:", "async function loadBookstoreShowcase(" in html)
