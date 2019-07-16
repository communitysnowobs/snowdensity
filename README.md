# snowdensity

We have prepared a simple function in Matlab that will calculate snow water equivalent   
based on day, month, year, lat, lon, and snow depth at the observation point. In this   
.zip file you will find a single matlab (.m) function file and two files containing   
climatological normals of winter precipitation (Dec-Jan-Feb) and temperature difference   
(diff between mean T of warmest month and mean T of coldest month).   
The function information is below.  

function [SWE,DOY] = swe_calculator(Y,M,D,H,LAT,LON)  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  

%This function implements a power law regression in order to produce a  
%value of snow water equivalent (SWE) based on various parameters  
%associated with a snow depth measurement. The input variables can be  
%scalars (single measurement) or vectors (batch measurements). The  
%following information on units, etc., is critical.  
  
%David Hill, Oregon State University  
%June 2019  
  
%SWE (output) - snow water equivalent (mm)  
%H - snow depth (mm)  
%Y - year  
%M - month (1 --> 12)  
%D - day (1 --> 31 (or 28, or 30, as appropriate))  
%LAT - latitude. Positive for N. Hem.  
%LON - longitude (signed). So, -120 or so for North America.  
%DOY - day of water year (Oct 1 is the origin, i.e. DOY=1)  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
