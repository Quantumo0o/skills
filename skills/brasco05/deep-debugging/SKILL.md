# Deep Debugging Skill

**Kein blindes Fixen. Kein Raten. Erst beweisen, dann lösen.**

## Trigger-Wörter (Skill sofort laden)

Dieser Skill wird **sofort aktiviert** wenn der User eines dieser Wörter schreibt:
- `debug`, `debugg`, `debugge`, `debugging`
- `bug`, `bugfix`, `buggy`
- `broken`, `kaputt`, `geht nicht`, `funktioniert nicht`
- `fehler`, `error`, `crash`, `absturz`
- `tief debuggen`, `tief analysieren`, `schau tiefer`, `such mal tiefer`
- `immer noch kaputt`, `immer noch ein fehler`
- `warum funktioniert X nicht`, `was ist falsch`
- `401`, `403`, `500` (direkt als Nachricht)

---

## Wenn du diesen Skill liest: STOPP.

Leg alle Fix-Ideen beiseite. Du wirst NICHTS ändern bevor du die Ursache zu 100% kennst.

---

## PRE-PHASE — Quick Triage (30 Sekunden, IMMER zuerst)

Bevor du irgendwas analysierst — diese 5 Dinge in 30 Sekunden prüfen:

```
□ Server neu gestartet nach letzter Änderung?
□ ENV-Variablen korrekt gesetzt (auch in .env.local)?
□ npm install / yarn nach Package-Änderungen ausgeführt?
□ Datenbank-Migration gelaufen? (npx prisma migrate dev)
□ Browser-Cache geleert / Hard Reload (Ctrl+Shift+R)?
```

**Wenn eines davon "Nein" → erst das fixen, dann weiter.**
Wenn alle "Ja" → weiter zu Phase 1.

---

## PHASE 1 — Daten sammeln (nur beobachten, nichts anfassen)

Beantworte diese 4 Fragen mit echten Beweisen aus Logs/Code:

### 1. Was genau passiert?
- Exakte Fehlermeldung oder Stack Trace aus den Logs
- HTTP Status Code (401? 403? 500? Redirect?)
- Welcher Endpoint / welche Funktion / welcher Service ist betroffen
- Was sieht der User vs. was passiert im Backend

### 2. Wann passiert es?
- Immer oder nur manchmal?
- Nur bei bestimmten Usern / Rollen / Inputs?
- Seit wann — nach welchem Commit / welcher Änderung?
- Reproduzierbar in welchen Schritten genau?

### 3. Was sollte stattdessen passieren?
- Erwartetes Verhalten klar in einem Satz benennen
- Tatsächliches Verhalten klar in einem Satz benennen

### 4. Was wurde zuletzt geändert?
- Letzter relevanter Commit
- Neue ENV-Variablen, neue Abhängigkeiten, neue Migrationen?

**→ STOPP. Erst wenn alle 4 Fragen beantwortet sind: weiter zu Phase 2.**

---

## PHASE 2 — Hypothese aufstellen (PFLICHT)

Formuliere EINE konkrete, testbare Hypothese bevor du irgendetwas anfasst:

```
"Der Fehler tritt auf weil [konkrete Ursache],
was ich beweise/widerlege indem ich [konkreter Test]."
```

**Gute Hypothese:**
```
"Der User wird rausgeworfen weil das JWT nach dem Login nicht 
korrekt im Cookie gesetzt wird, was ich beweise indem ich 
den Set-Cookie Header in der Login-Response in den Backend 
Logs überprüfe."
```

**Schlechte Hypothese:**
```
"Irgendwas stimmt mit der Auth nicht."
→ Zu vage. Nochmal. Konkrete Ursache benennen.
```

**Melde die Hypothese bevor du weitermachst.**
Format: `🔬 HYPOTHESE: [deine Hypothese]`

---

## PHASE 3 — Binary Search (Fehler eingrenzen)

Teile das Problem in zwei Hälften. Teste eine Hälfte.
- Liegt der Fehler dort → weiter aufteilen
- Liegt er nicht dort → andere Hälfte testen

### Für Auth/Session-Bugs (häufigster Fall):
```
Schritt 1: Login-Request → wird JWT korrekt generiert?
 → Logs: POST /auth/login → 200 oder Fehler?

Schritt 2: JWT im Response → landet er korrekt beim Client?
 → Set-Cookie Header vorhanden? LocalStorage befüllt?

Schritt 3: Folge-Request → wird JWT mitgeschickt?
 → Authorization: Bearer [token] im Request-Header? Cookie present?

Schritt 4: Guard/Middleware → wird JWT korrekt validiert?
 → JwtAuthGuard wirft 401? Welche Fehlermeldung?

Schritt 5: JWT_SECRET → ist er korrekt gesetzt?
 → Gleicher Secret beim Generieren (JwtModule) und Validieren (JwtStrategy)?
```

### Für allgemeine API-Bugs:
```
Request rein → Middleware → Guard → Controller → Service → DB → Response
     ↑              ↑          ↑         ↑           ↑
     Wo bricht die Kette? Jeden Schritt einzeln testen.
```

### Für Frontend-Bugs (React/Next.js):
```
User-Action → Event Handler → State-Update → Re-render → API-Call → Response → UI-Update
     ↑               ↑              ↑             ↑           ↑          ↑
     Wo bricht die Kette?

Checkliste:
□ Console.log DIREKT nach dem Event: kommt die Action überhaupt an?
□ State korrekt? (React DevTools → Components → State inspizieren)
□ useEffect dependencies richtig? (zu wenige → stale closure, zu viele → infinite loop)
□ API-Call: Network Tab → Request Payload korrekt? Response korrekt?
□ Hydration Error: passiert nur SSR? Client-only Code in Server Component?
□ Keys fehlen in Liste? → React warnt, aber rendert falsch
□ Async State: wird State gesetzt bevor Component unmounted?
```

### Für Datenbank-Bugs (Prisma/TypeORM):
```
□ Schema stimmt mit Migration überein? → prisma db push oder migrate dev
□ Fehlende Relation: include/join vergessen?
□ Null-Safety: Feld optional aber kein null-check?
□ Transaction abgebrochen: welcher Teil schlägt fehl?
□ Connection Pool erschöpft: zu viele offene Connections?

Prisma Debug-Modus aktivieren:
const prisma = new PrismaClient({ log: ['query', 'error', 'warn'] })
→ Zeigt jeden SQL-Query mit Parametern
```

### Für Performance-Bugs:
```
□ N+1 Problem: wird in einer Schleife jedes Mal eine DB-Query gemacht?
□ Missing Index: EXPLAIN ANALYZE auf den langsamen Query
□ Re-renders: React DevTools Profiler → was rendert unnötig?
□ Bundle Size: next build → welche Packages sind zu groß?
□ Memory Leak: Interval/EventListener nicht aufgeräumt bei unmount?
```

**Melde nach jeder Testphase:**
- ✅ [Schritt X] OK — Fehler liegt nicht hier
- ❌ [Schritt X] FEHLER GEFUNDEN — [was genau]

---

## PHASE 4 — Fix (erst jetzt)

Nur wenn die Ursache durch Phase 1-3 bewiesen ist:

1. **Minimalen Fix implementieren** — nur das was den Fehler behebt, nichts anderes
2. **Nicht gleichzeitig refactoren** — ein Problem, ein Fix
3. **Direkt testen** ob der spezifische Fehler weg ist
4. **Verification** ausführen bevor "fertig" gemeldet wird

---

## Häufige Fehlerquellen (NestJS/Next.js-Stack)

| Symptom | Zuerst prüfen |
|---|---|
| User wird nach Login rausgeworfen | JWT_SECRET Mismatch zwischen JwtModule und JwtStrategy, Cookie SameSite/Secure Settings, CORS-Config |
| HTTP 401 bei authentifizierten Requests | JWT expired, falscher Secret, Bearer Token fehlt im Header, `validate()` wird nicht aufgerufen |
| HTTP 403 | Rolle fehlt, Guard-Logik prüfen, Tenant-Isolation blockiert |
| HTTP 500 ohne Stack Trace | Unbehandelte Promise-Rejection, console.error in Logs suchen |
| "Cannot read property of undefined" | Null-checks fehlen, DB-Query gibt null zurück |
| Route nicht gefunden (404) | Module nicht in AppModule importiert, falscher Controller-Prefix, Global-Prefix-Dopplung (api/api/) |
| DB-Fehler beim Start | Migration nicht ausgeführt, Spalte existiert nicht, ENV-Variable fehlt |
| Cookie wird nicht gesetzt | SameSite=None + Secure=true nötig bei Cross-Origin; SameSite=Lax für same-site |
| Cookie wird nicht mitgeschickt | Cross-Origin Fetch braucht `credentials: 'include'`, Next.js Rewrites funktionieren nur SSR-seitig |
| JWT Strategy extrahiert Token aber 401 | `secretOrKey` in JwtStrategy stimmt NICHT mit secret in JwtModule überein (Fallback-Wert-Problem!) |
| Hydration Error (Next.js) | Client-only API (window/localStorage) in Server Component, Date/Math.random() Mismatch |
| Infinite Re-render Loop | useEffect dependency array falsch, State-Update in Render-Funktion |
| "React Hook called conditionally" | useState/useEffect NACH einem Early Return — alle Hooks VOR Early Returns |
| Prisma: "Unknown field" | Schema geändert aber kein `prisma generate` ausgeführt |
| CORS Error trotz CORS-Config | Preflight OPTIONS-Request nicht behandelt, Origin-Whitelist unvollständig |

---

## Debugging-Tools

### NestJS Backend
```bash
# Live-Logs mit tee
npm run start:dev 2>&1 | tee /tmp/backend-debug.log

# JWT manuell dekodieren
echo "$TOKEN" | cut -d. -f2 | base64 -d | jq .

# Login + /me curl-Test
curl -X POST http://localhost:4000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"...","password":"..."}' \
  -c /tmp/cookies.txt -v 2>&1 | grep "Set-Cookie"

curl http://localhost:4000/api/auth/me \
  -b /tmp/cookies.txt -v 2>&1 | grep "HTTP"
```

### Prisma
```bash
# Alle Queries loggen
DATABASE_URL=... npx prisma studio   # DB direkt inspizieren

# Migration Status prüfen
npx prisma migrate status

# Schema mit DB vergleichen
npx prisma db pull  # zieht aktuelles DB-Schema
```

### React / Next.js
```bash
# Build-Fehler analysieren
next build 2>&1 | grep -E "Error|Warning"

# Bundle-Größe analysieren
ANALYZE=true next build  # mit @next/bundle-analyzer

# TypeScript-Fehler finden
tsc --noEmit
```

### Allgemein
```bash
# Letzten Commit der eine Datei geändert hat
git log --oneline --follow -p -- src/auth/jwt.strategy.ts | head -50

# Wann hat ein Bug angefangen? Binary search in Git
git bisect start
git bisect bad HEAD
git bisect good [letzter-funktionierender-commit]
```

---

## Reporting-Format (PFLICHT nach jedem Debugging)

```
🔍 DEBUG REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fehler: [Exakte Fehlermeldung aus Logs]
Lokalisiert: [Datei:Zeile / Funktion / Service]
Ursache: [Was wirklich passiert ist — eine klare Erklärung]
Beweis: [Wie die Ursache bewiesen wurde]
Fix: [Was genau geändert wurde — Datei + was]
Verifiziert: [Ja — wie getestet, welcher Test grün]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Absolute Regeln

- **NIEMALS** fixen ohne Hypothese aus Phase 2
- **NIEMALS** mehrere Dinge gleichzeitig ändern
- **NIEMALS** "probieren ob es hilft" — nur beweisbasierte Fixes
- **NIEMALS** Phase überspringen weil der Fix "offensichtlich" wirkt
- Wenn nach 3 Fix-Versuchen der Bug noch existiert → zurück zu Phase 1, neue Hypothese
- **Scope-Disziplin:** Nur den gemeldeten Bug fixen, keine anderen Baustellen anfassen

---

## Lessons Learned (aus echten Bugs)

### JWT Secret Mismatch (2026-03-19)
**Symptom:** User wird nach Login sofort rausgeworfen, `/auth/me` gibt 401

**Falle:** `JwtModule.register()` und `JwtStrategy` hatten **unterschiedliche Fallback-Secrets**:
- Login signierte mit: `'caresys-super-secret-jwt-key-2026'`
- Strategy verifizierte mit: `'fallback-secret-for-dev'`

**Beweis-Methode:** `validate()` in JwtStrategy temporär loggen → wurde NIE aufgerufen → Signatur-Verifikation schlägt fehl → Secrets stimmen nicht überein

**Fix:** Fallback-Secret in `jwt.strategy.ts` angleichen:
```typescript
secretOrKey: process.env.JWT_SECRET || 'caresys-super-secret-jwt-key-2026',
```

### Cross-Origin Cookie Problem (2026-03-19)
**Symptom:** Login erfolgreich, aber alle API-Calls geben 401

**Falle:** `fetch()` vom Browser sendet Cookies **NICHT** bei Cross-Origin-Requests (localhost:3000 → localhost:4000), auch wenn `credentials: 'include'` gesetzt ist und Next.js Rewrites konfiguriert sind.

**Warum Next.js Rewrites nicht helfen:** Rewrites funktionieren nur für **SSR-seitige** Requests, nicht für client-side `fetch()`.

**Fix:** Sicherstellen dass alle API-Calls über die **gleiche Origin** laufen (Next.js als Proxy) ODER JWT auch im Response-Body zurückgeben und im `Authorization` Header senden.

### NestJS Controller-Prefix-Dopplung (2026-03-21)
**Symptom:** API-Endpoint gibt 404, obwohl Controller und Route korrekt aussehen

**Falle:** Global Prefix `api` + Controller-Pfad `api/something` → `/api/api/something` → 404

**Fix:** Controller-Pfad niemals mit `api/` prefixen. Nur den Ressourcennamen:
```typescript
@Controller('users')  // ✅ → /api/users
@Controller('api/users')  // ❌ → /api/api/users
```

### React Rules of Hooks Violation (2026-03-22)
**Symptom:** "React Hook useState is called conditionally" Error, App crasht

**Falle:** `useState` oder `useEffect` nach einem Early Return:
```typescript
if (!user) return null  // ← Early Return
const [data, setData] = useState([])  // ← Hook DANACH → Fehler!
```

**Fix:** Alle Hooks VOR jeden Early Return verschieben:
```typescript
const [data, setData] = useState([])  // ← Erst Hooks
if (!user) return null  // ← Dann Early Return
```

### req.user.id vs req.user.sub (2026-03-22)
**Symptom:** `req.user.id` ist `undefined` in NestJS Controller, obwohl JWT korrekt

**Falle:** JWT-Standard speichert die User-ID in `sub`, nicht in `id`. NestJS JwtStrategy gibt das decoded JWT payload zurück — also `sub`, nicht `id`.

**Fix:** Immer `req.user.sub` statt `req.user.id` in NestJS-Controllern:
```typescript
@Get('me')
getMe(@Request() req) {
  return this.usersService.findOne(req.user.sub)  // ✅
}
```
