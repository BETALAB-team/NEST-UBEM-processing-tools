%% Importazione delle coordinate geospaziali

% Percorso del file
file_path = 'Coordinate_GD.csv';

% Leggi il file .csv
data = readtable(file_path);


% Estrai le coordinate Web Mercator dalla colonna 2 e 3
lon = data.x_coordinates;
lat = data.y_coordinates;

% Converti le coordinate UTM in latitudine e longitudine (da usare se
% vengono fornite coordinate UTM)
% proj = projcrs(3857,'Authority','EPSG'); % Funzione di conversione
% [lat, lon] = projinv(proj, xx, yy);

coordinates = [lon,lat]; % Coordinate dei punti (longitudine, latitudine)

% Crea una mappa geografica
figure
geoplot(coordinates(:,2),coordinates(:,1),'o',...
    "MarkerSize",5,"MarkerEdgeColor","r", ...
    "MarkerFaceColor","r");
title('Case study: Padua historical center');
legend('Buildings')
geolimits([min(coordinates(:,2))-0.0005 max(coordinates(:,2))+0.0005],[min(coordinates(:,1)) max(coordinates(:,1))])

clearvars -except Risc Rafr ACS T_est names coordinates
% clearvars data file_path ans proj xx yy

%% Search for the minimum continuous linear path

% The coordinates variable represents the coordinates in latitude and 
% longitude of the points to be considered

% Calculates the Euclidean distance between all points
n = size(coordinates, 1); % Number of points to consider
distances = zeros(n, n); % Array distance initialisation 
for i = 1:n
    for j = 1:n
        distances(i, j) = sqrt((coordinates(i, 1) - coordinates(j, 1))^2 + (coordinates(i, 2) - coordinates(j, 2))^2);
    end
end

% I initialize the path as a sequential path
path = 1:n;

% Calculate the total length of the initial route
total_distance = sum(distances(sub2ind(size(distances), path, [path(2:end), path(1)])));

% Loop until there is no improvement
improved = true; % flag
while improved
    improved = false;
    % Loops on all possible exchanges of two points in the path
    for i = 1:n - 1
        for j = i + 1:n
            % Calculates path length after exchange
            new_path = path;
            new_path(i:j) = path(j:-1:i);
            new_distance = sum(distances(sub2ind(size(distances), new_path, [new_path(2:end), new_path(1)])));
            % If the length of the path after the exchange is shorter, make the exchange
            if new_distance < total_distance
                path = new_path;
                total_distance = new_distance;
                improved = true;
            end
        end
    end
end

% Plot della rete ideale
figure
geoplot(coordinates(path, 2), coordinates(path, 1),'-o',"LineWidth",2, ...
    "MarkerSize",5,"MarkerEdgeColor","r", ...
    "MarkerFaceColor","r");
title('Case study: Padua historical center');
legend('Thermal network (ideal)')
geolimits([min(coordinates(:,2))-0.0005 max(coordinates(:,2))+0.0005],[min(coordinates(:,1)) max(coordinates(:,1))])

% geobasemap satellite
% geobasemap streets-dark
% geobasemap topographic

% Calcolo del vettore distanze relative tra i punti del percorso
distanceRelative = zeros(size(coordinates,1),1); % Inizializzazione distanze relative
distanceRelative (1) = 1000; % Distanza del primo edificio dalla stazione centrale
lon = coordinates(:,1); lat = coordinates(:,2);
for ii = 1:(size(coordinates,1))-1
    distanceRelative(ii+1) = deg2km(distance(coordinates(path(ii),2),coordinates(path(ii),1),coordinates(path(ii+1),2),coordinates(path(ii+1),1)))*1000;
end

clearvars -except Risc Rafr ACS T_est names coordinates distanceRelative 
% clearvars dist_matrix path new_path new_distance distances ii edges G T i improved j n total_distance ans
