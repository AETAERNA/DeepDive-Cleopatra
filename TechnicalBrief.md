# Technical Brief – Deep Dive I: Cleopatra’s Tomb

## Background

*Taposiris Magna* is a Ptolemaic temple complex west of Alexandria that has long been proposed as the final resting place of **Cleopatra VII** and **Mark Antony**.  In 2013, Abbas et al. published the results of a **Phase II geophysical survey** employing very‑low‑frequency electromagnetic (VLF‑EM) profiling and two‑dimensional resistivity imaging beneath the Osiris‑Isis temple.  Among several features, they identified a **deep resistive anomaly** roughly 20 × 20 m in size at a depth of 25–45 m.  The anomaly was interpreted as either a lithological variation or a potential cavity but was not investigated further.

In 2025, marine archaeologists led by **Dr. Kathleen Martínez** and **Dr. Robert Ballard** discovered a **submerged ancient port** off the coast near Taposiris and mapped a **1.3 km tunnel** extending from the temple toward the Mediterranean Sea.  Artifacts recovered from this corridor—including coins minted during Cleopatra’s reign, amphorae, and architectural fragments—suggest that the tunnel and port were part of a Ptolemaic ceremonial or funerary infrastructure.

## Objectives

This project revisits the 2013 survey data in light of the 2025 marine discoveries.  The goals are to:

1. **Geo‑align the Phase II anomaly** with the newly mapped tunnel trajectory and port structures.
2. **Simulate muon radiography signatures** to evaluate whether a void of the anomaly’s size could be detected with portable muon detectors.
3. **Implement a certainty scoring model** that quantifies the likelihood that a candidate coordinate and depth correspond to the anomaly and the tunnel.
4. **Develop visual tools**—including interactive maps and heatmaps—to support non‑invasive targeting and future excavation planning.

## Methods

### Data Integration

The Phase II anomaly is digitised as a GeoJSON polygon (see `data/geojson/phase2_refined_deep_zone.geojson`).  Coordinates are refined from Fig. 23 of Abbas et al. (2013) and geospatially aligned with the 2025 tunnel path and submerged port location.  This unified model serves as the basis for all subsequent simulations and visualisations.

### Muon Tomography Simulation

Muon radiography leverages the attenuation of cosmic‑ray muons as they pass through rock.  Air‑filled cavities allow a greater fraction of muons to traverse a given path than solid rock.  A simplified grid‑based model (see `code/muon_tomo_sim.py`) calculates the expected muon flux excess (%) across a 50 × 50 m area containing a 20 × 20 m void.  Overburden thickness is reduced along the tunnel path to emulate the lower density corridor.  Peaks in the simulated flux excess (>20 %) suggest that a cavity would be detectable over background rock with detectors deployed for several months.

### Certainty Scoring

The function `compute_certainty` defined in `code/confidence_model.py` assigns a certainty score to any longitude/latitude/depth triple.  A baseline score (0.87) reflects the confidence in the Phase II anomaly’s reality.  The score is increased if:

- The point falls within the anomaly polygon and between 25 m and 45 m depth (× 1.15).
- The point is within 20 m of the tunnel line (× 1.20).

The score is decreased for depths shallower than 30 m (× 0.85).  Values are capped at 1.0.  This framework allows rapid prioritisation of candidate drill sites or excavation zones.

### Visualisation

An interactive map created with Folium (`code/make_phase2_preview_map.py`) overlays the anomaly polygon, the 2025 tunnel, and the submerged port on satellite imagery.  Users can explore the spatial relationships and zoom in on areas of interest.  A muon flux heatmap produced by the simulation script visualises how the void and tunnel manifest as a positive flux anomaly against the limestone background.

## Recommendations

1. **Non‑Invasive Verification:** Deploy portable muon detectors above the anomaly to measure muon flux and confirm the presence of an air‑filled cavity.  Complement this with 3D electrical resistivity and magnetotelluric surveys over a 50 × 50 m grid to refine the anomaly boundaries.
2. **Targeted Excavation:** If non‑invasive data indicate a significant void, plan a minimally invasive borehole under strict archaeological supervision to verify the chamber’s existence and contents.
3. **Extension to Other Sites:** Apply the PT‑EL methodology to other Ptolemaic or Hellenistic sites where historical conjecture suggests hidden tombs (e.g., Alexandria’s royal quarter).

## Conclusion

By combining legacy geophysical data, recent archaeological discoveries, and AI‑assisted modeling, this project offers a systematic approach to evaluating deep subsurface anomalies.  The tools provided here are modular and extensible, laying the foundation for future **Deep Dive** volumes into ciphers, lost devices, and other mysteries where data integration and predictive modeling can shed light on the past.