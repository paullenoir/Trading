import { Component, OnInit, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApexAnnotations, ApexPlotOptions, ApexResponsive, NgApexchartsModule } from 'ng-apexcharts';
import { ApiService } from '../api.service';

import {
  ApexAxisChartSeries,
  ApexChart,
  ApexXAxis,
  ApexYAxis,
  ApexTitleSubtitle,
  ApexDataLabels,
  ApexTooltip
} from 'ng-apexcharts';
import { CommonModule } from '@angular/common';
import { HistoriqueTrade } from './historique_trade_interface';
import { IndicatorMACD } from './indicator_macd_interface';
import { MarketPrice } from './market_price_interface';
import { Tendance } from './tendance_interface';
import { IndicatorEMA } from './indicator_ema';
import { Indicator2sma } from './indicator_2sma';
import { IndicatorIchimoku } from './indicator_ichimoku';
import { IndicatorRSI } from './indicator_rsi';
import { IndicatorStochastic } from './indicator_stochastic';
import { IndicatorBollingerBand } from './indocator_bollingerband';

export type ChartOptions = {
  series: ApexAxisChartSeries[];
  chart: ApexChart;
  xaxis: ApexXAxis;
  yaxis: ApexYAxis[];  // Mise à jour pour accepter un tableau d'axes Y pour plusieurs graphiques
  title: ApexTitleSubtitle;
  tooltip: ApexTooltip;
  dataLabels: ApexDataLabels;
  plotOptions: ApexPlotOptions;  // Ajout pour personnaliser les couleurs des chandeliers
  annotations: ApexAnnotations;  // Ajout pour inclure des annotations comme la ligne zéro pour MACD
  responsive: ApexResponsive[];  // Ajout pour la réactivité en fonction de la taille de l'écran
};


@Component({
  selector: 'app-market-strategy-summary',
  standalone: true,
  imports: [NgApexchartsModule, CommonModule],  // Importation de NgApexchartsModule
  templateUrl: './market-strategy-summary.component.html',
  styleUrls: ['./market-strategy-summary.component.css'],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]  // Ajout de CUSTOM_ELEMENTS_SCHEMA
})
export class MarketStrategySummaryComponent{
  historiqueTrade: HistoriqueTrade[] = [];
  marketPrice : MarketPrice[] = [];
  tendance: Tendance[] = [];
  indicatorema: IndicatorEMA[] = [];
  indicatorMACD: IndicatorMACD[] = [];
  indicator2MM: Indicator2sma[] = [];
  indicatorIchimoku: IndicatorIchimoku [] = [];
  indicatorRSI: IndicatorRSI [] = [];
  indicatorStochastic: IndicatorStochastic [] = [];
  indicatorBollingerBand: IndicatorBollingerBand [] = [];

  public chartOptions: Partial<ChartOptions> | any;
  public chartOptionsMACD: Partial<ChartOptions> | any;
  public chartOptionsRSI: Partial<ChartOptions> | any;
  public chartOptionsStochastic: Partial<ChartOptions> | any;
  allQueryParams: { [key: string]: string } = {}; // Stockera tous les paramètres market,interval,strategy
  MM_courte: string = "MM10";
  MM_longue: string = "MM20";

  constructor(private route: ActivatedRoute, private apiservice: ApiService) {
    this.ngOnInit();
  }

  ngOnInit(): void {
    this.route.queryParamMap.subscribe(params => {
      // `params.keys` contient tous les noms des paramètres
      // `params.get()` est utilisé pour récupérer chaque valeur
      params.keys.forEach(key => {
        this.allQueryParams[key] = params.get(key) ?? ''; // Remplit l'objet avec clé-valeur
      });
    });

    this.apiservice.getMarketPrice(this.allQueryParams['market'], this.allQueryParams['interval']).subscribe({
      next: (data) => {
        this.marketPrice = data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Assignez les données reçues au tableau
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des résumés de marché', err);
      }
    });

    this.apiservice.getHistoricTrade(this.allQueryParams['market'], this.allQueryParams['interval'],this.allQueryParams['strategy']).subscribe({
      next: (data) => {
        this.initializeChart(data);
        this.historiqueTrade = data; // Assignez les données reçues au tableau
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des résumés de marché', err);
      }
    });
  }

  initializeChart(data: any) {    
    const strategy = this.allQueryParams['strategy'];
    if (strategy === 'tendance') {
      this.apiservice.getTendance(this.allQueryParams['market'], this.allQueryParams['interval']).subscribe({
        next: (data) => {
          this.tendance = data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Assignez les données reçues au tableau
        },
        error: (err) => {
          console.error('Erreur lors de la récupération des résumés de marché', err);
        }
      });
      this.apiservice.getIndicatorEMA(this.allQueryParams['market'], this.allQueryParams['interval']).subscribe({
        next: (data) => {
          this.indicatorema = data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Assignez les données reçues au tableau
          this.configureTendanceChart();
        },
        error: (err) => {
          console.error('Erreur lors de la récupération des résumés de marché', err);
        }
      });
      
    } 
    else if (strategy === 'macd') {
      this.apiservice.getIndicatorMACD(this.allQueryParams['market'], this.allQueryParams['interval']).subscribe({
        next: (data) => {
          this.indicatorMACD = data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Assignez les données reçues au tableau
          this.configureMACDChart();
        },
        error: (err) => {
          console.error('Erreur lors de la récupération des résumés de marché', err);
        }
      });
      
    } 
    else if (strategy === 'ichimoku') {
      this.apiservice.getIndicatorIchimoku(this.allQueryParams['market'], this.allQueryParams['interval']).subscribe({
        next: (data) => {
          this.indicatorIchimoku = data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Assignez les données reçues au tableau
          this.configureichimokuChart();
        },
        error: (err) => {
          console.error('Erreur lors de la récupération des résumés de marché', err);
        }
      });
      
    }
    else if (strategy === '2MM') {
      let jsonString = JSON.stringify(data, (key, value) => {
        return value;
      });
      let jsonObject = JSON.parse(jsonString);
      const array = JSON.parse(jsonObject[0]["strategyParameter"]);
      this.MM_courte = "MM" + array[0]
      this.MM_longue = "MM" + array[1]
      this.apiservice.getIndicator2MM(this.allQueryParams['market'], this.allQueryParams['interval']).subscribe({
        next: (data) => {
          this.indicator2MM = data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Assignez les données reçues au tableau
          this.configure2smaChart();
        },
        error: (err) => {
          console.error('Erreur lors de la récupération des résumés de marché', err);
        }
      });

      
    }
    else if (strategy === 'bollingerband') {
      this.apiservice.getIndicatorBollingerBand(this.allQueryParams['market'], this.allQueryParams['interval']).subscribe({
        next: (data) => {
          this.indicatorBollingerBand = data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Assignez les données reçues au tableau
          this.configureBollingerBandsChart();
        },
        error: (err) => {
          console.error('Erreur lors de la récupération des résumés de marché', err);
        }
      });
      
    }
    else if (strategy === 'rsi') {
      this.apiservice.getIndicatorRSI(this.allQueryParams['market'], this.allQueryParams['interval']).subscribe({
        next: (data) => {
          this.indicatorRSI = data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Assignez les données reçues au tableau
          this.configureRSIChart();
        },
        error: (err) => {
          console.error('Erreur lors de la récupération des résumés de marché', err);
        }
      });
      
    } 
    else if (strategy === 'stochastic') {
      this.apiservice.getIndicatorStochastic(this.allQueryParams['market'], this.allQueryParams['interval']).subscribe({
        next: (data) => {
          this.indicatorStochastic = data.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()); // Assignez les données reçues au tableau
          this.configureStochasticChart();
        },
        error: (err) => {
          console.error('Erreur lors de la récupération des résumés de marché', err);
        }
      });
      
    }
  }

  configureTendanceChart(): void {
    this.chartOptions = {
      series: [
        {
          name: 'Market Price',
          type: 'candlestick',
          data: this.marketPrice.map(data => ({
            x: new Date(data.date),
            y: [
              parseFloat(data.open_price),
              parseFloat(data.high_price),
              parseFloat(data.low_price),
              parseFloat(data.close_price)
            ]
          }))
        },
        // Ajout des séries pour les EMA
        {
          name: 'EMA20',
          type: 'line',
          data: this.indicatorema.map(data => ({
            x: new Date(data.date),
            y: parseFloat(data.EMA20)
          })),
          color: '#FF0000'
        },
        {
          name: 'EMA50',
          type: 'line',
          data: this.indicatorema
          .map(data => ({
            x: new Date(data.date),
            y: parseFloat(data.EMA50)
          }))
          .filter(data => !isNaN(data.y)), // Filtre après conversion
          color: '#00FF00' // Vert pour l'EMA50
        },
        {
          name: 'EMA200',
          type: 'line',
          data: this.indicatorema
          .map(data => ({
            x: new Date(data.date),
            y: parseFloat(data.EMA200)
          }))
          .filter(data => !isNaN(data.y)), // Filtre après conversion
          color: '#0000FF' // Bleu pour l'EMA200
        }
      ],
      chart: {
        type: 'line',  // Type général pour permettre l'affichage des deux sections
        height: 450,  // Hauteur totale combinée
        toolbar: {
          show: true
        }
      },
      title: {
        text: 'Market Price with Tendance Strategy',
        align: 'left'
      },
      stroke: {
        width: 1, // Épaisseur de ligne fine (1 pixel)
      },
      xaxis: {
        type: 'datetime',
        labels: {
          format: 'dd MMM yyyy'
        }
      },
      yaxis: [
        {
          title: {
            text: 'Price'
          },
          tooltip: {
            enabled: true
          },
          labels: {
            formatter: (value: number) => {
              return value.toFixed(2); // Affiche la valeur avec 4 chiffres après la virgule
            }
          }
        }
      ],
      tooltip: {
        shared: true,
        x: {
          format: 'dd MMM yyyy'
        }
      },
      plotOptions: {
        candlestick: {
          colors: {
            upward: '#ffffff',  // Bougie haussière blanche
            downward: '#ff0000' // Bougie baissière rouge
          },
          wick: {
            useFillColor: true
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        position: 'top'
      },
      annotations: {
        xaxis: this.historiqueTrade.map(trade => {
          const startDate = new Date(trade.date_start);
          const endDate = trade.date_end ? new Date(trade.date_end) : new Date(); // Si pas de `date_end`, utiliser `date_start`

          return {
            x: startDate.getTime(),
            x2: endDate.getTime(),
            y: 0,  // Ajustez en fonction de votre échelle
            y2: 20, 
            fillColor: trade.date_end ? (!trade.dollars_profit.startsWith('-') ? '#90EE90' : '#FFB6C1') : '#FFA500', // Jaune si trade en cours (pas de date_end)
            opacity: 0.2,
            borderColor: '#000000',
            label: {
              text: trade.date_end ? `${parseFloat(trade.percent_profit).toFixed(2)}%` : 'En cours',
              style: {
                color: '#000000',
                background: '#ffffff'
              }
            }
          };
        }),
      },
      grid: {
        row: {
          colors: ['#f3f3f3', 'transparent'], // Couleurs alternées pour chaque ligne
          opacity: 0.5
        }
      },
      responsive: [
        {
          breakpoint: 600,
          options: {
            chart: {
              height: 600
            },
            legend: {
              position: 'bottom'
            }
          }
        }
      ]
    };
  }

  configureMACDChart(): void {
    this.chartOptions = {
      series: [
        {
          name: 'Market Price',
          type: 'candlestick',
          data: this.marketPrice.map(data => ({
            x: new Date(data.date),
            y: [
              parseFloat(data.open_price),
              parseFloat(data.high_price),
              parseFloat(data.low_price),
              parseFloat(data.close_price)
            ]
          }))
        }
      ],
      chart: {
        type: 'line',  // Type général pour permettre l'affichage des deux sections
        height: 450,  // Hauteur totale combinée
        toolbar: {
          show: true
        }
      },
      title: {
        text: 'Market Price with MACD Strategy',
        align: 'left'
      },
      xaxis: {
        type: 'datetime',
        labels: {
          format: 'dd MMM yyyy'
        }
      },
      yaxis: [
        {
          title: {
            text: 'Price'
          },
          tooltip: {
            enabled: true
          },
          labels: {
            formatter: (value: number) => {
              return value.toFixed(2); // Affiche la valeur avec 4 chiffres après la virgule
            }
          }
        }
      ],
      tooltip: {
        shared: true,
        x: {
          format: 'dd MMM yyyy'
        }
      },
      plotOptions: {
        candlestick: {
          colors: {
            upward: '#ffffff',  // Bougie haussière blanche
            downward: '#ff0000' // Bougie baissière rouge
          },
          wick: {
            useFillColor: true
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        position: 'top'
      },
      // Ajout d'une deuxième section pour MACD
      annotations: {
        xaxis: this.historiqueTrade.map(trade => {
          const startDate = new Date(trade.date_start);
          const endDate = trade.date_end ? new Date(trade.date_end) : new Date(); // Si pas de `date_end`, utiliser `date_start`
  
          return {
              x: startDate.getTime(),
              x2: endDate.getTime(),
              y: 0,  // Ajustez en fonction de votre échelle
              y2: 20, 
              fillColor: trade.date_end ? (!trade.dollars_profit.startsWith('-') ? '#90EE90' : '#FFB6C1') : '#FFA500', // Jaune si trade en cours (pas de date_end)
              opacity: 0.2,
              borderColor: '#000000',
              label: {
                  text: trade.date_end ? `${parseFloat(trade.percent_profit).toFixed(2)}%` : 'En cours',
                  style: {
                      color: '#000000',
                      background: '#ffffff'
                  }
              }
          };
      })
    },
      grid: {
        row: {
          colors: ['#f3f3f3', 'transparent'], // Couleurs alternées pour chaque ligne
          opacity: 0.5
        }
      },
      responsive: [
        {
          breakpoint: 600,
          options: {
            chart: {
              height: 600
            },
            legend: {
              position: 'bottom'
            }
          }
        }
      ]
    };
  
    // Options pour le graphique MACD en dessous
    this.chartOptionsMACD = {
      series: [
        {
          name: 'MACD Line',
          type: 'line',
          data: this.indicatorMACD.map(data => ({
            x: new Date(data.date),
            y: parseFloat(data.macd)
          })),
          color: '#00bfff'  // Bleu pour la ligne MACD
        },
        {
          name: 'MACD Signal Line',
          type: 'line',
          data: this.indicatorMACD.map(data => ({
            x: new Date(data.date),
            y: parseFloat(data.macd_signal)
          })),
          color: '#ff6347'  // Rouge pour la ligne du signal MACD
        },
        {
          name: 'MACD Histogram',
          type: 'column',
          data: this.indicatorMACD.map(data => ({
            x: new Date(data.date),
            y: parseFloat(data.macd_histogram)
          })),
          color: '#90ee90'  // Vert clair pour l'histogramme MACD
        }
      ],
      chart: {
        height: 150,
        type: 'line',
        toolbar: {
          show: false
        }
      },
      xaxis: {
        type: 'datetime',
        labels: {
          show: false  // On masque les labels pour éviter la redondance
        }
      },
      yaxis: {
        title: {
          text: 'MACD'
        },
        labels: {
          formatter: (value: number) => {
            return value.toFixed(2); // Affiche la valeur avec 4 chiffres après la virgule
          }
        }
      },
      grid: {
        borderColor: '#f1f1f1'
      }
    };
  }

  configureichimokuChart(): void{
    this.chartOptions = {
      series: [
        {
          name: 'Market Price',
          type: 'candlestick',
          data: this.marketPrice.map(data => ({
            x: new Date(data.date),
            y: [
              parseFloat(data.open_price),
              parseFloat(data.high_price),
              parseFloat(data.low_price),
              parseFloat(data.close_price)
            ]
          }))
        },
        {
          name: 'Conversion Line (Tenkan-sen)',
          type: 'line',
          data: this.indicatorIchimoku.map(data => ({
              x: new Date(data.date),
              y: parseFloat(data.Ichimoku_Conversion)
          })),
          color: '#FF7F0E' // Orange
        },
        {
          name: 'Base Line (Kijun-sen)',
          type: 'line',
          data: this.indicatorIchimoku.map(data => ({
              x: new Date(data.date),
              y: parseFloat(data.Ichimoku_Base)
          })),
          color: '#1F77B4' // Bleu
        },
        {
          name: 'Leading Span A (Senkou Span A)',
          type: 'line',
          data: this.indicatorIchimoku.map(data => ({
              x: new Date(data.date),
              y: parseFloat(data.Ichimoku_LeadingA)
          })),
          color: '#2CA02C' // Vert
        },
        {
          name: 'Leading Span B (Senkou Span B)',
          type: 'line',
          data: this.indicatorIchimoku.map(data => ({
              x: new Date(data.date),
              y: parseFloat(data.Ichimoku_LeadingB)
          })),
          color: '#D62728' // Rouge
        },
        {
          name: 'Lagging Span (Chikou Span)',
          type: 'line',
          data: this.indicatorIchimoku.map(data => ({
              x: new Date(data.date),
              y: parseFloat(data.Ichimoku_Lagging)
          })),
          color: '#9467BD' // Violet
        }
      ],
      chart: {
        type: 'line',  // Type général pour permettre l'affichage des deux sections
        height: 450,  // Hauteur totale combinée
        toolbar: {
          show: true
        }
      },
      title: {
        text: 'Market Price with Tendance Strategy',
        align: 'left'
      },
      stroke: {
        width: 1, // Épaisseur de ligne fine (1 pixel)
      },
      xaxis: {
        type: 'datetime',
        labels: {
          format: 'dd MMM yyyy'
        }
      },
      yaxis: [
        {
          title: {
            text: 'Price'
          },
          tooltip: {
            enabled: true
          },
          labels: {
            formatter: (value: number) => {
              return value.toFixed(2); // Affiche la valeur avec 4 chiffres après la virgule
            }
          }
        }
      ],
      tooltip: {
        shared: true,
        x: {
          format: 'dd MMM yyyy'
        }
      },
      plotOptions: {
        candlestick: {
          colors: {
            upward: '#ffffff',  // Bougie haussière blanche
            downward: '#ff0000' // Bougie baissière rouge
          },
          wick: {
            useFillColor: true
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        position: 'top'
      },
      annotations: {
        xaxis: this.historiqueTrade.map(trade => {
          const startDate = new Date(trade.date_start);
          const endDate = trade.date_end ? new Date(trade.date_end) : new Date(); // Si pas de `date_end`, utiliser `date_start`

          return {
            x: startDate.getTime(),
            x2: endDate.getTime(),
            y: 0,  // Ajustez en fonction de votre échelle
            y2: 20, 
            fillColor: trade.date_end ? (!trade.dollars_profit.startsWith('-') ? '#90EE90' : '#FFB6C1') : '#FFA500', // Jaune si trade en cours (pas de date_end)
            opacity: 0.2,
            borderColor: '#000000',
            label: {
              text: trade.date_end ? `${parseFloat(trade.percent_profit).toFixed(2)}%` : 'En cours',
              style: {
                color: '#000000',
                background: '#ffffff'
              }
            }
          };
        }),
      },
      grid: {
        row: {
          colors: ['#f3f3f3', 'transparent'], // Couleurs alternées pour chaque ligne
          opacity: 0.5
        }
      },
      responsive: [
        {
          breakpoint: 600,
          options: {
            chart: {
              height: 600
            },
            legend: {
              position: 'bottom'
            }
          }
        }
      ]
    };
  }

  configure2smaChart(): void{
    this.chartOptions = {
      series: [
        {
          name: 'Market Price',
          type: 'candlestick',
          data: this.marketPrice.map(data => ({
            x: new Date(data.date),
            y: [
              parseFloat(data.open_price),
              parseFloat(data.high_price),
              parseFloat(data.low_price),
              parseFloat(data.close_price)
            ]
          }))
        },
        // Ajout des séries pour les EMA
        {
          name: this.MM_courte,
          type: 'line',
          data: this.indicator2MM.map(data => ({
            x: new Date(data.date),
            y: parseFloat(data[this.MM_courte] as string) // Accès dynamique sécurisé
          })),
          color: '#FF0000'
        },
        {
          name: this.MM_longue,
          type: 'line',
          data: this.indicator2MM.map(data => ({
            x: new Date(data.date),
            y: parseFloat(data[this.MM_longue] as string) // Accès dynamique sécurisé
          })),
          color: '#0000FF'
        }
      ],
      chart: {
        type: 'line',  // Type général pour permettre l'affichage des deux sections
        height: 450,  // Hauteur totale combinée
        toolbar: {
          show: true
        }
      },
      title: {
        text: 'Market Price with Tendance Strategy',
        align: 'left'
      },
      stroke: {
        width: 1, // Épaisseur de ligne fine (1 pixel)
      },
      xaxis: {
        type: 'datetime',
        labels: {
          format: 'dd MMM yyyy'
        }
      },
      yaxis: [
        {
          title: {
            text: 'Price'
          },
          tooltip: {
            enabled: true
          },
          labels: {
            formatter: (value: number) => {
              return value.toFixed(2); // Affiche la valeur avec 4 chiffres après la virgule
            }
          }
        }
      ],
      tooltip: {
        shared: true,
        x: {
          format: 'dd MMM yyyy'
        }
      },
      plotOptions: {
        candlestick: {
          colors: {
            upward: '#ffffff',  // Bougie haussière blanche
            downward: '#ff0000' // Bougie baissière rouge
          },
          wick: {
            useFillColor: true
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        position: 'top'
      },
      annotations: {
        xaxis: this.historiqueTrade.map(trade => {
          const startDate = new Date(trade.date_start);
          const endDate = trade.date_end ? new Date(trade.date_end) : new Date(); // Si pas de `date_end`, utiliser `date_start`

          return {
            x: startDate.getTime(),
            x2: endDate.getTime(),
            y: 0,  // Ajustez en fonction de votre échelle
            y2: 20, 
            fillColor: trade.date_end ? (!trade.dollars_profit.startsWith('-') ? '#90EE90' : '#FFB6C1') : '#FFA500', // Jaune si trade en cours (pas de date_end)
            opacity: 0.2,
            borderColor: '#000000',
            label: {
              text: trade.date_end ? `${parseFloat(trade.percent_profit).toFixed(2)}%` : 'En cours',
              style: {
                color: '#000000',
                background: '#ffffff'
              }
            }
          };
        }),
      },
      grid: {
        row: {
          colors: ['#f3f3f3', 'transparent'], // Couleurs alternées pour chaque ligne
          opacity: 0.5
        }
      },
      responsive: [
        {
          breakpoint: 600,
          options: {
            chart: {
              height: 600
            },
            legend: {
              position: 'bottom'
            }
          }
        }
      ]
    };
  }

  configureBollingerBandsChart(): void {
    this.chartOptions = {
        series: [
            {
                name: 'Market Price',
                type: 'candlestick',
                data: this.marketPrice.map(data => ({
                    x: new Date(data.date),
                    y: [
                        parseFloat(data.open_price),
                        parseFloat(data.high_price),
                        parseFloat(data.low_price),
                        parseFloat(data.close_price)
                    ]
                }))
            },
            {
                name: 'Lower Band',
                type: 'line',
                data: this.indicatorBollingerBand.map(data => ({
                    x: new Date(data.date),
                    y: parseFloat(data.BB_Lower)
                })),
                color: '#FF0000' // Rouge pour la bande inférieure
            },
            {
                name: 'Middle Band',
                type: 'line',
                data: this.indicatorBollingerBand.map(data => ({
                    x: new Date(data.date),
                    y: parseFloat(data.BB_Middle)
                })),
                color: '#0000FF' // Bleu pour la bande médiane
            },
            {
                name: 'Upper Band',
                type: 'line',
                data: this.indicatorBollingerBand.map(data => ({
                    x: new Date(data.date),
                    y: parseFloat(data.BB_Upper)
                })),
                color: '#00FF00' // Vert pour la bande supérieure
            }
        ],
        chart: {
            type: 'line', // Type général
            height: 450,
            toolbar: {
                show: true
            }
        },
        title: {
            text: 'Market Price with Bollinger Bands',
            align: 'left'
        },
        stroke: {
            width: 1
        },
        xaxis: {
            type: 'datetime',
            labels: {
                format: 'dd MMM yyyy'
            }
        },
        yaxis: [
            {
                title: {
                    text: 'Price'
                },
                labels: {
                    formatter: (value: number) => {
                        return value.toFixed(2);
                    }
                }
            }
        ],
        tooltip: {
            shared: true,
            x: {
                format: 'dd MMM yyyy'
            }
        },
        dataLabels: {
            enabled: false
        },
        legend: {
            position: 'top'
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'],
                opacity: 0.5
            }
        },
        responsive: [
            {
                breakpoint: 600,
                options: {
                    chart: {
                        height: 600
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        ]
    };
  }

  //comme MACD A refaire
  configureRSIChart(): void {
    this.chartOptions = {
      series: [
        {
          name: 'Market Price',
          type: 'candlestick',
          data: this.marketPrice.map(data => ({
            x: new Date(data.date),
            y: [
              parseFloat(data.open_price),
              parseFloat(data.high_price),
              parseFloat(data.low_price),
              parseFloat(data.close_price)
            ]
          }))
        }
      ],
      chart: {
        type: 'line',  // Type général pour permettre l'affichage des deux sections
        height: 450,  // Hauteur totale combinée
        toolbar: {
          show: true
        }
      },
      title: {
        text: 'Market Price with MACD Strategy',
        align: 'left'
      },
      xaxis: {
        type: 'datetime',
        labels: {
          format: 'dd MMM yyyy'
        }
      },
      yaxis: [
        {
          title: {
            text: 'Price'
          },
          tooltip: {
            enabled: true
          },
          labels: {
            formatter: (value: number) => {
              return value.toFixed(2); // Affiche la valeur avec 4 chiffres après la virgule
            }
          }
        }
      ],
      tooltip: {
        shared: true,
        x: {
          format: 'dd MMM yyyy'
        }
      },
      plotOptions: {
        candlestick: {
          colors: {
            upward: '#ffffff',  // Bougie haussière blanche
            downward: '#ff0000' // Bougie baissière rouge
          },
          wick: {
            useFillColor: true
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        position: 'top'
      },
      // Ajout d'une deuxième section pour MACD
      annotations: {
        xaxis: this.historiqueTrade.map(trade => {
          const startDate = new Date(trade.date_start);
          const endDate = trade.date_end ? new Date(trade.date_end) : new Date(); // Si pas de `date_end`, utiliser `date_start`
  
          return {
              x: startDate.getTime(),
              x2: endDate.getTime(),
              y: 0,  // Ajustez en fonction de votre échelle
              y2: 20, 
              fillColor: trade.date_end ? (!trade.dollars_profit.startsWith('-') ? '#90EE90' : '#FFB6C1') : '#FFA500', // Jaune si trade en cours (pas de date_end)
              opacity: 0.2,
              borderColor: '#000000',
              label: {
                  text: trade.date_end ? `${parseFloat(trade.percent_profit).toFixed(2)}%` : 'En cours',
                  style: {
                      color: '#000000',
                      background: '#ffffff'
                  }
              }
          };
      })
    },
      grid: {
        row: {
          colors: ['#f3f3f3', 'transparent'], // Couleurs alternées pour chaque ligne
          opacity: 0.5
        }
      },
      responsive: [
        {
          breakpoint: 600,
          options: {
            chart: {
              height: 600
            },
            legend: {
              position: 'bottom'
            }
          }
        }
      ]
    };
    this.chartOptionsRSI = {
      series: [
          {
              name: 'RSI 7',
              type: 'line',
              data: this.indicatorRSI.map(data => ({
                  x: new Date(data.date),
                  y: parseFloat(data.rsi_7)
              })),
              color: '#00bfff' // Bleu pour le RSI 7
          },
          {
              name: 'RSI 14',
              type: 'line',
              data: this.indicatorRSI.map(data => ({
                  x: new Date(data.date),
                  y: parseFloat(data.rsi_14)
              })),
              color: '#ff6347' // Rouge pour le RSI 14
          },
          {
              name: 'RSI 21',
              type: 'line',
              data: this.indicatorRSI.map(data => ({
                  x: new Date(data.date),
                  y: parseFloat(data.rsi_21)
              })),
              color: '#90ee90' // Vert clair pour le RSI 21
          }
      ],
      chart: {
          height: 150,
          type: 'line',
          toolbar: {
              show: false
          }
      },
      xaxis: {
          type: 'datetime',
          labels: {
              show: false // On masque les labels pour éviter la redondance
          }
      },
      yaxis: {
          title: {
              text: 'RSI'
          },
          labels: {
              formatter: (value: number) => {
                  return value.toFixed(2); // Affiche la valeur avec 2 chiffres après la virgule
              }
          }
      },
      grid: {
          borderColor: '#f1f1f1'
      }
  };
  
  }

  //comme MACD A refaire
  configureStochasticChart(): void{
    this.chartOptions = {
      series: [
        {
          name: 'Market Price',
          type: 'candlestick',
          data: this.marketPrice.map(data => ({
            x: new Date(data.date),
            y: [
              parseFloat(data.open_price),
              parseFloat(data.high_price),
              parseFloat(data.low_price),
              parseFloat(data.close_price)
            ]
          }))
        }
      ],
      chart: {
        type: 'line',  // Type général pour permettre l'affichage des deux sections
        height: 450,  // Hauteur totale combinée
        toolbar: {
          show: true
        }
      },
      title: {
        text: 'Market Price with MACD Strategy',
        align: 'left'
      },
      xaxis: {
        type: 'datetime',
        labels: {
          format: 'dd MMM yyyy'
        }
      },
      yaxis: [
        {
          title: {
            text: 'Price'
          },
          tooltip: {
            enabled: true
          },
          labels: {
            formatter: (value: number) => {
              return value.toFixed(2); // Affiche la valeur avec 4 chiffres après la virgule
            }
          }
        }
      ],
      tooltip: {
        shared: true,
        x: {
          format: 'dd MMM yyyy'
        }
      },
      plotOptions: {
        candlestick: {
          colors: {
            upward: '#ffffff',  // Bougie haussière blanche
            downward: '#ff0000' // Bougie baissière rouge
          },
          wick: {
            useFillColor: true
          }
        }
      },
      dataLabels: {
        enabled: false
      },
      legend: {
        position: 'top'
      },
      // Ajout d'une deuxième section pour MACD
      annotations: {
        xaxis: this.historiqueTrade.map(trade => {
          const startDate = new Date(trade.date_start);
          const endDate = trade.date_end ? new Date(trade.date_end) : new Date(); // Si pas de `date_end`, utiliser `date_start`
  
          return {
              x: startDate.getTime(),
              x2: endDate.getTime(),
              y: 0,  // Ajustez en fonction de votre échelle
              y2: 20, 
              fillColor: trade.date_end ? (!trade.dollars_profit.startsWith('-') ? '#90EE90' : '#FFB6C1') : '#FFA500', // Jaune si trade en cours (pas de date_end)
              opacity: 0.2,
              borderColor: '#000000',
              label: {
                  text: trade.date_end ? `${parseFloat(trade.percent_profit).toFixed(2)}%` : 'En cours',
                  style: {
                      color: '#000000',
                      background: '#ffffff'
                  }
              }
          };
      })
    },
      grid: {
        row: {
          colors: ['#f3f3f3', 'transparent'], // Couleurs alternées pour chaque ligne
          opacity: 0.5
        }
      },
      responsive: [
        {
          breakpoint: 600,
          options: {
            chart: {
              height: 600
            },
            legend: {
              position: 'bottom'
            }
          }
        }
      ]
    };
    this.chartOptionsStochastic = {
      series: [
          {
              name: '%K Line',
              type: 'line',
              data: this.indicatorStochastic.map(data => ({
                  x: new Date(data.date),
                  y: parseFloat(data.stochastic_k)
              })),
              color: '#1E90FF' // Bleu pour la ligne %K
          },
          {
              name: '%D Line',
              type: 'line',
              data: this.indicatorStochastic.map(data => ({
                  x: new Date(data.date),
                  y: parseFloat(data.stochastic_d)
              })),
              color: '#FF6347' // Rouge pour la ligne %D
          }
      ],
      chart: {
          height: 150,
          type: 'line',
          toolbar: {
              show: false
          }
      },
      xaxis: {
          type: 'datetime',
          labels: {
              show: false // Masque les labels pour éviter la redondance
          }
      },
      yaxis: {
          title: {
              text: 'Stochastic'
          },
          labels: {
              formatter: (value: number) => {
                  return value.toFixed(2); // Affiche la valeur avec 2 chiffres après la virgule
              }
          }
      },
      grid: {
          borderColor: '#f1f1f1'
      }
  };
  
  }

  calculateTotalDollarsProfit(): number {
    return this.historiqueTrade
      .map(trade => parseFloat(trade.dollars_profit) || 0) // Convertit en nombre et gère les valeurs non valides
      .reduce((total, profit) => total + profit, 0); // Calcule la somme totale
  }
}