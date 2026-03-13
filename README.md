# Bug Hunter Pro 🔍

## AI-Powered Vulnerability Scanner for Bug Bounty Hunters

Bug Hunter Pro - это профессиональный инструмент для поиска уязвимостей, предназначенный для баг-баунти охотников, исследователей безопасности и специалистов по пентестингу. Инструмент автоматизирует процесс обнаружения уязвимостей OWASP Top 10 и генерирует детальные отчеты.

### 🚀 Возможности

- ✅ **Автоматическое сканирование** - Обход сайтов и автоматическое обнаружение уязвимостей
- ✅ **OWASP Top 10 Detection** - Обнаружение XSS, SQLi, LFI, SSRF, XXE и других уязвимостей
- ✅ **AI-Powered анализ** - Интеграция с Groq AI для интеллектуального анализа
- ✅ **Многопоточное сканирование** - Быстрая обработка множества URL
- ✅ **Детальные отчеты** - JSON отчеты с описанием найденных уязвимостей
- ✅ **Гибкая конфигурация** - YAML конфигурация с кастомными payloads
- ✅ **Bug Bounty готовность** - Отчеты готовы для отправки на HackerOne, Bugcrowd, Intigriti

### 📦 Установка

#### Требования
- Python 3.8+
- pip

#### Быстрая установка

```bash
# Клонировать репозиторий
git clone https://github.com/aldaniyar1978/bug-hunter-pro.git
cd bug-hunter-pro

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Установить зависимости
pip install -r requirements.txt
```

### ⚙️ Конфигурация

Скопируйте `config.yaml` и добавьте ваш Groq API ключ:

```yaml
groq:
  api_key: "your-groq-api-key-here"
  model: "mixtral-8x7b-32768"
```

Получить API ключ можно на [Groq Console](https://console.groq.com/)

### 🎯 Использование

#### Базовое сканирование

```bash
python scanner.py -u https://example.com
```

#### С кастомной конфигурацией

```bash
python scanner.py -u https://example.com -c my_config.yaml
```

#### Параметры командной строки

```
-u, --url       Целевой URL для сканирования (обязательно)
-c, --config    Файл конфигурации (по умолчанию: config.yaml)
```

### 📊 Примеры использования

#### Сканирование веб-приложения

```bash
python scanner.py -u https://target-website.com
```

#### Результат:
```
╔═══════════════════════════════════════════════════════════╗
║           Bug Hunter Pro - Vulnerability Scanner        ║
║              AI-Powered Bug Bounty Tool                  ║
╚═══════════════════════════════════════════════════════════╝

[+] Starting scan on: https://target-website.com
[*] Crawling website...
[+] Found 15 URLs
[*] Scanning: https://target-website.com/login
[*] Scanning: https://target-website.com/search

============================================================
SCAN RESULTS
============================================================
[!] Found 2 vulnerabilities

[1] XSS - High
    URL: https://target-website.com/search?q=<script>alert(1)</script>
    Payload: <script>alert(1)</script>
    Description: Reflected XSS vulnerability detected

[2] SQL Injection - Critical
    URL: https://target-website.com/user?id=' OR 1=1--
    Payload: ' OR 1=1--
    Description: SQL Injection vulnerability detected

[+] Report saved to: report_20250313_104530.json
```

### 🔍 Обнаруживаемые уязвимости

1. **Cross-Site Scripting (XSS)**
   - Reflected XSS
   - Stored XSS
   - DOM-based XSS

2. **SQL Injection (SQLi)**
   - Error-based SQLi
   - Boolean-based SQLi
   - Time-based blind SQLi

3. **Local File Inclusion (LFI)**
   - Path traversal
   - File disclosure

4. **Remote File Inclusion (RFI)**
   - Remote code execution
   - File upload vulnerabilities

5. **Server-Side Request Forgery (SSRF)**
   - Internal port scanning
   - Cloud metadata access

6. **XML External Entity (XXE)**
   - File disclosure via XXE
   - SSRF via XXE

7. **Command Injection**
   - OS command injection
   - Code injection

8. **Open Redirect**
   - URL redirection vulnerabilities

### 📁 Структура проекта

```
bug-hunter-pro/
├── scanner.py           # Главный сканер
├── config.yaml          # Конфигурация
├── requirements.txt     # Python зависимости
├── Dockerfile          # Docker конфигурация
├── exploits/           # Модули сканирования
│   ├── __init__.py
│   ├── xss_scanner.py
│   ├── sqli_scanner.py
│   ├── lfi_scanner.py
│   └── ssrf_scanner.py
├── reports/            # Директория для отчетов
└── README.md
```

### 🐳 Docker

```bash
# Собрать образ
docker build -t bug-hunter-pro .

# Запустить сканирование
docker run bug-hunter-pro python scanner.py -u https://example.com
```

### 🛡️ Bug Bounty платформы

Bug Hunter Pro готов для работы с:

- [HackerOne](https://hackerone.com)
- [Bugcrowd](https://bugcrowd.com)
- [Intigriti](https://intigriti.com)
- [YesWeHack](https://yeswehack.com)
- [Synack](https://synack.com)

### 📝 Отчеты

Отчеты сохраняются в JSON формате со следующей структурой:

```json
[
  {
    "type": "XSS",
    "severity": "High",
    "url": "https://example.com/search?q=payload",
    "payload": "<script>alert(1)</script>",
    "description": "Reflected XSS vulnerability detected"
  }
]
```

### ⚠️ Ответственное использование

**ВАЖНО:** Этот инструмент предназначен только для легального тестирования безопасности.

- ✅ Используйте только на своих приложениях
- ✅ Получите письменное разрешение перед тестированием
- ✅ Следуйте правилам bug bounty программ
- ❌ НЕ используйте для несанкционированного доступа
- ❌ НЕ нарушайте законы о компьютерных преступлениях

### 🤝 Вклад в проект

Приветствуются pull requests! Для больших изменений, пожалуйста, сначала откройте issue.

### 📄 Лицензия

MIT License - смотрите файл LICENSE

### 👨‍💻 Автор

**aldaniyar1978**
- GitHub: [@aldaniyar1978](https://github.com/aldaniyar1978)

### 🔗 Полезные ресурсы

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [HackerOne Resources](https://www.hackerone.com/resources)
- [Bug Bounty Platforms List](https://github.com/disclose/bug-bounty-platforms)

### 📞 Поддержка

Если у вас возникли проблемы или вопросы, откройте [Issue](https://github.com/aldaniyar1978/bug-hunter-pro/issues)

---

⭐ Если этот проект был полезен, поставьте звезду на GitHub!

**Disclaimer**: Используйте этот инструмент ответственно и в соответствии с законами вашей юрисдикции.
