% Script to convert and manage Padova inputs (testato su caso studio di
% Padova - centro storico)

clc
% close all
clear all

%% H, C, DHW reading and parsing
% Lettura ed eleborazione dei dati termici in output dalla simulazione di
% Eureca. Questa sezione legge i file .csv contenenti i dati e ne
% seleziona quelli utilizza simulazione della rete 5GDHC, ovvero i fabbisogni orari di heating,
% cooling e DHW per ogni edifici.

% Percorso della cartella da dove leggere gli input
folder_path = 'ToSend';

% Elenco di tutti i file .csv nella cartella
files = dir(fullfile(folder_path, 'Results *.csv'));
num_files = length(files); % Numero di file
num_rows = 8760; % Numero di righe in ogni file (ore dell'anno)

% Inizializzazione delle variabili per memorizzare i dati
PDsens = NaN(num_rows, num_files); %Fabbisogno sensibile
PDlat = NaN(num_rows, num_files); %Fabbisogno latente
PDpreheat = NaN(num_rows, num_files); %Fabbisogno pre heat
PDpostheat = NaN(num_rows, num_files); %Fabbisogno post heat
ACS = NaN(num_rows, num_files); %DHW

% Inizializza una cella per memorizzare gli #ID
buildings_ID = cell(length(files), 1);

% Loop attraverso ogni file .csv
for i = 1:num_files
    
    name_file = files(i).name; % estrae il nome del file nella cartella

    % Estrai l'ID dal nome del file (assumendo che sia dopo "Building ")
    [~, nome_senza_estensione, ~] = fileparts(name_file);
    posizione_ID = strfind(nome_senza_estensione, 'Building ');
    ID = str2double(nome_senza_estensione(posizione_ID + length('Building '):end));
    
    % Salva l'ID nella lista
    buildings_ID{i} = ID;
   
    % Crea il percorso completo del file
    full_file_path = fullfile(folder_path, name_file);
    % Leggi il file .csv in una variabile temporanea
    temp_data = readtable(full_file_path);
    
    % Seleziono colonne utili e le assegno alle varaibili specifiche
    PDsens(:, i) = temp_data.('TZSensibleLoad_W_');
    PDlat(:, i) = temp_data.('TZLatentLoad_W_');
    PDpreheat(:, i) = temp_data.('TZAHUPreHeaterLoad_W_');
    PDpostheat(:, i) = temp_data.('TZAHUPostHeaterLoad_W_');
    ACS(:, i) = temp_data.('TZDHWDemand_W_');
 
end

% Management dei dati raccolti per generare le variabili necessarie al
% modello 5GDHC

% Variabile ACS (come le altre aggiungo colonna ore per compatibilità con
% modello)
ACS = [(1:8760)',ACS]; 

% Crea una variabile per i valori positivi (heating)
Risc = PDsens + PDlat;
Risc(Risc < 0) = 0;
Risc = [(1:8760)',Risc]; % Aggiungo colonna ore

% Crea una variabile per i valori negativi (cooling)
Rafr = PDsens + PDlat;
Rafr(Rafr > 0) = 0;
Rafr = - Rafr; % Cambio segno per convenzione modello
Rafr = [(1:8760)',Rafr]; % Aggiungo colonna ore

% Crea variabile per i nomi (ID) degli edifici
names = string(buildings_ID');


clearvars -except Risc Rafr ACS T_est names 

% Plot heating and cooling data (solo per scopi di visualizzazione
% preliminare)

figure;
tiledlayout(2,1)
nexttile
colorRisc=copper(size(names,2)+1); %heating colormap
colorRafr=sky(size(names,2)+1); %cooling colormap
hold on;
for i=2:size(names,2)+1
    plot(Risc(:,i),'Color',colorRisc(i,:));
    plot(Rafr(:,i),'Color',colorRafr(i,:));
end

hold off;
title('Hourly heating and cooling output from urban-scale simulation (38 buildings)');
xlabel('Hours'); xlim([1 8760]);
ylabel('Thermal load [kWh]');
grid on;

%% Lettura del file climatico 
% Questo script legge un file .csv generato fuori linea dall'elaborazione
% di un file climatico .epw 

file_path = 'T_est.csv'; % Percorso del file
data = readtable(file_path); % Lettura file .csv
numeric_data = (data{:, 4}); % Estrapolazione quarta colonna, dove è contenuto il dato nuemrico utile (dry bulb temp)

numeric_data = numeric_data(~isnan(numeric_data)); % Ignora i valori non numerici (NaN)

T_est = [(1:length(numeric_data))', numeric_data]; % Crea la variabile t_est

clearvars -except Risc Rafr ACS T_est names 

% Plot heating and cooling data (solo per scopi di visualizzazione
% preliminare)

nexttile
hold on;
plot(T_est(:,2));
hold off;
title('Hourly outdoor temperature');
xlabel('Hours'); xlim([1 8760]);
ylabel('Temperature [°C]');
grid on;
