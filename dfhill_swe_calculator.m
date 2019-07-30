function [SWE,DOY] = dfhill_swe_calculator(Y,M,D,H,LAT,LON)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%This function implements a power law regression in order to produce a
%value of snow water equivalent (SWE) based on various parameters
%associated with a snow depth measurement. The input variables can be
%scalars (single measurement) or vectors (batch measurements). The
%following information on units, etc., is critical.

%David Hill, Oregon State University
%June 2019

%SWE (output) - snow water equivalent (mm)
%DOY (output) - day of water year (Oct 1 is the origin, i.e. DOY=1)
%H - snow depth (mm)
%Y - year
%M - month (1 --> 12)
%D - day (1 --> 31 (or 28, or 30, as appropriate))
%LAT - latitude. Positive for N. Hem.
%LON - longitude (signed). So, -120 or so for North America.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%load grids for winter precipitation (PPTWT) and temperature difference
%(TD).
%See https://adaptwest.databasin.org/pages/adaptwest-climatena for info on
%data.
%See http://www.cacpd.org.s3-website-us-west-2.amazonaws.com/climate_normals/NA_ReadMe.txt
%for specific metadata. The grids that I have included with this calculator
%have been put into geographic coords and they have been clipped to
%(72>lat>30) and (-168<lon<-60).

%load the temp difference data. As coded below, files need to be in same
%directory as this script. That is easily changed.
[td,R]=arcgridread('td_final.txt');

%load the winter precip data.
[pptwt,R]=arcgridread('ppt_wt_final.txt');

%convert R to MapCellsReference
R_map=refmatToMapRasterReference(R,size(td));

%now, do interpolation to get PPTWT and TD at the requested locations

TD=mapinterp(td,R_map,LON,LAT,'nearest');
PPTWT=mapinterp(pptwt,R_map,LON,LAT,'nearest');

%Next, we need to turn our year / month / day information into a 'day of
%water year' (DOY)

DOY=datenum(Y,M,D)-datenum(Y,9,30); %OCT 1 will have a DOY of 1
DOY(DOY<0)=DOY(DOY<0)+365; %make all values positive, in range of 1 --> 365

%finally, we apply the regression equation. First define the regression
%coefficients.

a=[0.0533 0.948 0.1701 -0.1314 0.2922]; %accumulation phase
b=[0.0481 1.0395 0.1699 -0.0461 0.1804]; %ablation phase

SWE=a(1)*H.^a(2).*PPTWT.^a(3).*TD.^a(4).*DOY.^a(5).*(-tanh(.01*(DOY ...
    - 180))+1)/2 + b(1)*H.^b(2).*PPTWT.^b(3).*TD.^b(4).*DOY.^b(5) .* ...
         (tanh(.01*(DOY-180))+1)/2;
end

