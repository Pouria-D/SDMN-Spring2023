% IN The Name OF GOD
% SDMN Course SPring 1402
% HW3 - OFDM Implementation 
% Pouria Dadkhah - 401201381

clc;
clear;
close all;

% OFDM parameters
fs = 1; % 15.36e6;
N = 16; % 512;
% guard = 5.7e-6;
cpLen = 3; % round(guard * fs);
symLen = N + cpLen;

% Channel parameters
% tau = 5e-6;
% amp = 0.8;
% delay = round(tau * fs);
% h = zeros(1, N);
% h(1) = 1;
% h(delay) = amp;
h = [1 0.8 0.5 0.2];
H = fft(h, N);

% Input sequence
xLen = 16; %10240;
% x = zeros(1, inLen);
x = [1 0 0 0 1 1 0 0 1 0 1 0 0 1 1 0];
% x = randi([0 1], 1, xLen);

figure()
stem(0:length(x) - 1, abs(x))
legend('X[k]')
grid on

% Tx
Nsym = ceil(xLen / N);
tx = zeros(1, Nsym * symLen);
for i = 1:Nsym
    x1 = (i - 1) * N + 1; x2 = i * N;
    tx1 = (i - 1) * symLen + 1; tx2 = i * symLen;
    tx(tx1 + cpLen:tx2) = ifft(x(x1:x2));
    tx(tx1:tx1 + cpLen - 1) = tx(tx2 - cpLen + 1:tx2);
end

figure()
subplot(1,3,1)
stem((0:length(tx) - 1) / fs, abs(tx))
legend('cp\_x[n]')
grid on

% Channel
rx = conv(tx, h);

% figure()
subplot(1,3,2)
stem((0:length(rx) - 1) / fs, abs(rx))
legend('|y[n]|')
grid on

% Rx
y = zeros(1, Nsym * N);
Hx = zeros(1, Nsym * N);
for i = 1:Nsym
    y1 = (i - 1) * N + 1; y2 = i * N;
    rx1 = (i - 1) * symLen + 1; rx2 = i * symLen;
    y(y1:y2) = fft(rx(rx1 + cpLen:rx2));
    Hx(y1:y2) = H .* x(y1:y2);
end

% figure()
subplot(1,3,3)
hold on
stem((0:length(y) - 1) / fs, abs(y))
stem((0:length(Hx) - 1) / fs, abs(Hx))
legend('|Y[k]|', '|H[k]X[k]|')
grid on

% Equalizer
seq = zeros(1, Nsym * N);
for i = 1:Nsym
    y1 = (i - 1) * N + 1; y2 = i * N;
    seq1 = (i - 1) * N + 1; seq2 = i * N;
    seq(y1:y2) = y(y1:y2) ./ H;
end

seq = (abs(seq) >= 0.5) + 0;

figure()
stem(0:length(x) - 1, x)
hold on
stem(0:length(x) - 1, seq)
title('Output Bit Sequence')
grid on
ber = biterr(x, seq);
