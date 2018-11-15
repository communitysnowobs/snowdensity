# snowdensity

We have prepared a simple function in Matlab that will calculate snow water equivalent based on day, month, year, lat, lon, and snow depth at the observation point. In this .zip file you will find a single matlab (.m) function file and several folders containing climatological normals of precipitation and temperature. The function information is below.

function [SWE,DOY] = swe_calculator(Y,M,D,H,LAT,LON,CODE)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This function implements a power law regression in order to produce a
%value of snow water equivalent (SWE) based on various parameters
%associated with a snow depth measurement. The input variables can be
%scalars (single measurement) or vectors (batch measurements). The
%following information on units, etc., is critical.

%David Hill, Oregon State University
%October 2018

%SWE (output) - snow water equivalent (mm)
%H - snow depth (mm)
%Y - year
%M - month (1 --> 12)
%D - day (1 --> 31 (or 28, or 30, as appropriate))
%LAT - latitude. Positive for N. Hem.
%LON - longitude (signed). So, -120 or so for North America.
%CODE - 1 for CONUS, 2 for Alaska, 3 for British Columbia
%DOY - day of water year
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
