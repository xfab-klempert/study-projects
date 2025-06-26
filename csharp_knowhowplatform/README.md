# Projektablauf: Interne Know-how-Plattform

## **Projektziel**
Entwicklung einer internen Plattform für Know-how, Zertifikate und Wissenstransfer im Unternehmen.

**Haupttechnologien:**
- Programmiersprache: **C#**
- Backend-Framework: **ASP.NET Core WebAPI**
- Frontend: **Razor Pages** (klassisch, einfacher Einstieg) oder **Blazor Pages** (moderner, jedoch eher für Single Page Apps) oder (optional, fortgeschritten) **React**
- Datenbank (Wahlweise): **PostgreSQL** oder **MSSQL**  
- Authentifizierung: **JWT-Token**
- Datenzugriff: **Entity Framework Core**
- Microservice-Kommunikation: **REST API** (optional: RabbitMQ)

---

## **Wichtige Hinweise**
- Ich habe dir in jeden Abschnitt Lernlinks gepackt die dir weiter helfen  
  - Microsoft Learn bietet viele wichtige Informationen 
  - Baue ruhig erstmal in eigenen Projekt die Tutorials nach und dann wenn du es kannst erst in deine App 
  - du musst nicht alles gleich komplett bauen (zb Login/Register) sondern baue dir erstmal Buttons oder Felder zum Testen deiner Methoden die du dann wieder heraus nimmst  
- Nutze nur **eine Datenbank** (egal ob PostgreSQL oder MSSQL) - ist einfacher 
- **Alle Tabellen** (User, Skill, Certificate, Transfer, KnowledgeEntry, etc.) sind in dieser DB und sind über Foreign Keys/Beziehungen verbunden
- Der Azubi soll beim Setup entscheiden, ob er PostgreSQL oder MSSQL verwendet  
- bei jedem wichtigen, funktionsfähigen Entwicklungsschritt mache einen **Git Commit** damit du dein Fortschritt nicht verlierst und immer wieder bei Fehlern zurücksetzten kannst
    - Git Tutorial: https://rogerdudler.github.io/git-guide/index.de.html

## **Vorbereitungen** 
- [ ] Installiere dir **Visual Studio** (falls noch nicht installiert)
  - Paket **Webentwicklung** (ASP.NET) wird benötigt
  - (optional) .NET-Desktopentwicklung   
- [ ] Installiere dir MSSQL Server oder Postgres 

---

## **Meilenstein 1: Projekt Grundstruktur anlegen**

**Ziel:** Projektstruktur und erste Modelle
**Empfohlene Technologien:**  
- Git, ASP.NET Core WebAPI, Entity Framework Core

**Lernlinks & Ressourcen:**  
- [**WICHTIG! ASP.NET MVC Tutorial (auf jeden Fall mal durchgehen)**](https://learn.microsoft.com/de-de/aspnet/core/tutorials/first-mvc-app/start-mvc?view=aspnetcore-9.0&tabs=visual-studio)
- [**WICHTIG! Datenbank Tutorial**](https://learn.microsoft.com/de-de/aspnet/core/data/ef-mvc/?view=aspnetcore-9.0)
- [(optional) Interaktives C# Basic Tutorial - falls du noch die Grundlagen brauchst](https://www.w3schools.com/cs/index.php)
- [(optional) Razor Pages Tutorial](https://learn.microsoft.com/de-de/aspnet/core/tutorials/razor-pages/?view=aspnetcore-9.0)
- [(optional) Blazor Pages Tutorial](https://learn.microsoft.com/de-de/aspnet/core/blazor/tutorials/?view=aspnetcore-9.0)
- [(optional) WebApi Tutorial)](https://learn.microsoft.com/de-de/aspnet/core/tutorials/first-web-api?view=aspnetcore-9.0&tabs=visual-studio)

**Aufgaben:**
- [ ] Git-Repository anlegen (z.B. auf GitHub)
  - leg dir dafür ein Github Account mit deiner Firmen Mail an und nenne ihn am besten "xfab-[ANMELDENAME]"
- [ ] ASP.NET Core MVC Beispiel Projekt erstellen und mal starten
- [ ] Entity Framework Core über Nuget installieren (Provider je nach DB wählen: [Postgres](https://www.nuget.org/packages/Npgsql.EntityFrameworkCore.PostgreSQL), [MSSQL](https://www.nuget.org/packages/Microsoft.EntityFrameworkCore.SqlServer))
- [ ] Grundstruktur commiten 

---

## **Meilenstein 2: Datenmodell & User/Skill Service**

**Ziel:** User können sich registrieren, einloggen und ihr Know-how (Skills, Zertifikate) verwalten

**Empfohlene Technologien:**
- ASP.NET Core WebAPI, Entity Framework Core, JWT Auth, Razor/Blazor/React

**Aufgaben:**
- [ ] Modelle: User, Skill, Certificate, mit sinnvollen Relationen (z.B. User→Skills als M:N, User→Certificate als 1:N)
- [ ] CRUD-APIs (Create/Read/Update/Delete) für User, Skills, Zertifikate
  - Methoden um zu erstellen / zu updaten / zu lesen / zu löschen für jedes Modell 
- [ ] Page: Profil- und Skillverwaltung
  - Wie du das Frontend aufbaust ist dir überlassen, am Ende plan nur am besten vorher wie so ein Webservice aufgebaut sein könnte (Home mit suche, Profil für jeden Nutzer, etc.)
- [ ] Datenbankverbindung testen, Migrationen einspielen
- [ ] Registrierung & Login (optional über JWT, ansonsten simple bauen)

**Links & Ressourcen:**  
- [EF Core Relationships (1:1, 1:N, N:M)](https://learn.microsoft.com/en-us/ef/core/modeling/relationships/)
- [JWT Auth in ASP.NET Core](https://learn.microsoft.com/de-de/aspnet/core/security/authentication/configure-jwt-bearer-authentication?view=aspnetcore-9.0)
- [Blazor Getting Started](https://learn.microsoft.com/en-us/aspnet/core/blazor/get-started)

---

<br><br>
## Ab hier hast du komplette Freiheit wie du es baust, hauptsache die Grundlegenden Funktionen sind erfüllt, also falls du Ideen für eigene hast bau es ruhig ein

## **Meilenstein 3: Home - Suche & Matching**

**Ziel:** User können gezielt nach Know-how im Unternehmen suchen, Hilfe Anfragen stellen und sich für Hilfestellungen melden

**Aufgaben:**
- [ ] Skill-Suche (nach Name, Level, User, Zertifikat, etc.)
   - UI: Suchmaske, Ergebnisanzeige
- [ ] Matching-Funktion: „Wer kann mir zu Thema X helfen?“
  - Eigenes Modell für Anfrage mit CRUD
  - UI: Anfrage Formular, Übersicht, Möglichkeit sich zurückzumelden 

---

## **Meilenstein 4: Know-how-Transfer**

**Ziel:** Nutzer können KnowHow Transfers erstellen oder Anfragen (beachte das abzubilden). Andere Nutzer können sich anmelden als Hörer oder Speaker. 

**Aufgaben:**
- [ ] Know How Transfer Sektion 
  - Transfer-Modell mit CRUD 
  - UI: Transfer erstellen, Anfragen managen, zurückmelden 

---

<br><br>
##  Ab hier setze ich dir keine Aufgaben mehr, da du selbst planen sollst.
- Jedoch wichtig: Du baust eigene API MicroServices (ohne Frontend) welche später angebunden werden können aber eigenständig laufen


## **Meilenstein 5: Wissensspeicher - eigener Webservice (optional, fortgeschritten)**

**Ziel:** Beiträge/Vorträge im System ablegen, durchsuchen, verknüpfen

**Empfohlene Technologien:**
- REST, eigene API, eigene Tabellen 
- optional eigene DB - z.B. bei Postgres in ein Cluster möglich, bei MSSQL musst du schauen ob es deine Version zulässt

---

## **Meilenstein 6: Notification-Service - eigener Webservice (optional, fortgeschritten)**

**Ziel:** Asynchrone Benachrichtigungen bei Transfers/Anfragen

**Empfohlene Technologien:**
- RabbitMQ, Rebus(optional), eigene API

**Links & Ressourcen:**
- [RabbitMQ Getting Started](https://www.rabbitmq.com/getstarted.html)
- [Rebus](https://rebus.fm/what-is-rebus/)

---

<br><br>
## **Abschluss & Refactoring**

**Ziel:** Doku, Präsentation, Codequalität

**Aufgaben:**
- [ ] Readme & technische Doku
- [ ] Präsentation/Demo
- [ ] Optional: Automatisierte Tests, CI/CD

**Links & Ressourcen:**
- [README Best Practices](https://www.makeareadme.com/)

---

<br><br>
## **Bonus-Meilenstein: Docker & Orchestrierung (optional, für Deployment und Teamarbeit)**

**Ziel:** Deployment mit Docker Compose, lokale Infrastruktur und Team-Onboarding vereinfachen

**Empfohlene Technologien:**
- Docker, Docker Compose, Portainer(als UI für Docker)

**Aufgaben:**
- [ ] Schreibe die Dockerfiles für die verschiedenen Apps
- [ ] Erstelle ein `docker-compose.yml`, um alles als Stack zu starten 
  - Wahlweise für PostgreSQL oder MSSQL (Beispiele: [Postgres Compose](https://hub.docker.com/_/postgres), [MSSQL Compose](https://hub.docker.com/_/microsoft-mssql-server))
- [ ] Dokumentiere im Readme, wie alles per Compose gestartet wird
- [ ] Optional: RabbitMQ in Compose einbinden, falls Notification-Service genutzt wird

**Links & Ressourcen:**
- [Docker Tutorial](https://docs.docker.com/get-started/workshop/)
- [Docker Compose Dokumentation](https://docs.docker.com/compose/)
- [Containerisieren einer .NET-App](https://learn.microsoft.com/de-de/dotnet/core/docker/build-container?tabs=windows&pivots=dotnet-9-0)
- [Portainer](https://www.portainer.io/)

---

**Viel Erfolg!**