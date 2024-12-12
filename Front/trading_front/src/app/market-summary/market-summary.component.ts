import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ApiService } from '../api.service';
import { MarketSummary } from './market-summary_interface';

@Component({
  selector: 'app-market-summary',
  standalone: true,
  templateUrl: './market-summary.component.html',
  styleUrl: './market-summary.component.css',
  imports: [CommonModule ]
})
export class MarketSummaryComponent implements OnInit{

  marketSummaries: MarketSummary[] | null = null;
  intervalTimes: string[] | null = null;
  selectedInterval: string = '1d'; // Interval par défaut

  constructor(private router: Router, private apiservice: ApiService){}

  ngOnInit(): void {
    this.apiservice.getMarketSummaries().subscribe({
      next: (data) => {
        this.marketSummaries = data; // Assignez les données reçues au tableau
        this.extractUniqueIntervals(); // Appelez cette méthode après avoir reçu les données
      },
      error: (err) => {
        console.error('Erreur lors de la récupération des résumés de marché', err);
      }
    });
  }

  extractUniqueIntervals(): void {
    this.intervalTimes = Array.from(new Set(this.marketSummaries?.map(summary => summary.interval_time )));
    
  }

  selectInterval(interval: string): void {
    this.selectedInterval = interval;
    this.getFilteredSummaries();
  }

  getFilteredSummaries(): any[] {
    let a: any[];
    a = this.marketSummaries?.filter(summary => summary.interval_time == this.selectedInterval) || [];
    return a;
  }

  navigateToStrategyPage(marketName: string, intervalTime: string, strategy: string): void {
    this.router.navigate(['/strategy', strategy], {
      queryParams: {
        market: marketName,
        interval: intervalTime,
        strategy: strategy
      }
    });
  }

  // Fonction pour calculer la couleur dominante
  getBackgroundColor(marketSummary: MarketSummary): string {
    const colors = [
      marketSummary.strategy_tendance_color,
      marketSummary.strategy_macd_color,
      marketSummary.strategy_ichimoku_color,
      marketSummary.strategy_2sma_color,
      marketSummary.strategy_bb_color,
      marketSummary.strategy_rsi_color,
      marketSummary.strategy_stochastic_color
    ];

    const yellowWeight = 2;

    const redCount = colors.filter(color => color === 'red').length;
    const greenCount = colors.filter(color => color === 'green').length;
    const yellowCount = colors.filter(color => color === 'yellow').length * yellowWeight;

    // Déterminer la couleur dominante
    if (redCount > greenCount && redCount > yellowCount) {
      return 'red';
    } else if (greenCount > redCount && greenCount > yellowCount) {
      return 'green';
    } else {
      return 'yellow';
    }
  }
}
