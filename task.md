# Bayesian Analysis of Temperature Variation Across Altitude in Ticino (2025)
## Introduction
This project analyzes the average temperature for every month in 2025 across 21 different meteorological stations in Canton Ticino, Switzerland. The data is sourced from the OASI (Osservatorio Ambientale e Stazioni di Inquinamento) database, which provides environmental and atmospheric measurements from multiple monitoring points throughout the canton.

## Motivation and Research Question
The primary motivation is to understand how altitude affects temperature patterns in Ticino, a region characterized by significant topographical variation. Altitudes in our dataset range from 190m (Verbano/Valle Maggia) to 1850m (Robiei), creating an ideal setting to study altitudinal temperature gradients—a fundamental concept in atmospheric science.

Our central research hypothesis is: Temperature patterns differ significantly between high-altitude (>900m) and low-altitude (<300m) stations, with higher altitudes showing systematically lower temperatures.

Data Structure and Hierarchical Nature
This dataset naturally exhibits a hierarchical structure, making it ideal for Bayesian hierarchical modeling:

Level 1 (Observations): Monthly temperature measurements (12 months × 21 stations = 252 observations)

Level 2 (Groups): Individual meteorological stations

Covariates: Altitude, latitude, longitude, season

This hierarchical structure allows us to:

Model station-specific temperature patterns while borrowing strength from the population level

Compare pooled, unpooled, and hierarchical approaches to inference

Make predictions for new (unobserved) stations based on the population distribution

## Dataset Overview
Source: OASI Database (www.ti.ch/oasi)
Temporal Coverage: 2025 (12 months)
Spatial Coverage: 21 meteorological stations across Canton Ticino
Variables:

Station name and geographic coordinates (latitude, longitude)

Monthly average temperature (°C)

Station altitude (m above sea level, range: 190–1850m)

Month (1–12)

Season flag (0=Winter, 1=Spring, 2=Summer, 3=Autumn)

Data Quality: All measurements are aggregated as monthly averages with provisional data flags marked where applicable.

Bayesian Methodology Overview
This analysis employs Bayesian inference across multiple components:

Hypothesis Testing: Testing whether temperature differences between altitude classes are practically significant using ROPE (Region of Practical Equivalence)

Regression Modeling: Estimating the relationship between altitude and temperature, including robust regression to handle potential outliers

Hierarchical vs. Unpooled Models: Comparing complete pooling, no pooling, and partial pooling approaches using information criteria (WAIC)

Posterior Predictive Checks: Custom implementation of predictive checks to validate model fit without relying on automatic PPC functions

Report Structure
The remainder of this report is organized as follows:

Exploratory Data Analysis (EDA): Descriptive statistics and visualizations of temperature distribution across stations, seasons, and altitudes

Hypothesis Test: Bayesian test of altitude effect on temperature with prior sensitivity analysis and frequentist comparison

Regression Model: Linear and robust regression models for temperature as a function of altitude

Hierarchical Analysis: Implementation and comparison of unpooled and hierarchical normal models

Model Comparison: WAIC-based model comparison and discussion of implications

Conclusions: Summary of findings and insights for future work

