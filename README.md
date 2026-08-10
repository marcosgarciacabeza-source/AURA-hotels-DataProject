# 🏨 Hospitality Analytics: Executive Financial & Operational Dashboard (USALI Standard)

[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Industry](https://img.shields.io/badge/Industry-Hospitality_%26_Revenue_Management-0F172A)](#)

Un cuadro de mando de Business Intelligence diseñado para la toma de decisiones ejecutivas en el sector hotelero, modelado bajo el estándar **USALI** (*Uniform System of Accounts for the Lodging Industry*) y construido sobre una arquitectura dimensional en estrella (*Star Schema*).

---

## 📌 1. Visión General del Proyecto

Este proyecto aborda la necesidad de transformar transacciones operativas atomizadas (reservas, cargos de restaurante, comisiones de OTAs y costes fijos) en un flujo de información estratégica para comités de dirección y *Asset Managers* de un grupo hotelero.

El grupo gestiona **4 propiedades** con distintos perfiles (urbanos y vacacionales/resort), analizando el periodo **2023 - 2025** (incluyendo el lanzamiento operativo del *Hotel 04 - Alpine Retreat* en julio de 2024).

### 🎯 Objetivos de Negocio:
* **P&L Consolidado:** Monitorizar la conversión del Ingreso Bruto al Beneficio Operativo (**GOP**).
* **Revenue Management:** Analizar la eficiencia de precios (**ADR**), ocupación y el impacto de los costes de captación por canal (Directo vs. OTAs).
* **Márgenes Departamentales:** Evaluar la rentabilidad individual de Alojamiento, F&B y MICE.

---

## 🏗️ 2. Arquitectura del Modelo de Datos

El modelo sigue un diseño en estrella (*Star Schema*) optimizado para análisis de alto rendimiento en Power BI (VertiPaq Engine):

* **Tabla de Hechos (`Fact_Cargos_Diarios`):** Registra las transacciones diarias categorizadas por concepto, hotel y departamento.
* **Tablas de Dimensiones:**
  * `Dim_Calendario`: Dimensión temporal ordenada con claves compuestas `YYYYMM` (`AñoMesKey`) para ordenación cronológica.
  * `Dim_Hoteles`: Atributos de las propiedades (Ubicación, Capacidad, Tipo, Fecha de Apertura).
  * `Dim_Canales`: Segmentación de canales de distribución y estructuras de comisión asociadas.
  * `Dim_Capacidad`: Registro de habitaciones disponibles por hotel y fecha.

---

## 📐 3. Metodología & Métricas Clave (DAX)

Se implementaron medidas dinámicas utilizando patrones avanzados en DAX (`SWITCH`, `CALCULATE`, `SELECTEDVALUE`):

```dax
