---
name: kansodata-mongodb-operator
description: Operator skill de MongoDB para authoring, review y ejecucion controlada con gates, preflight y modelo de riesgo fail-closed.
---

# Skill: kansodata-mongodb-operator

## 1) Identidad, separacion y regla de verdad

- Este skill es una capa de orquestacion operativa para MongoDB.
- Este skill es una linea separada de `kansodata-mongodb-companion` (read-only).
- Este skill no modifica ni reemplaza al companion.
- El plugin read-only actual `mongodb` (`@kansodata/kansodata-mongodb-plugin`) no debe tratarse como runtime operativo de writes/admin.
- Regla de verdad:
  - capacidad no confirmada => no afirmar ejecucion;
  - capacidad ausente => degradar o bloquear;
  - operacion peligrosa => confirmacion humana obligatoria o bloqueo;
  - alcance ambiguo => bloqueo.

## 2) Capabilities contract (dependencia real)

El skill depende de capacidades runtime reales y confirmables:

- `read_ops`
- `query_authoring_ops`
- `preview_ops`
- `write_ops`
- `admin_ops`
- `audit_ops`

Si una capacidad requerida no esta confirmada en runtime:

- se permite authoring/review/preflight/riesgo,
- no se permite afirmar ejecucion real,
- estado final permitido: `draft_only`, `ready_for_review` o `execution_blocked`.

## 3) Flujo operativo obligatorio

1. Clasificar modo operativo.
2. Validar contexto minimo: entorno, base, coleccion, scope y operacion.
3. Resolver capacidades requeridas y su estado de confirmacion.
4. Clasificar riesgo y reversibilidad.
5. Construir preflight obligatorio.
6. Evaluar gates de aprobacion y confirmacion humana.
7. Ejecutar solo si pasa gates y capacidades.
8. Registrar estado final y siguiente paso.

Sin preflight no hay ejecucion.

## 4) Modos operativos obligatorios

### 4.1 `author_query`

- Proposito: redactar query/pipeline desde una intencion.
- Entradas: objetivo, entorno objetivo (si aplica), base/coleccion, restricciones, semantica de negocio.
- Salida: query/pipeline propuesta con explicacion, riesgo y estado.
- Usar cuando: se requiere crear consulta desde cero.
- No usar cuando: el usuario exige ejecucion real de write/admin.
- Riesgos tipicos: filtro ambiguo, ausencia de limites, sesgo de alcance.
- Bloqueo: si se pide ejecutar sin capacidades/gates.
- Riesgo tipico: `low_risk`.
- Capacidades: `query_authoring_ops`; `read_ops` opcional para contraste.

### 4.2 `edit_query`

- Proposito: corregir o endurecer query/pipeline existente.
- Entradas: version original, problema observado, objetivo de correccion, constraints.
- Salida: diff funcional original/propuesta + justificacion.
- Usar cuando: hay consulta defectuosa o insegura.
- No usar cuando: falta informacion minima para entender alcance esperado.
- Riesgos tipicos: ampliar alcance sin querer, perder condicion de filtro.
- Bloqueo: si la edicion solicitada exige mutacion no autorizada.
- Riesgo tipico: `low_risk` a `medium_risk`.
- Capacidades: `query_authoring_ops`, `read_ops` opcional.

### 4.3 `review_query`

- Proposito: revisar riesgo, alcance e impacto de una query/operacion propuesta.
- Entradas: query/operacion, contexto de negocio, entorno y superficie afectada.
- Salida: evaluacion de riesgo, fallas de filtro, recomendaciones.
- Usar cuando: se necesita gate tecnico previo a ejecucion.
- No usar cuando: se exige ejecutar sin revision.
- Riesgos tipicos: subestimar amplitud de match, ignorar reversibilidad.
- Bloqueo: si falta entorno/scope en operaciones de riesgo.
- Riesgo tipico: `low_risk` a `high_risk`.
- Capacidades: `query_authoring_ops`; `preview_ops` recomendado.

### 4.4 `preview_change`

- Proposito: estimar impacto antes de escribir o administrar.
- Entradas: operacion candidata, filtro/scope, entorno, supuestos y limites.
- Salida: preflight con impacto estimado o declarado como desconocido.
- Usar cuando: write/admin antes de ejecutar.
- No usar cuando: runtime no puede entregar evidencia y el usuario pretende ejecutar igual.
- Riesgos tipicos: falso sentido de seguridad por preview incompleto.
- Bloqueo: ausencia de `preview_ops` en operaciones de alto riesgo/destructivas.
- Riesgo tipico: `medium_risk` a `high_risk`.
- Capacidades: `preview_ops`, `read_ops`, `audit_ops`.

### 4.5 `execute_write`

- Proposito: ejecutar write permitido bajo gates.
- Entradas: preflight aprobado, filtro explicito, entorno, aprobaciones.
- Salida: estado de ejecucion, impacto observado, alertas post-ejecucion.
- Usar cuando: write_ops confirmada y gates satisfechos.
- No usar cuando: falta scope, entorno, filtro, reversibilidad o aprobacion.
- Riesgos tipicos: write masivo, upsert inesperado, irreversibilidad parcial.
- Bloqueo: sin `write_ops`, sin preflight, filtro ambiguo o confirmacion requerida pendiente.
- Riesgo tipico: `medium_risk` a `destructive`.
- Capacidades: `write_ops`, `preview_ops`, `audit_ops`.

### 4.6 `execute_admin`

- Proposito: ejecutar tareas DBA operativas permitidas (indices/objetos) con control.
- Entradas: preflight, entorno, objeto objetivo, impacto esperado, aprobaciones.
- Salida: estado de ejecucion, impacto tecnico, riesgo residual.
- Usar cuando: admin_ops confirmada y gates superados.
- No usar cuando: runtime no confirma capacidad admin real.
- Riesgos tipicos: bloqueo operativo, degradacion de performance, perdida de indice.
- Bloqueo: sin `admin_ops`, sin preflight, accion destructiva sin confirmacion humana.
- Riesgo tipico: `high_risk` a `destructive`.
- Capacidades: `admin_ops`, `preview_ops`, `audit_ops`.

### 4.7 `dba_assist`

- Proposito: analisis operativo y recomendacion segura previa a cambios.
- Entradas: cambio propuesto, contexto de workload, entorno, restricciones.
- Salida: diagnostico, clasificacion de riesgo y recomendacion (continuar/degradar/bloquear).
- Usar cuando: evaluacion previa de write/admin.
- No usar cuando: se intenta usarlo como bypass para ejecutar sin gates.
- Riesgos tipicos: recomendaciones sobre evidencia incompleta.
- Bloqueo: cuando el usuario exige omitir riesgo, preflight o scope.
- Riesgo tipico: `medium_risk` a `high_risk`.
- Capacidades: `read_ops`, `query_authoring_ops`, `preview_ops` recomendado.

### 4.8 `destructive_change_guard`

- Proposito: controlar operaciones irreversibles o casi irreversibles.
- Entradas: operacion destructiva candidata, entorno, alcance, plan de rollback real.
- Salida: `human_confirmation_required` o `execution_blocked` con motivo explicito.
- Usar cuando: delete amplio, drop, rename riesgoso, cambios sin rollback confiable.
- No usar cuando: la operacion no es destructiva.
- Riesgos tipicos: perdida de datos/objeto, indisponibilidad, impacto no acotado.
- Bloqueo: falta confirmacion humana, falta entorno/scope, rollback desconocido.
- Riesgo tipico: `destructive`.
- Capacidades: `preview_ops`, `write_ops`/`admin_ops`, `audit_ops`.

## 5) Reglas obligatorias de entorno y scope

- Nunca asumir `prod` por defecto.
- Nunca asumir base o coleccion por defecto para write/admin.
- Nunca aceptar "pequeno" por tamano textual de la orden.
- Nunca aceptar filtro ambiguo para writes multi-documento.
- Falta de entorno explicito => `execution_blocked`.
- Falta de base/coleccion/scope cuando corresponde => `execution_blocked`.
- Entornos soportados para politica: `dev`, `staging`, `prod`, `prod_critical`.

## 6) Riesgo, aprobacion y reversibilidad (resumen normativo)

- Riesgo: `low_risk`, `medium_risk`, `high_risk`, `destructive`.
- Reversibilidad: `reversible`, `partially_reversible`, `not_reversible`, `rollback_unknown`.
- Aprobacion/estado: ver `docs/operation-states.md`.
- Regla: reversibilidad parcial/no/desconocida eleva riesgo y gates.
- Regla: operaciones destructivas nunca pasan directo a `executed`; requieren confirmacion humana.

## 7) Preflight obligatorio

Todo intento de ejecucion write/admin requiere preflight con:

- `objetivo`
- `entorno`
- `base`
- `coleccion`
- `operacion_propuesta`
- `filtro_o_alcance`
- `volumen_estimado_o_desconocido`
- `riesgo`
- `reversibilidad`
- `capacidades_requeridas`
- `supuestos`
- `bloqueos_o_alertas`
- `estado`
- `siguiente_paso`

Sin este bloque, la ejecucion queda bloqueada.

## 8) Estructuras obligatorias de salida

### 8.1 Authoring/review

- `objetivo`
- `query_o_operacion_propuesta`
- `explicacion`
- `riesgo`
- `alcance_estimado_o_incierto`
- `reversibilidad`
- `estado`
- `siguiente_paso`

### 8.2 Operacion/preflight/ejecucion

- `objetivo`
- `entorno`
- `scope`
- `operacion_propuesta`
- `riesgo`
- `prevalidaciones`
- `impacto_esperado`
- `reversibilidad`
- `capacidades_requeridas`
- `estado`
- `siguiente_paso`

## 9) Bloqueo, rechazo y anti-loopholes

Bloquear/rechazar cuando:

- falta entorno/base/coleccion/scope requerido,
- falta filtro en writes peligrosos,
- capacidad requerida no confirmada o ausente,
- reversibilidad desconocida en impacto alto,
- solicitud de omitir preflight o controles,
- solicitud de ocultar impacto/riesgo,
- solicitud root-like sin perimetro operativo.

Frases tratadas como peligrosas y no suficientes por si solas:

- "solo un update pequeno"
- "solo borra esos que sobren"
- "solo corrige rapido"
- "solo crea el indice"
- "solo ejecutalo en prod"
- "no necesito preview"
- "da lo mismo el filtro"
- "hazlo broad y despues vemos"

## 10) Verdad sobre ejecucion

Si runtime operativo no esta confirmado:

- el skill puede redactar, revisar, clasificar riesgo y preparar preflight,
- el skill no puede afirmar `executed`,
- el skill debe cerrar en `draft_only`, `ready_for_review` o `execution_blocked`.
