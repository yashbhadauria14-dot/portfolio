import urllib.request

with urllib.request.urlopen('http://localhost:8080/index.html') as resp:
    print('HTTP Status:', resp.status)
    content = resp.read().decode('utf-8')
    print('Content length:', len(content))
    
    print('1. Email button wired correctly:', 'mailto:bhadauriayash14@gmail.com' in content)
    print('2. PapaParse CDN present:', 'papaparse.min.js' in content)
    print('3. SheetJS CDN present:', 'xlsx.full.min.js' in content)
    print('4. Project 1 (Hospital live CSV fetch):', 'loadHospitalDashboard' in content)
    print('5. Project 2 (Retail live Excel fetch):', 'loadRetailDashboard' in content)
    print('6. Project 3 (ETL live Excel & client-side cleaning):', 'loadEtlDashboard' in content)
    print('7. Project 4 (Superstore live CSV & derived insights):', 'loadSuperstoreDashboard' in content)
    print('8. Project 5 (Bookstore raw SQL showcase):', 'loadBookstoreShowcase' in content)
    print('9. Refresh Data button present:', 'btn-dash-refresh' in content)
