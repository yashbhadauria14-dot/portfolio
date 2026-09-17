import urllib.request

with urllib.request.urlopen('http://localhost:8080/index.html') as resp:
    print('HTTP Status:', resp.status)
    content = resp.read().decode('utf-8')
    print('Content length:', len(content))
    skills_part = content.split('id="skills"')[1].split('</section>')[0]
    print('1. Skills section (No percentages):', '%' not in skills_part)
    print('2. Projects (All 5 GitHub projects present):', content.count('class="glass-card project-card"') == 5)
    print('3. Contact Section (Functional buttons):', 'mailto:bhadauriayash14@gmail.com' in content and 'https://www.linkedin.com/in/yash-pratap-singh-807560253/' in content and 'tel:+917704038276' in content and '+91 7704038276' in content)
    print('4. Bootcamp Section present:', 'PW | NSDC | PwC' in content and 'daily practice discipline' in content.lower())
    print('5. Interactive Dashboards support all 5:', 'bookstore' in content and 'superstore' in content and 'hospital' in content and 'retail' in content and 'etl' in content)
